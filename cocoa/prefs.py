# Cocoa preferences utilities
# Copyright (C) 2003-2009 James R. Eagan <eaganjr@acm.org>

from AppKit import *
from Foundation import *
import objc
from PyObjCTools.KeyValueCoding import kvc

class JREPrefs(object):
    '''
    A dict-like interface to NSUserDefaults.
    '''
    
    _sharedInstance = None

    def __init__(self, defaults=None, defaultsDict=None):
        if defaults is None:
            self._defaults = NSUserDefaults.standardUserDefaults()
            if hasattr(self, '_defaultPrefs'):
                self._defaults.registerDefaults_(self._defaultPrefs)
            elif defaultsDict:
                self._defaults.registerDefaults_(defaultsDict)
        else: 
            self._defaults = defaults

    def __getitem__(self, key):
        return self._defaults.valueForKey_(key)

    def __setitem__(self, key, value):
        NSLog(u"defaults.%s = %s" % (key, value))
        self._defaults.setValue_forKey_(value, key)

    @classmethod
    def sharedPreferences(cls):
        if cls._sharedInstance is None:
            cls._sharedInstance = cls()
        return kvc(cls._sharedInstance)
    
    def synchronize(self):
        self._defaults.synchronize()