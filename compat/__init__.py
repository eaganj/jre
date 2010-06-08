try:
    from collections import namedtuple
except ImportError:
    from namedtuple import namedtuple

try:
    from collections import OrderedDict
except ImportError:
    from odict2 import OrderedDict

from ConfigParser26 import ConfigParser as ConfigParser26

__all__ = 'namedtuple OrderedDict ConfigParser26'.split()
