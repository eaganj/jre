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