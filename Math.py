# Misc Math utility functions
# Copyright (C) 2004 James R. Eagan <eaganjr@acm.org>
#
# Created: 040603

import math


def nextPow(p, b=2):
    '''
    Compute the next largest power of b from p.  
    If p is a power of b, then p is returned.

    Assumes `p > 1`.

    :Example: `nextPow(512) -> 512`
    :Example: `nextPow(513) -> 1024`
    '''
    return int(b**(math.ceil(math.log(p, b))))
