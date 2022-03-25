from pkg_resources import get_distribution, DistributionNotFound
from .version import __version__ as v


def version_report():
    print(__version__)
    return __version__


try:
    version = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    version = "unknown"

__title__ = "0x20bf"
__author__ = "@RandyMcMillan, @BitKarrot"
__version__ = v
__license__ = "Apache License 2.0"
__copyright__ = "Copyright 2022 0x20bf.org"

"""
:copyright: (c) 2022 0x20bf.org
:license: Apache License 2.0, see LICENSE for more details.
"""
