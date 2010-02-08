# Misc debugging utility functions
# Copyright (C) 2003-2009 James R. Eagan <eaganjr@acm.org>

from __future__ import with_statement

from AppKit import *
from Foundation import *
import objc

from contextlib import contextmanager
import inspect
import os
import sys

import jre.debug
import jre.geom as geom

from functools import wraps


def cocoa_threadsafe(func):
    try:
        num_args = func.func_code.co_argcount
        # print 'Made', func, 'threadsafe with', num_args, 'args'
        return cocoa_threadsafe_map[num_args](func)
    except:
        print >> sys.stderr, "Warning: Could not make", func, "cocoa threadsafe"
        jre.debug.printStackTrace()
        return func
threadsafe = cocoa_threadsafe

def cocoa_threadsafe_func(func):
    @wraps(func)
    def poolwrapper_func():
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func()
        finally:
            del pool
    
    return poolwrapper_func
    
def cocoa_threadsafe0(func):
    @wraps(func)
    def poolwrapper0(self):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self)
        finally:
            del pool
    
    return poolwrapper0

def cocoa_threadsafe1(func):
    @wraps(func)
    def poolwrapperone_(self, arg):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self, arg)
        finally:
            del pool
    
    return poolwrapperone_

def cocoa_threadsafe2(func):
    @wraps(func)
    def poolwrapperone_two_(self, arg1, arg2):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self, arg1, arg2)
        finally:
            del pool
    
    return poolwrapperone_two_

def cocoa_threadsafe3(func):
    @wraps(func)
    def poolwrapperone_two_three_(self, arg1, arg2, arg3):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self, arg1, arg2, arg3)
        finally:
            del pool
    
    return poolwrapperone_two_three_

def cocoa_threadsafe4(func):
    @wraps(func)
    def poolwrapperone_two_three_four_(self, arg1, arg2, arg3, arg4):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self, arg1, arg2, arg3, arg4)
        finally:
            del pool
    
    return poolwrapperone_two_three_four_

def cocoa_threadsafe5(func):
    @wraps(func)
    def poolwrapperone_two_three_four_five_(self, arg1, arg2, arg3, arg4, arg5):
        pool = NSAutoreleasePool.alloc().init()
        try:
            return func(self, arg1, arg2, arg3, arg4, arg5)
        finally:
            del pool
    
    return poolwrapperone_two_three_four_five_

cocoa_threadsafe_map = { 0: cocoa_threadsafe_func,
                         1: cocoa_threadsafe0,
                         2: cocoa_threadsafe1,
                         3: cocoa_threadsafe2,
                         4: cocoa_threadsafe3,
                         5: cocoa_threadsafe4,
                         6: cocoa_threadsafe5,
                       }

def observable(key):
    def decorator(method):
        @wraps(method)
        def observable_wrapper(self, *args, **kwargs):
            self.willChangeValueForKey_(key)
            return method(self, *args, **kwargs)
            self.didChangeValueForKey_(key)
        return observable_wrapper
    return decorator

__imageTypes = dict(jpg=NSJPEGFileType, jpeg=NSJPEGFileType,
                    gif=NSGIFFileType,
                    png=NSPNGFileType,
                    tif=NSTIFFFileType, tiff=NSTIFFFileType,
                    pdf=None)
                    
def writeImage(image, fileName):
    #image = NSImage.alloc().initWithContentsOfFile_(u'/Users/eaganj/Pictures/Demo Pictures/2629228316_8e1752b2eb_o.jpg')
    #rep = NSBitmapImageRep.representationOfImageRepsInArray_usingType_properties_(image.representations(), NSJPEGFileType, dict(NSImageCompressionFactor=3.0))
    #rep.writeToFile_atomically_(u"/Users/eaganj/Pictures/Demo Pictures/.thumbs/2629228316_8e1752b2eb_o.jpg", True)
    
    suffix = os.path.splitext(fileName)[1][1:]
    fileType = __imageTypes[suffix]
    
    if suffix == u'pdf':
        data = getPDFRepresentationForImage(image)
    else:
        rep = NSBitmapImageRep.imageRepWithData_(image.TIFFRepresentation())
        data = rep.representationUsingType_properties_(fileType, {NSImageCompressionFactor: 3.0})
    data.writeToFile_atomically_(fileName, True)
    #rep = NSBitmapImageRep.representationOfImageRepsInArray_usingType_properties_(imageReps, fileType, {NSImageCompressionFactor: 3.0})
    #rep.writeToFile_atomically_(fileName, True)

def getPDFRepresentationForImage(image):
    view = NSImageView.alloc().initWithFrame_(NSMakeRect(0, 0, *image.size()))
    view.setImage_(image)
    view.display()
    return view.dataWithPDFInsideRect_(NSMakeRect(0, 0, *image.size()))

def oldWriteImage(img, fileName):
    format = os.path.splitext(fileName)[1][1:]
    rep = img.representations()[0]
    try:
        if format in ('jpg', 'jpeg'):
            props = {NSImageCompressionFactor: 3.0}
            data = str(rep.representationUsingType_properties_(NSJPEGFileType, props))
        elif format == 'png':
            data = str(rep.representationUsingType_properties_(NSPNGFileType, {}))
        elif format in ('tiff', 'tif'):
            data = str(img.TIFFRepresentationUsingCompression_factor_(NSTIFFCompressionLZW, 6.0))
    except AttributeError:
        format = 'tiff'
        fileName = os.path.splitext(fileName)[0] + '.tiff'
        data = str(img.TIFFRepresentationUsingCompression_factor_(NSTIFFCompressionLZW, 6.0))

    with open(fileName, 'w') as f:
        f.write(data)
        f.close()

def makeImageThumbnail(image, width=200, height=200):
    size = geom.scaleRectToFitInRect(NSMakeRect(0, 0, *image.size()),
                                     NSMakeRect(0, 0, width, height))[1]
    thumb = NSImage.alloc().initWithSize_(size)
    try:
        thumb.lockFocus()
        image.drawInRect_fromRect_operation_fraction_(NSMakeRect(0, 0, *thumb.size()),
                                                      NSMakeRect(0, 0, *image.size()), 
                                                      NSCompositeSourceOver, 
                                                      1.0)
    finally:
        thumb.unlockFocus()
    
    return thumb


# def swizzle(cls, oldMethod, newMethod):
#     newSEL = objc.selector(oldMethod, selector=oldMethod.selector, signature=oldMethod.signature)
#     objc.classAddMethod(cls, newMethod, newSEL)

# Replacement wrapper lambdas depending on the number of parameters required.  Support up to 8
# parameters, including self.  This is necessary to suppress a PyObjC DeprecationWarning about
# Not all Objective-C arguments being present in the Python argument list (collapsed as *args).
__swizzleIMPMap = {0: lambda f: lambda: f(),
                   1: lambda f: lambda self: f(self),
                   2: lambda f: lambda self, a: f(self, a),
                   3: lambda f: lambda self, a, b: f(self, a, b),
                   4: lambda f: lambda self, a, b, c: f(self, a, b, c),
                   5: lambda f: lambda self, a, b, c, d: f(self, a, b, c, d),
                   6: lambda f: lambda self, a, b, c, d, e: f(self, a, b, c, d, e),
                   7: lambda f: lambda self, a, b, c, d, e, g: f(self, a, b, c, d, e, g),
                   8: lambda f: lambda self, a, b, c, d, e, g, h: f(self, a, b, c, d, e, g, h),
                  }
                  
def swizzleMethod(old):
    def swizzleWithNewMethod_(f):
        cls = old.definingClass
        oldSelectorName = old.__name__.replace("_", ":")
        oldIMP = cls.instanceMethodForSelector_(oldSelectorName)
        newSelectorName = f.__name__.replace("_", ":")
        
        argc = len(inspect.getargspec(f)[0])
        newSEL = objc.selector(f, selector=newSelectorName, signature=old.signature)
        #oldSEL = objc.selector(lambda self, *args: oldIMP(self, *args), selector=newSelectorName, signature=old.signature)
        oldSEL = objc.selector(__swizzleIMPMap[argc](oldIMP), selector=newSelectorName, signature=old.signature)
    
        # Swap the two methods
        objc.classAddMethod(cls, newSelectorName, oldSEL)
        objc.classAddMethod(cls, oldSelectorName, newSEL)
        #NSLog(u"Swizzled %s.%s <-> %s" % (cls.__name__, oldSelectorName, newSelectorName))
        
        return f
    
    return swizzleWithNewMethod_

# Add context manager methods to NSAutoreleasePool as a category hack
class NSAutoreleasePool(objc.Category(NSAutoreleasePool)):
    def __enter__(self):
            return self
    def __exit__(self, ext, exv, extb):
            del self
            return False

@contextmanager
def PoolManager(pool):
    yield
    del pool


class NSView(objc.Category(NSView)):
    def convertRectToWindow_(self, rect):
        superview = self.superview()
        return superview.convertRectToBase_(rect) if superview else self.convertRectToBase_(rect)

### Include submodules
import image
import prefs
import util
from _bundleUserDefaults import *
from _singleton import *
