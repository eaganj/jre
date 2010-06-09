try:
    from collections import namedtuple
except ImportError:
    from namedtuple import namedtuple

try:
    from collections import OrderedDict
except ImportError:
    from odict2 import OrderedDict

import ConfigParser26
import subprocess26

__all__ = 'namedtuple OrderedDict ConfigParser26 subprocess26'.split()
