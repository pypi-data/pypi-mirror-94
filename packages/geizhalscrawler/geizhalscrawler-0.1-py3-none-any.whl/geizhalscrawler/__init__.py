"""Init file for Geizhalscrawler."""
from pkg_resources import get_distribution, DistributionNotFound
from .geizhalscrawler import Device, Geizhals

NAME = "geizhalscrawler"
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
