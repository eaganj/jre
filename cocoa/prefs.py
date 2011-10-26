# Cocoa preferences utilities
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