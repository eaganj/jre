try:
    from collections import namedtuple
except ImportError:
    from namedtuple import namedtuple

try:
    from collections import OrderedDict
except ImportError:
    from odict import OrderedDict

__all__ = 'namedtuple OrderedDict'.split()
