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

import weakref
            
class Observable(object):
    def __init__(self, *eventNames):
        self._listeners = {}
        self.notify = ObservableNotifier(self, eventNames)
    
    def register(self, listener, **callbacks):
        ''' 
        Register a listener for the observable.  `callbacks` should be a mapping of event names
        to the callbacks that should be invoked when the event fires.
        '''
        
        try:
            key = weakref.ref(listener)
        except TypeError:
            key = listener # FIXME: silently stores a non-weak-ref.
            
        self._listeners[listener] = callbacks
    
    def unregister(self, listener):
        del self._listeners[listener]

    def registerEvent(self, eventName):
        self.notify._events.append(eventName)
    
    def _fireNotification(self, event, *args, **kw):
        # Make sure we iterate over a copy in case any listeners unregister themselves.
        listeners = self._listeners.items() 
        for listener, callbacks in listeners:
            if isinstance(listener, weakref.ref):
                if not listener():
                    del self._listeners[listener]
                    continue
                listener = listener() # de-ref
                
            if not callbacks.has_key(event):
                if hasattr(listener, event):
                    getattr(listener, event)(*args, **kw)
                else:
                    pass # Silently ignore undefined event handlers
            else:
                callbacks[event](*args, **kw)
            
class ObservableNotifier(object):
    def __init__(self, observable, events):
        self._observable = observable
        self._events = set(events)
    
    def __getattr__(self, name):
        if self.__dict__.has_key(name): 
            return self.__dict__[name]
        if name in self._events:
            return ObservableNotifierProxy(self._observable, name)
        raise AttributeError(name)

class ObservableNotifierProxy(object):
    def __init__(self, observable, event):
        self._observable = observable
        self._event = event
    
    def __call__(self, *args, **kw):
        self._observable._fireNotification(self._event, *args, **kw)