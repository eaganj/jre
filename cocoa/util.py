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

from Foundation import *
from AppKit import *
import objc
from PyObjCTools import AppHelper

class JREAlertSheet(NSObject):
    def __call__(self, *args, **kwargs):
        self.display_message(*args, **kwargs)
        
    def display_message(self, win, title, message, primary=None, secondary=None, tertiary=None,
                        delegate=None, endSheetMethod=None):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
                self._do_display_message, 
                (win, title, message, primary, secondary, tertiary, delegate, endSheetMethod),
                True)
                
    def _do_display_message(self, (win, title, message, primary, secondary, tertiary,
                            delegate, endSheetMethod)):
        if win is None:
            self._display_message_modal(title, message, primary, secondary, tertiary)
        else:
            delegate = delegate or self
            self.__endSheetMethod = endSheetMethod
            NSBeginAlertSheet(title,
                              primary,
                              secondary,
                              tertiary,
                              win,
                              self,
                              self.didEndSheet_returnCode_contextInfo_,
                              None,
                              0,
                              message)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        if self.__endSheetMethod is not None:
            return self.__endSheetMethod(sheet, code, info)
        else:
            sheet.orderOut_(self)
    
    def _display_message_modal(self, title, message, primary, secondary, tertiary):
        NSRunAlertPanel(title, message, u"OK", secondary, tertiary)
            
showAlertForWindow = JREAlertSheet.alloc().init()

def UINOT_IMPLEMENTED(message='This feature is not currently implemented.'):
    message = '%s\n\n%s' % (message, TRACE_STR(1).strip())
    NSRunAlertPanel(u'Not implemented', message, u'OK', None, None)
    
def makeMenuWithTitle_fromItems_(title, items):
    '''
    Make a menu from a sequence of ``items''.  Each item should be a pair
    ``(label, value)'' where value is either the represented object or a list.
    If a list, then it is treated as a sub-menu, and the list must contain more
    label, value pairs.

    Requirement: values must be hashable.
    '''
    menu = NSMenu.alloc().initWithTitle_(title)
    for label, value in items:
        if label is None:
            menuItem = NSMenuItem.separatorItem()
        elif isinstance(value, list):
            menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(label, None, u'')
            submenu = CBMakeMenuWithTitle_fromItems_(label, value)
            menuItem.setSubmenu_(submenu)
        else:
            menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(label, None, u'')
            menuItem.setRepresentedObject_(value)
            menuItem.setTag_(hash(value))

        menu.addItem_(menuItem)

    return menu