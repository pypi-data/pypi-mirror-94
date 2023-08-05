import asyncio
import sys
import subprocess
import contextlib
import functools
import json
import os
import ssl
import tempfile
from typing import Union, Tuple, Optional
import yaml
import sys
import threading
import itertools
import time
import re
import warnings

import aiohttp
import click
import dask
from dask.distributed import Security
import rich

from .compatibility import COILED_VERSION, PY_VERSION


class GatewaySecurity(Security):
    """A security implementation that temporarily stores credentials on disk.

    The normal ``Security`` class assumes credentials already exist on disk,
    but our credentials exist only in memory. Since Python's SSLContext doesn't
    support directly loading credentials from memory, we write them temporarily
    to disk when creating the context, then delete them immediately."""

    def __init__(self, tls_key, tls_cert):
        self.tls_key = tls_key
        self.tls_cert = tls_cert

    def __repr__(self):
        return "GatewaySecurity<...>"

    def get_connection_args(self, role):
        with tempfile.TemporaryDirectory() as tempdir:
            key_path = os.path.join(tempdir, "dask.pem")
            cert_path = os.path.join(tempdir, "dask.crt")
            with open(key_path, "w") as f:
                f.write(self.tls_key)
            with open(cert_path, "w") as f:
                f.write(self.tls_cert)
            ctx = ssl.create_default_context(
                purpose=ssl.Purpose.SERVER_AUTH, cafile=cert_path
            )
            ctx.verify_mode = ssl.CERT_REQUIRED
            ctx.check_hostname = False
            ctx.load_cert_chain(cert_path, key_path)
        return {"ssl_context": ctx, "require_encryption": True}


async def handle_api_exception(response, exception_cls=Exception):
    with contextlib.suppress(aiohttp.ContentTypeError, json.JSONDecodeError):
        # First see if it's an error we created that has a more useful
        # message
        error_body = await response.json()
        if "message" in error_body:
            raise exception_cls(error_body["message"])
        else:
            raise exception_cls(", ".join(f"{k}={v}" for (k, v) in error_body.items()))

    error_text = await response.text()

    if not error_text:
        # Response contains no text/body, let's not raise an empty exception
        error_text = f"{response.status} - {response.reason}"
    raise Exception(error_text)


def normalize_server(server: str) -> str:
    # Check if using an older server
    if "beta.coiledhq.com" in server or "beta.coiled.io" in server:
        # NOTE: https is needed here as http is not redirecting
        server = "https://cloud.coiled.io"

    return server


async def handle_credentials(
    *,
    server: str = None,
    token: str = None,
    save: Union[bool, None] = None,
    retry: bool = True,
) -> Tuple[str, str, str]:
    """Validate and optionally save credentials

    Parameters
    ----------
    server
        Server to connect to. If not specified, will check the
        ``coiled.server`` configuration value.
    token
        Coiled user token to use. If not specified, will prompt user
        to input token.
    save
        Whether or not save credentials to coiled config file.
        If ``None``, will ask for input on whether or not credentials
        should be saved. Defaults to None.
    retry
        Whether or not to try again if invalid credentials are entered.
        Retrying is often desired in interactive situations, but not
        in more programmatic scenerios. Defaults to True.

    Returns
    -------
    user
        Username
    token
        User API token
    server
        Server being used
    """
    # If testing locally with `ngrok` we need to
    # rewrite the server to localhost
    server = server or dask.config.get("coiled.server")
    server = normalize_server(server)
    login_url = f"{server}/profile"
    if token is None:
        rich.print(f"Please login to [link]{login_url}[/link] to get your token")
        token = click.prompt(
            "Token", hide_input=True
        )  # Using click instead of getpass to make testing easier

    # Validate token and get username
    async with aiohttp.ClientSession(
        headers={"Authorization": "Token " + token, "Client-Version": COILED_VERSION}
    ) as session:
        response = await session.request("GET", server + "/api/v1/users/me/")
        data = await response.json()
        if response.status == 426:
            # Upgrade required
            await handle_api_exception(response, exception_cls=ImportError)
        if response.status >= 400:
            if retry and "Invalid token" in data.get("detail", ""):
                # Token is not valid, ask for a new one
                rich.print(
                    "[red]Invalid Coiled token encountered. Typically this occurs after logging out of "
                    f"{server} which resets your token for security reasons.\n"
                )
                return await handle_credentials(server=server, token=None, save=None)
            else:
                await handle_api_exception(response)

    user = data["username"]

    # Avoid extra printing when creating clusters
    if save is not False:
        rich.print("[green]Authentication successful")

    if save is None:
        # Optionally save user credentials for next time
        save_creds = input("Save credentials for next time? [Y/n]: ")
        if save_creds.lower() in ("y", "yes", ""):
            save = True
    if save:
        default_file = os.path.join(os.path.dirname(__file__), "coiled.yaml")
        config_file = os.path.join(
            os.path.expanduser("~"), ".config", "dask", "coiled.yaml"
        )
        # Make sure directory with config exists
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        configs = dask.config.collect_yaml([default_file, config_file])
        creds = {
            "coiled": {
                "user": user,
                "token": token,
                "server": server,
            }
        }
        config = dask.config.merge(*configs, creds)
        with open(config_file, "w") as f:
            f.write(yaml.dump(config))
        rich.print(f"Credentials have been saved at [blue]{config_file}")
        # Make sure saved configuration values are set for the current Python process
        dask.config.set(config)

    return user, token, server


class Spinner:
    """A spinner context manager to denotate we are still working"""

    def __init__(self, delay=0.2):
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.busy = False

    def write_next(self):
        with self._screen_lock:
            sys.stdout.write(next(self.spinner))
            sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            sys.stdout.write("\b")
            if cleanup:
                sys.stdout.write(" ")  # overwrite spinner with blank
                sys.stdout.write("\r")  # move to next line
            sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write("\r")


def is_slug(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9-_]+$", name))


class ParseIdentifierError(ValueError):
    def __init__(self, which_name):
        super().__init__(
            f"Invalid {which_name}: should have format (<account>/)<name>,"
            ' for example "coiled/xgboost" or "python-37". The <name> '
            ' is required ("xgboost" and "python-37" in the previous examples),'
            " and can contain ASCII letters, numbers, hyphens and underscores."
            f' The account prefix (i.e. "coiled/") can be used to specifies a {which_name}'
            " from a different account."
        )


def parse_identifier(
    identifier: str, property_name: str = "name"
) -> Tuple[Optional[str], str]:
    """
    Parameters
    ----------
    identifier:
        identifier of the resource, i.e. "coiled/xgboost" or "python-37"
    property_name:
        The name of the parameter that was being validated; will be printed
        with any error messages, i.e. "software_environment".

    Examples
    --------
    >>> parse_identifier("coiled/xgboost", "software_environment")
    ("coiled", "xgboost")
    >>> parse_identifier("xgboost", "software_environment")
    (None, "xgboost")

    Raises
    ------
    ParseIdentifierError
    """
    identifiers = identifier.split("/")
    len_full_name = len(identifiers)
    if len_full_name == 1:
        account = None
        name = identifiers[0]
    elif len_full_name == 2:
        account, name = identifiers
    else:
        raise ParseIdentifierError(property_name)

    if not is_slug(name):
        raise ParseIdentifierError(property_name)

    return account, name


def get_platform():
    # Determine platform
    if sys.platform == "linux":
        platform = "linux"
    elif sys.platform == "darwin":
        platform = "osx"
    elif sys.platform == "win32":
        platform = "windows"
    else:
        raise ValueError(f"Invalid platform {sys.platform} encountered")
    return platform


class ExperimentalFeatureWarning(RuntimeWarning):
    """Warning raise by an experimental feature"""

    pass


def experimental(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is an experimental feature which is subject "
            "to breaking changes, being removed, or otherwise updated without notice "
            "and should be used accordingly.",
            ExperimentalFeatureWarning,
        )
        return func(*args, **kwargs)

    return inner


async def run_command_in_subprocess(cmd: str, suppress_error: bool = False):
    """Run the command in subprocess.

    If a user is using a python version < 3.8 then he will get a RuntimeError exception -
    ``Cannot add child handler, the child watcher does not have a loop attached``. As a
    workaround for the issue, we check if the user is running any earlier version of python
    and run the command in subprocess instead.

    For reference on the RuntimeError exception: https://bugs.python.org/issue35621

    """

    if PY_VERSION < "3.8":
        proc = subprocess.Popen(
            cmd.split(" "),
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        for line in proc.stdout:
            yield line.rstrip()

    else:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,  # type: ignore
            stderr=asyncio.subprocess.PIPE,  # type: ignore
        )

        lines = []
        while proc.returncode is None:
            await asyncio.sleep(0.5)
            async for line in proc.stdout:
                line = line.decode().rstrip()
                lines.append(line)
                yield line

            async for line in proc.stderr:
                line = line.decode().rstrip()
                lines.append(line)
                yield line

        if proc.returncode and not suppress_error:
            raise ValueError("\n".join(lines))
