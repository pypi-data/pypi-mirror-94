import asyncio

import click
import rich

from .utils import CONTEXT_SETTINGS
from ..utils import handle_credentials


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--server", help="Coiled server to use")
@click.option("-t", "--token", help="Coiled user token")
@click.option(
    "--retry/--no-retry",
    default=True,
    help="Whether or not to automatically ask for a new token if an invalid token is entered",
)
def login(server, token, retry):
    """Configure your Coiled account credentials"""
    try:
        asyncio.get_event_loop().run_until_complete(
            handle_credentials(server=server, token=token, save=True, retry=retry)
        )
    except ImportError as e:
        rich.print(f"[red]{e}")
