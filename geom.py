# Misc geometry utility functions
# Copyright (C) 2004 James R. Eagan <eaganjr@acm.org>
#
# Created: 040608


import math

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
    return (bx - ax, by - ay)

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

    return (((ox + (ow - iw) / 2), (oy + (oh - ih) / 2)), (iw, ih))

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
    return ((src[0][0], src[0][1]), (w, h))