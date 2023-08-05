import sys
from ._version import get_versions
from distutils.version import LooseVersion

COILED_VERSION = get_versions()["version"]

PY_VERSION = LooseVersion(".".join(map(str, sys.version_info[:3])))
