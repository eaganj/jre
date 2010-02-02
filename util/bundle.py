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