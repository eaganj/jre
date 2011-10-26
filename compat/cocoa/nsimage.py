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

__all__ = ()

try:
    from AppKit import *
    from Foundation import *
    import objc

    if 'CGImageForProposedRect_context_hints_' not in NSImage.__dict__:
        class NSImage(objc.Category(NSImage)):
            def CGImageForProposedRect_context_hints_(self, rect, context, hints):
                import Quartz
            
                imageSize = self.size()
            
                bitmapContext = Quartz.CGBitmapContextCreate(None, imageSize.width, imageSize.height, 8, 0, NSColorSpace.genericRGBColorSpace().CGColorSpace(), Quartz.kCGBitmapByteOrder32Host|Quartz.kCGImageAlphaPremultipliedFirst)
            
                # Don't use a context manager here since that's not available in Leopard's PyObjC
                NSGraphicsContext.saveGraphicsState()
                try:
                    NSGraphicsContext.setCurrentContext_(
                        NSGraphicsContext.graphicsContextWithGraphicsPort_flipped_(bitmapContext, False))
                    self.drawInRect_fromRect_operation_fraction_(NSMakeRect(0, 0, 
                                                                    imageSize.width, imageSize.height),
                                                                 NSZeroRect,
                                                                 NSCompositeCopy,
                                                                 1.0)
                finally:
                    NSGraphicsContext.restoreGraphicsState()
                                                             
                cgImage = Quartz.CGBitmapContextCreateImage(bitmapContext)
                return cgImage
except ImportError:
    pass