# Cocoa preferences utilities
# Copyright (C) 2003-2009 James R. Eagan <eaganjr@acm.org>

from __future__ import with_statement

from AppKit import *
from Foundation import *
import objc

import os

import jre.geom as geom

__imageTypes = dict(jpg=NSJPEGFileType, jpeg=NSJPEGFileType,
                    gif=NSGIFFileType,
                    png=NSPNGFileType,
                    tif=NSTIFFFileType, tiff=NSTIFFFileType,
                    pdf=None)
                    
def writeImage(image, fileName):
    suffix = os.path.splitext(fileName)[1][1:]
    fileType = __imageTypes[suffix]
    
    # Ugly hack.  This should be more extensible.
    if suffix == u'pdf':
        data = getPDFRepresentationForImage(image)
    else:
        rep = NSBitmapImageRep.imageRepWithData_(image.TIFFRepresentation())
        data = rep.representationUsingType_properties_(fileType, {NSImageCompressionFactor: 3.0})
    data.writeToFile_atomically_(fileName, True)

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

# if 'CGImageForProposedRect_context_hints_' not in NSImage.__dict__:
if True:
    class NSImage(objc.Category(NSImage)):
        def jreCGImageForProposedRect_context_hints_(self, rect, context, hints):
            import Quartz

            imageSize = self.size()

            if not rect or not (rect[0][0] or rect[0][1] or rect[1][0] or rect[1][1]):
                rect = NSMakeRect(0, 0, imageSize.width, imageSize.height)

            # bitmapContext = Quartz.CGBitmapContextCreate(None, imageSize.width, imageSize.height, 8, 0, NSColorSpace.genericRGBColorSpace().CGColorSpace(), Quartz.kCGBitmapByteOrder32Host|Quartz.kCGImageAlphaPremultipliedFirst)
            bitmapContext = Quartz.CGBitmapContextCreate(None, rect[1][0], rect[1][1], 8, 0, NSColorSpace.genericRGBColorSpace().CGColorSpace(), Quartz.kCGBitmapByteOrder32Host|Quartz.kCGImageAlphaPremultipliedFirst)

            NSGraphicsContext.saveGraphicsState()
            try:
                NSGraphicsContext.setCurrentContext_(
                        NSGraphicsContext.graphicsContextWithGraphicsPort_flipped_(bitmapContext, False))
                self.drawInRect_fromRect_operation_fraction_(NSMakeRect(0, 0, rect[1][0], rect[1][1]),
                                                             NSZeroRect,
                                                             NSCompositeCopy,
                                                             1.0)
            finally:
                NSGraphicsContext.restoreGraphicsState()

            cgImage = Quartz.CGBitmapContextCreateImage(bitmapContext)
            return cgImage

if True:
    class NSImageRep(objc.Category(NSImageRep)):
        def jreCGImageForProposedRect_context_hints_(self, rect, bitmapContext, hints):
            import Quartz

            if not rect or not (rect[0][0] or rect[0][1] or rect[1][0] or rect[1][1]):
                rect = NSMakeRect(0, 0, self.pixelsWide(), self.pixelsHigh())

            if bitmapContext is None:
                bitmapContext = Quartz.CGBitmapContextCreate(
                                    None, rect[1][0], rect[1][1], 8, 0,
                                    NSColorSpace.genericRGBColorSpace().CGColorSpace(),
                                    Quartz.kCGBitmapByteOrder32Host|Quartz.kCGImageAlphaPremultipliedFirst)

            NSGraphicsContext.saveGraphicsState()
            try:
                NSGraphicsContext.setCurrentContext_(
                        NSGraphicsContext.graphicsContextWithGraphicsPort_flipped_(bitmapContext, False))
                # self.drawInRect_fromRect_operation_fraction_(NSMakeRect(0, 0, rect[1][0], rect[1][1]),
                #                                              NSZeroRect,
                #                                              NSCompositeCopy,
                #                                              1.0)
                self.drawInRect_(NSMakeRect(0, 0, rect[1][0], rect[1][1]))
            finally:
                NSGraphicsContext.restoreGraphicsState()

            cgImage = Quartz.CGBitmapContextCreateImage(bitmapContext)
            return cgImage