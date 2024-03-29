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

try:
    from Quartz import CAShapeLayer
    from Quartz import *
    from Quartz.QuartzCore import *
    
    __all__ = ('CAShapeLayer',)
except ImportError:
    kCAFillRuleNonZero = u'non-zero'
    kCAFillRuleEvenOdd = u'even-odd'
    kCALineJoinMiter = 'miter'
    kCALineJoinRound = 'round'
    kCALineJoinBevel = 'bevel'
    kCALineCapButt = 'butt'
    kCALineCapRound = 'round'
    kCALineCapSquare = 'square'
    
    class CAShapeLayer(CALayer):
        __CGConstantForCAConstant = { kCALineJoinBevel: 2,
                                      kCALineJoinMiter: 0,
                                      kCALineJoinRound: 1,
                                      kCALineCapSquare: 2,
                                      kCALineCapRound: 1,
                                      kCALineCapButt: 0,
                                      kCAFillRuleEvenOdd: 1,
                                      kCAFillRuleNonZero: 0,
                                    }
        
        def init(self):
            self = super(CAShapeLayer, self).init()
            if not self:
                return self
            
            self._path = None
            self._fillColor = NSColor.blackColor().quartzColor()
            self._fillRule = kCAFillRuleNonZero
            self._lineCap = kCALineCapButt
            self._lineDashPattern = None
            self._lineDashPhase = 0.0
            self._lineJoin = kCALineJoinMiter
            self._lineWidth = 1.0
            self._miterLimit = 10.0
            self._strokeColor = None
            
            # self.setNeedsDisplayOnBoundsChange_(True)
            
            return self
        
        def path(self):
            return self._path
        def setPath_(self, path):
            self._path = path
            self.setNeedsDisplay()
        
        def fillColor(self):
            return self._fillColor
        def setFillColor_(self, color):
            self._fillColor = color
            self.setNeedsDisplay()
        
        def fillRule(self):
            return self._fillRule
        def setFillRule_(self, rule):
            self._fillRule = rule
            self.setNeedsDisplay()
        
        def lineCap(self):
            return self._lineCap
        def setLineCap_(self, lineCap):
            self._lineCap = lineCap
            self.setNeedsDisplay()
        
        def lineDashPattern(self):
            return self._lineDashPattern
        def setLineDashPattern_(self, pattern):
            self._lineDashPattern = pattern
            self.setNeedsDisplay()
        
        def lineDashPhase(self):
            return self._lineDashPhase
        def setLineDashPhase_(self, phase):
            self._lineDashPhase = phase
            self.setNeedsDisplay()
        
        def lineJoin(self):
            return self._lineJoin
        def setLineJoin_(self, lineJoin):
            self._lineJoin = lineJoin
            self.setNeedsDisplay()
        
        def lineWidth(self):
            return self._lineWidth
        def setLineWidth_(self, width):
            self._lineWidth = width
            self.setNeedsDisplay()
        
        def miterLimit(self):
            return self._miterLimit
        def setMiterLimit_(self, limit):
            self._miterLimit = limit
            self.setNeedsDisplay()
        
        def strokeColor(self):
            return self._strokeColor
        def setStrokeColor_(self, color):
            self._strokeColor = color
            self.setNeedsDisplay()
        
        def _disabled_for_debugging_display(self):
            image = NSImage.alloc().initWithSize_(self.frame().size)
            image.lockFocus()
            try:
                pass
                # nsGraphicsContext = NSGraphicsContext.currentContext()
                # context = nsGraphicsContext.graphicsPort()
                # CGContextBeginPath(context)
                # CGContextAddPath(context, self._path)
                # CGContextSetLineCap(context, self.__CGConstantForCAConstant[self._lineCap])
                # # if self._lineDashPattern:
                # #     CGContextSetLineDash(context, self._lineDashPhase, self._lineDashPattern,
                # #                          len(self._lineDashPattern))
                # CGContextSetLineJoin(context, self.__CGConstantForCAConstant[self._lineJoin])
                # CGContextSetLineWidth(context, self._lineWidth)
                # CGContextSetMiterLimit(context, self._miterLimit)
                # if self._fillColor:
                #     CGContextSetFillColorWithColor(context, self._fillColor)
                # CGContextFillPath(context)
                # 
                # # Now stroke it
                # if self._strokeColor:
                #     CGContextSetStrokeColorWithColor(context, self._strokeColor)
                # 
                # CGContextBeginPath(context)
                # CGContextAddPath(context, self._path)
                # CGContextStrokePath(context)
                
            finally:
                image.unlockFocus()
            
            self.setContents_(image)
            del image
            
        def _disabled_for_debugging_drawInContext_(self, context):
            super(CAShapeLayer, self).drawInContext_(context)
            if not self._path:
                print "No path!"
                return
            
            # self._fillColor = NSColor.blackColor().quartzColor()
            # self._fillRule = kCAFillRuleNonZero
            # self._lineCap = kCALineCapButt
            # self._lineDashPattern = None
            # self._lineDashPhase = 0.0
            # self._lineJoin = kCALineJoinMiter
            # self._lineWidth = 1.0
            # self._miterLimit = 10.0
            # self._strokeColor = None
            # 
            
            CGContextBeginPath(context)
            CGContextAddPath(context, self._path)
            CGContextSetLineCap(context, self.__CGConstantForCAConstant[self._lineCap])
            # if self._lineDashPattern:
            #     CGContextSetLineDash(context, self._lineDashPhase, self._lineDashPattern,
            #                          len(self._lineDashPattern))
            CGContextSetLineJoin(context, self.__CGConstantForCAConstant[self._lineJoin])
            CGContextSetLineWidth(context, self._lineWidth)
            CGContextSetMiterLimit(context, self._miterLimit)
            if self._fillColor:
                CGContextSetFillColorWithColor(context, self._fillColor)
            CGContextFillPath(context)
            
            # Now stroke it
            if self._strokeColor:
                CGContextSetStrokeColorWithColor(context, self._strokeColor)
            
            CGContextBeginPath(context)
            CGContextAddPath(context, self._path)
            CGContextStrokePath(context)

    __all__ = ('CAShapeLayer',
               'kCAFillRuleNonZero',
               'kCAFillRuleEvenOdd',
               'kCALineJoinMiter',
               'kCALineJoinRound',
               'kCALineJoinBevel',
               'kCALineCapButt',
               'kCALineCapRound',
               'kCALineCapSquare',)