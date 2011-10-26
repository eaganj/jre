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

import os.path
import plistlib # FIXME: Available only in Python 2.6 or later or on Mac

class Bundle(object):
    def __init__(self, path):
        self._path = path
    
    @classmethod
    def bundleWithPath_(cls, path):
        return cls(path)
    
    def bundleIdentifier(self):
        return self.infoDictionary()['CFBundleIdentifier']
    
    def infoDictionary(self):
        plistFile = os.path.join(self._path, u'Contents', u'Info.plist')
        return plistlib.readPlist(plistFile)
    
    def pathForResource_ofType_(self, resource, kind):
        # TODO: add Proper language support
        searchDirs = [ u'',
                       u'French.lproj',
                       u'English.lproj',
                     ]
        searchDirs = [ os.path.join(self._path, u'Contents', u'Resources', d) for d in searchDirs ]
        
        fileName = resource + os.path.extsep + kind if kind else resource
        for searchDir in searchDirs:
            filePath = os.path.join(searchDir, fileName)
            if os.path.exists(filePath):
                return filePath
        
        return None