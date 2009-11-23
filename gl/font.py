# Font library for PyOpenGL
# Copyright (C) 2004 James R. Eagan <eaganjr@acm.org>
#
# Created: 040602

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import ImageFont as pilFont
from PIL import Image, ImageDraw

import string
import jre.Math

class Font:
    '''
    A Font class for PyOpenGL.  Supports texture-mapped text applied to a
    quad.
    '''

    BL_BOTTOM = 1
    BL_MIDDLE = 2
    BL_TOP = 3

    def __init__(self, name=None, size=12):
        self._tex = None
        self._texName = None
        self._font = None
        self._coords = []

        if name is not None:
            self.load(name)

    def load(self, name, size=12):
        '''
        Load a font.  '.ttf' will be appended to the font name and the
        current directory searched for the font.  On Windows, the Windows
        font directory is also searched.
        '''
        try:
            if name.find('.ttf') == -1: name += '.ttf'
            self._font = pilFont.truetype(name, size)
        except:
            self._font = pilFont.load_default()
        self.makeTex()

    def makeTex(self):
        '''
        Uses the loaded font to create a texture suitable for mapping onto
        an OpenGL polygon.
        '''
        
        #image = Image.open('C:/Documents and Settings/h9320960/Desktop/temp.gif')
        #self._tex = Image.open('C:/temp.bmp')
        #self._texData = self._tex.tostring("raw", "RGBX", 0, -1)
        #self.bindTex()
        chars = string.join([ chr(i) for i in range(32, 127) ], '')
        w,h = self._font.getsize(chars)
        w,h = jre.Math.nextPow(w), jre.Math.nextPow(h)
        self._tex = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        #self._tex = Image.new('L', (w, h))
        draw = ImageDraw.Draw(self._tex)

        px,py = 0, 0
        for c in chars:
            cw,ch = self._font.getsize(c)
            #draw.text((px, py), c, font=self._font, fill=(255, 255, 255))
            draw.text((px, py), c, font=self._font)
            self._coords.append((float(px)/w, 1.0-(py+ch)/h, float(px+cw)/w, float(py)/h, cw, ch))
            px = px+cw

        #self._tex.save('C:/temp2.png')

        self._texData = self._tex.tostring('raw', 'RGBA', 0, -1)
        #self._texData = self._tex.tostring('raw', 'L', 0, -1)
        self.bindTex()

#    def makeTexBak(self):
#        '''
#        Uses the loaded font to create a texture suitable for mapping onto
#        an OpenGL polygon.
#        '''
#        chars = string.join([ chr(i) for i in range(32, 127) ], '')
#        w,h = self._font.getsize(chars)
#        w,h = jre.Math.nextPow(w), jre.Math.nextPow(h)
#        self._tex = Image.new('L', (w, h))
#        draw = ImageDraw.Draw(self._tex)
#
#        px,py = 0, 0
#        for c in chars:
#            cw,ch = self._font.getsize(c)
#            draw.text((px, py), c, font=self._font, fill=255)
#            self._coords.append((px, py, px+cw, py+ch))
#            px = px+cw
#
#        self._texData = self._tex.tostring('raw', 'L')#list(self._tex.getdata())
#        self.bindTex()


    def bindTex(self):
        '''
        Make the necessary OpenGL calls to prepare the loaded texture for use.
        '''
        self._texName = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texName)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
                     self._tex.size[0], self._tex.size[1],
                     0, GL_RGBA, GL_UNSIGNED_BYTE,
                     self._texData)
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE, 
        #             self._tex.size[0], self._tex.size[1],
        #             0, GL_LUMINANCE, GL_UNSIGNED_BYTE,
        #             self._texData)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

#    def bindTexBak(self):
#        '''
#        Make the necessary OpenGL calls to prepare the loaded texture for use.
#        '''
#        self._texName = glGenTextures(1)
#        glBindTexture(GL_TEXTURE_2D, self._texName)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#        print "setup texture with w,h:", self._tex.size[0], self._tex.size[1], "--", len(self._texData), "bytes"
#        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#        glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE_ALPHA, 
#                     self._tex.size[0], self._tex.size[1],
#                     0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE,
#                     self._texData)
#        print "loaded texture data"

    def drawString(self, x, y, text, scale=1, baseline=BL_BOTTOM, pathf=None):
        '''
        Draw text at coords x,y.  All text must be in the ASCII range [32,127].

        `pathf`, if defined, is a function of the form:
            `pathf(x, y, t) -> (x,y)` 
                where `x, y` is the point at which the string is to be drawn
                and `t` (in [0, 1]) is the parameterized location along the
                string to draw a particular character.
        '''

        x0, y0 = x, y
        tw,th = self.getSize(text)

        yoffset = 0.0
        if baseline == self.BL_MIDDLE:
            yoffset -= th/2.0 * scale

        glEnable(GL_TEXTURE_2D)
        glAlphaFunc(GL_GEQUAL, 0.0625)
        glEnable(GL_ALPHA_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        glBegin(GL_QUADS)
        xpos = 0.0
        shift = 1.0 / len(text)
        for ch in text:
            i = ord(ch) - ord(' ')
            # left, bottom, right, top, width, height
            l, t, r, b, w, h = self._coords[i] 
            #w, h = w/640.0*scale, h/480.0*scale
            if pathf is not None:
                x, y = pathf(x0, y0, xpos)
                y += yoffset
            w, h = self.getSize(ch, scale)
            glTexCoord2d(l, b); glVertex3d(x    , y    , 0.0)
            glTexCoord2d(r, b); glVertex3d(x + w, y    , 0.0)
            glTexCoord2d(r, t); glVertex3d(x + w, y + h, 0.0)
            glTexCoord2d(l, t); glVertex3d(x    , y + h, 0.0)

            #print xpos, w, tw
            x += w
            xpos += shift
        glEnd()

        glDisable(GL_TEXTURE_2D)

#        if pathf is not None:
#            print "draw line strip"
#            glBegin(GL_LINE_STRIP)
#            glColor3f(0.0, 1.0, 0.0)
#            for t in [ 0.05*i for i in range(int(1.0/0.05)) ]:
#                x, y = pathf(x0, y0, t)
#                glVertex3f(x, y, 0.0)
#            glEnd()


    def debug(self, x=0.35, y=0.35, scale=0.01):
        glEnable(GL_TEXTURE_2D)

        glAlphaFunc(GL_GEQUAL, 0.0625)
        glEnable(GL_ALPHA_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable(GL_POLYGON_OFFSET_FILL)
        #glPolygonOffset(0.0, -0.1)


        glBegin(GL_QUADS)
        tw,th = self._tex.size[0], self._tex.size[1]
        w,h = tw*scale,th*scale
        glColor3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.177246,0.0); glVertex3f(x, y, 0.0)
        glTexCoord2f(0.177246,1.0); glVertex3f(x, y+h, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glTexCoord2f(0.188964,1.0); glVertex3f(x+0.1,y+h, 0.0)
        glTexCoord2f(0.188964,0.0); glVertex3f(x+0.1,y,0.0)
        
        #glTexCoord2i(0, 0); glVertex3f(x, y, 0.0)
        #glTexCoord2i(0, th); glVertex3f(x, y+h, 0.0)
        #glTexCoord2i(tw,th); glVertex3f(x+w,y+h, 0.0)
        #glTexCoord2i(tw,0); glVertex3f(x+w,y,0.0)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def getSize(self, text, scale=1):
        '''
        Get the size of a string of `text`.
        '''

        w, h = 0, 0
        for ch in text:
            cw, ch = self._coords[ord(ch) - ord(' ')][4:6]
            w += cw
            h = max(h, ch)

        return (w/640.0*scale,h/480.0*scale)
        

def main():
    import sys
    f = Font('arial')
    f._tex.save('C:/Documents and Settings/h9320960/Desktop/temp.gif')
    print "Check ~/temp.png"

if __name__ == '__main__':
    main() # for debugging
