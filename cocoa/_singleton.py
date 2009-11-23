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