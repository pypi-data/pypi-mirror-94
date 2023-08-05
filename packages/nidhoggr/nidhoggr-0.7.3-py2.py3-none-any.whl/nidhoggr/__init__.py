from os import path
from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution('nidhoggr')
    dist_loc = path.normcase(_dist.location)
    here = path.normcase(__file__)
    if not here.startswith(path.join(dist_loc, 'nidhoggr')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
