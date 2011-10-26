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

from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

class JRESingleton(NSObject):
    _sharedSingleton = None
    
    def __new__(cls):
        return cls.alloc().init()
    
    
    @classmethod
    def allocWithZone_(cls, zone):
        with objc.object_lock(cls):
            if cls._sharedSingleton is None:
                return super(JRESingleton, cls).allocWithZone_(zone)
        
        return None
    
    
    def init(self):
        self = super(JRESingleton, self).init()
        if not self:
            return self
        
        with objc.object_lock(self.__class__):
            if self.__class__._sharedSingleton is None:
                self.__class__._sharedSingleton = self
        
        return self.__class__._sharedSingleton
    
    
    def copyWithZone_(self, zone):
        return self
    
    @classmethod
    def sharedSingleton(cls):
        if cls._sharedSingleton is None:
            cls.alloc().init()
            
        return cls._sharedSingleton
    
Singleton = JRESingleton

__all__ = ['Singleton']