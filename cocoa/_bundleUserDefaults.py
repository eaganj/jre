# BundleUserDefaults.py
# Copyright (C) 2009 James R. Eagan <eaganjr@acm.org>
#
# Based on Objective-C version by John Chang on 2007-06-15 under license CC Public Domain
#                                       http://creativecommons.org/licenses/publicdomain
#
# Subclass of NSUserDefaults suitable for use in a plugin so as to store preferences in the plugin bundle's
# own preferences file (e.g. com.yourcompany.plugin.plist) instead of the application's preferences file
# (e.g. com.apple.iApplication.plist).


from Foundation import *
from AppKit import *
from CoreFoundation import *
import objc

import jre.debug

class JREBundleUserDefaults(NSUserDefaults):
    def initWithPersistentDomainName_(self, domain):
        self = super(BundleUserDefaults, self).init()
        if not self:
            return self
            
        self._domain = domain
        self._defaults = {}
        
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, 
                                                                   self._applicationWillTerminate_,
                                                                   NSApplicationWillTerminateNotification,
                                                                   None)
                                                                   
        return self
    
    def dealloc(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        
        super(BundleUserDefaults, self).dealloc()
    
    def _applicationWillTerminate_(self, notification):
        print 'BundleUserDefaults synchronizing before terminate'
        self.synchronize()
    
    def objectForKey_(self, name):
        value = CFPreferencesCopyAppValue(name, self._domain)
        if value == None:
            value = self._defaults.get(name, None)
        return value
    
    def setObject_forKey_(self, value, name):
        CFPreferencesSetAppValue(name, value, self._domain)
    
    def removeObjectForKey_(self, name):
        self.setObject_forKey_(None, name)
    
    def registerDefaults_(self, defaults):
        self._defaults = defaults
    
    def synchronize(self):
        return CFPreferencesSynchronize(self._domain, kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
    
    
    ### Pythonic interface
    def __new__(cls, domain):
        return cls.alloc().initWithPersistentDomainName_(domain)
        
    # These are not needed.  PyObjC already provides convenience methods for just this case!
    #
    # def __getitem__(self, key):
    #     return self.objectForKey_(key)
    # 
    # def __setitem__(self, key, value):
    #     self.setObject_forKey_(value, key)
    # 
    # def __delitem__(self, key):
    #     self.removeObjectForKey_(key)

BundleUserDefaults = JREBundleUserDefaults

__all__ = ['BundleUserDefaults']