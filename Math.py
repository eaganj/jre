# Misc Math utility functions
# JRElib -- Python utility library
# Copyright 2003-2011, James R. Eagan (code at my last name dot me)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

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
