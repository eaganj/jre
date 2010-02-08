# Misc geometry utility functions
# Copyright (C) 2004 James R. Eagan <eaganjr@acm.org>
#
# Created: 040608


import math
from compat import namedtuple

Point = namedtuple('Point', 'x y')
Size = namedtuple('Size', 'width height')
Rect = namedtuple('Rect', 'origin size')
MakeRect = lambda x, y, w, h: Rect(Point(x, y), Size(w, h))

def distSq(a, b):
    '''
    Compute the square of the distance between two points, `a` and `b`.
    '''

    ax, ay = a
    bx, by = b
    return (bx - ax)*(bx - ax) + (by - ay)*(by - ay)

def dist(a, b):
    '''
    Compute the distance between two points, `a`, and `b`.
    '''
    return math.sqrt(distSq(a, b))

def delta(a, b):
    '''
    Compute the x, y distance between two points (i.e. the dx, dy offsets).
    '''
    ax, ay = a
    bx, by = b
    return Point(bx - ax, by - ay)

def distPointLineSq(p, a, b):
    '''
    Compute the square of the distance between a point and a line.

    If the square of the distance is sufficient (e.g.
    in comparing the relative distances of different points) then this
    function can be used instead of `distPointLine` for efficiency.

    Source: Graphics Gems II, edited by James Arvo (1991 Printing).
    Translated to Python by James R. Eagan <eaganj@cc.gatech.edu>.
    '''
    px, py = p
    ax, ay = a
    bx, by = b

    a2 = (py - ay)*(bx - ax) - (px - ax)*(by - ay)
    return (a2*a2)/((bx - ax)*(bx - ax) + (by - ay)*(by - ay))

def distPointLineApprox(p, a, b):
    '''
    Compute the approximate distance between a point and a line.

    This distance function computes the approximate distance between
    a point and a line to save on a square-root computation.  Use this
    distance function if approximate values are acceptible.

    Source: Graphics Gems II, edited by James Arvo (1991 Printing).
    Translated to Python by James R. Eagan <eaganj@cc.gatech.edu>.
    '''
    px, py = p
    ax, ay = a
    bx, by = b

    a2 = (py - ay)*(bx - ax) - (px - ax)*(by - ay)
    return math.abs(a2) / (math.abs(bx - ax) + math.abs(by - ay)
                           - min(math.abs(bx - ax), math.abs(by - ay)) / 2)

def distPointLine(p, a, b):
    '''
    Compute the distance between a point and a line.
    '''

    return math.sqrt(distPointLineSq(p, a, b))

def distPointLineSeg(p, a, b, distFunc=dist, distPointLineFunc=distPointLine):
    '''
    Compute the distance between a point and a line segment.

    The default distance functions used here compute the actual
    distance between points.  This calculation involves an expensive
    square-root operation.  If the square of the distance is sufficient (e.g.
    in comparing the relative distances of different points) then the function
    `distSq` can be passed in as the `distFunc` parameter and 
    `distPointLineSq` as the `distPointLineFunc` parameter.

    Source: Graphics Gems II, edited by James Arvo (1991 Printing).
    Translated to Python by James R. Eagan <eaganj@cc.gatech.edu>.
    '''
    px, py = p
    ax, ay = a
    bx, by = b

    t = (px - ax)*(bx - ax) + (py - ay)*(by - ay) # dot product
    if t < 0:
        return distFunc(a, p)
    else:
        t = (bx - px)*(bx - ax) + (by - py)*(by - ay)
        if t < 0:
            return distFunc(b, p)
        else:
                return distPointLineFunc(p, a, b)
                
def centerRectInRect(inner, outer):
    ((ix, iy), (iw, ih)) = inner
    ((ox, oy), (ow, oh)) = outer

    #return (((ox + (ow - iw) / 2), (oy + (oh - ih) / 2)), (iw, ih))
    return MakeRect(ox + (ow -iw) / 2, oy + (oh - ih) / 2, iw, ih)

def isPointInRect(point, rect):
    rx1, ry1 = rect[0]
    rx2, ry2 = rect[1]
    rx2, ry2 = rx1 + rx2, ry1 + ry2 # convert from w, h to bounds
    x, y = point

    return rx1 <= x <= rx2 and ry1 <= y <= ry2

def scaleRectDownToFitInRect(src, dst):
    '''
    Find the scaled rectangle of src that just fits within dst.
    Scales down, but not up.
    
    ``scaleRectDownToFitInRect(rect, rect) -> rect''
    '''
    sw, sh = src[1]
    dw, dh = dst[1]
    scale = min(dw / float(sw), dh / float(sh), 1.0) # Scale down, but not up.
    w, h = scale * sw, scale * sh
    x, y = dst[0]
    return centerRectInRect(((x, y), (w, h)), dst)

def scaleRectToFitInRect(src, dst):
    '''
    Find the scaled rectangle of src that just fits within dst.
    
    ``scaleRectToFitInRect(rect, rect) -> rect''
    '''
    sw, sh = src[1]
    dw, dh = dst[1]
    scale = min(dw / float(sw), dh / float(sh))
    w, h = scale * sw, scale * sh
    x, y = dst[0]
    return centerRectInRect(((x, y), (w, h)), dst)

def cropRectToFitInRect(src, dst):
    '''
    Find the cropping rectangle of src to fit in dst.
    
    ``cropRectToFitInRect(rect, rect) -> rect''
    '''
    sw, sh = src[1]
    dw, dh = dst[1]
    w, h = min(sw, dw), min(sh, dh)
    # return ((src[0][0], src[0][1]), (w, h))
    return MakeRect(src[0][0], src[0][1], w, h)


#### FIXME: !!!
try:
    from Foundation import NSIntersectsRect
except ImportError:
    print "Warning: rectIntersectsRect not implemented in jre.geom"
def rectIntersectsRect(r1, r2):
    '''
    Find if two rectangles intersect.
    '''
    return NSIntersectsRect(r1, r2)
    # TODO: (code below from GNUstep)
    # NSIntersectsRect(NSRect aRect, NSRect bRect)
    # {
    #   /* Note that intersecting at a line or a point doesn't count */
    #   return (NSMaxX(aRect) <= NSMinX(bRect)
    #           || NSMaxX(bRect) <= NSMinX(aRect)
    #               || NSMaxY(aRect) <= NSMinY(bRect)
    #               || NSMaxY(bRect) <= NSMinY(aRect)) ? NO : YES;

### TODO: Implement rectIntersectionWithRect:
# Code below from GNUstep
# NSIntersectionRect (NSRect aRect, NSRect bRect)
# {
#   if (NSMaxX(aRect) <= NSMinX(bRect) || NSMaxX(bRect) <= NSMinX(aRect)
#     || NSMaxY(aRect) <= NSMinY(bRect) || NSMaxY(bRect) <= NSMinY(aRect)) 
#     {
#       return NSMakeRect(0.0, 0.0, 0.0, 0.0);
#     }
#   else
#     {
#       NSRect    rect;
# 
#       if (NSMinX(aRect) <= NSMinX(bRect))
#         rect.origin.x = bRect.origin.x;
#       else
#         rect.origin.x = aRect.origin.x;
# 
#       if (NSMinY(aRect) <= NSMinY(bRect))
#         rect.origin.y = bRect.origin.y;
#       else
#         rect.origin.y = aRect.origin.y;
# 
#       if (NSMaxX(aRect) >= NSMaxX(bRect))
#         rect.size.width = NSMaxX(bRect) - rect.origin.x;
#       else
#         rect.size.width = NSMaxX(aRect) - rect.origin.x;
# 
#       if (NSMaxY(aRect) >= NSMaxY(bRect))
#         rect.size.height = NSMaxY(bRect) - rect.origin.y;
#       else
#         rect.size.height = NSMaxY(aRect) - rect.origin.y;
# 
#       return rect;
#     }
# }

def rectIntersectsRectWithRotation(normal, rotated, degrees):
    '''
    Find if an unrotated rectangle intersects a rotated rectangle.  Rotation is expressed in degrees.
    
    Code translated from Clemens Klokmose.  Bugs introduced by me.
    '''
    (nx, ny), (nw, nh) = normal
    (rx, ry), (rw, rh) = rotated
    
    pivot = (rx + rw/2, ry + rh/2)
    blx,bly = rotatePointAroundPoint((rx, ry), pivot, degrees)
    tlx,tly = rotatePointAroundPoint((rx, ry+rh), pivot, degrees)
    trx,tr_y = rotatePointAroundPoint((rx+rw, ry+rh), pivot, degrees)
    brx,bry = rotatePointAroundPoint((rx+rw, ry), pivot, degrees)
    
    x = min(blx, tlx, trx, brx)
    y = min(bly, tly, tr_y, bry)
    w = max(blx, tlx, trx, brx) - x
    h = max(bly, tly, tr_y, bry) - y
    
    newRect = (x, y), (w, h)
    return rectIntersectsRect(normal, newRect)

def rotatePointAroundPoint(point, pivot, degrees):
    '''
    Calculate the position of a point rotated around a pivot by a number of degrees.
    
    Code translated from Clemens Klokmose.  Bugs introduced by me.
    '''
    rad = math.radians(degrees)
    x, y = point
    px, py = pivot
    dx, dy = delta(pivot, point)
    return Point((math.cos(rad) * dx - math.sin(rad) * dy) + px, 
                 (math.sin(rad) * dx + math.cos(rad) * dy) + py)

def rotateRectAroundPoint(rect, pivot, degrees):
    '''
    Calculate the rect resulting from rotating by a number of degrees around a pivot.
    '''
    origin, size = rect
    rotatedOrigin = rotatePointAroundPoint(origin, pivot, degrees)
    return Rect(rotatedOrigin, size)
