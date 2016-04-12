#!/usr/bin/env python
#a Imports
from PIL import Image
from gjslib.math.vectors import *

#a Classes
#a Globals
epsilon=1E-9

#a Point class
#c point
class point(object):
    """
    A simple point class of arbitrary dimensions.
    In effect this is just an object that stores a vector as a tuple
    It is useful for subclassing
    """
    #f __init__
    def __init__(self, coords=None):
        if coords is not None:
            self.set(coords)
            pass
        pass
    #f __len__
    def __len__(self):
        return len(self.coords)
    #f __iter__
    def __iter__(self):
        return self.coords.__iter__()
    #f __getitem__
    def __getitem__(self,key):
        return self.coords[key]
    #f __setitem__
    def __setitem__(self,key,value):
        c = list(self.coords)
        c[key] = value
        self.coords=tuple(c)
    #f get
    def get(self, scale=None, offset=None):
        """
        Return coordinates scaled by scale then translated by offset
        """
        if scale is None and offset is None:
            return self.coords
        if scale is None: scale=(1.0,)
        if offset is None: offset=(0.0,)
        if type(scale)!=tuple: scale=[scale]
        if type(offset)!=tuple: offset=[offset]
        cs = []
        i = 0
        ls = len(scale)
        lo = len(offset)
        for c in self.coords:
            cs.append(c*scale[i%ls]+offset[i%lo])  
            i += 1
            pass
        return cs
    #f set
    def set(self, coords):
        """
        Set the coordinates of a point
        """
        cs = []
        for c in coords:
            cs.append(c+0.0)
            pass
        self.coords = tuple(cs)
        pass
    #f perturb
    def perturb(self, quantum):
        """
        Perturb a point slightly in first 2 dimensions
        """
        cs = []
        for c in self.coords:
            cs.append(c)
            pass
        cs[0] += quantum+cs[1]*quantum
        cs[1] += quantum-cs[0]*quantum
        self.coords = tuple(cs)
        pass
    #f is_parallel_to
    def is_parallel_to(self, other, epsilon=epsilon):
        return abs(vectors.dot_product(self.coords, other.coords))<epsilon
    #f scale
    def scale(self, scale):
        c = vectors.vector_scale(self.coords,scale)
        die
        return c_point( c )
    #f add
    def add(self, other, scale=1):
        c = vectors.vector_add(self.coords, other.coords, scale=scale)
        die
        return c_point(c)
    #f __repr__
    def __repr__( self ):
        result = "("
        for c in self.coords:
            result += "%6.4f "%c
        result += ")"
        return result

#c line
class line(object):
    """
    A simple line class of 2 dimensions for drawing in a draw buffer

    This should be a separate class or a mixin for a basic line class
    The line is stored with its first end at lowest Y, lowest X if horizontal

    Maybe this should be a line segment?
    """
    #f __init__
    def __init__(self,x0,y0,x1,y1,resolution_bits=None):
        if y1<y0: (x0,y0,x1,y1) = (x1,y1,x0,y0)
        if y1==y0 and x1<x0: (x0,y0,x1,y1) = (x1,y1,x0,y0)
        self.p0 = (x0,y0)
        self.p1 = (x1,y1)
        self.dx = x1-x0
        self.dy = y1-y0
        self.res = resolution_bits
        self.is_steep = (self.dy>abs(self.dx))
        self.is_degenerate = (self.dy==0) and (self.dx==0)
        pass
    #f __getitem__
    def __getitem__(self,key):
        return (self.p0,self.p1)[key]
    #f __setitem__
    def __setitem__(self,key,value):
        die
        pass
    #f floor
    def floor(self,v):
        if self.res is None:
            return math.floor(v)
        return (v>>self.res)<<self.res
    #f __iter__
    def __iter__(self):
        self.x = self.floor(self.p0[0])
        self.y = self.floor(self.p0[1])

        self.xplus = 1
        self.yplus = 1
        self.xerr = self.dy
        self.yerr = abs(self.dx)
        if self.res is not None:
            self.xplus = 1<<self.res
            self.yplus = 1<<self.res
            self.xerr = self.xerr<<self.res
            self.yerr = self.yerr<<self.res
            pass
        if self.is_degenerate: self.xplus = 100
        if self.dx<=0: self.xplus=-self.xplus

        # The error term is held at a fixed-point resolution of self.res+1
        # This means that self.xerr, self.yerr are for _half_ a pixel of dx, dy
        error  = ((self.x-self.p0[0]) * self.xerr)
        error -= ((self.y-self.p0[1]) * self.yerr)
        if self.res is None:
            error=error*2
        elif self.res==0:
            error=error<<1
            pass
        else:
            error=error>>(self.res-1)
            pass
        self.error = error

        return self
    #f next
    def next(self):
        if self.is_steep: return self.next_steep()
        return self.next_shallow()
    #f next_shallow
    def next_shallow(self):
        if self.dx>0:
            if self.x>self.p1[0]:
                raise StopIteration()
            pass
        else:
            if self.x<self.p1[0]:
                raise StopIteration()
            pass
        r = self.x,self.y
        self.x += self.xplus
        self.error += self.xerr*2
        if self.error-self.yerr>0:
            self.error-=self.yerr*2
            self.y+=self.yplus
            pass
        return r
    #f next_steep
    def next_steep(self):
        if self.y>self.p1[1]:
            raise StopIteration()
        r = self.x,self.y
        self.y += self.yplus
        self.error -= self.yerr*2
        if self.error+self.xerr<0:
            self.error += self.xerr*2
            self.x     += self.xplus
            pass
        return r
    #f All done
    pass

#c path
class path(object):
    """
    A path is a set of lists of lines with attributes such as line width, type, ends, joins, and so on
    It may be stroked or filled
    If a path is to be filled then it needs to be closed
    A path to be stroked can be open
    When a path is stroked, if it has non-zero width it converts into a further set of closed paths
    that describe the drawing.
    The lines can be bezier_line or simple straight lines.
    """
    def __init__(self):
        pass
    def copy(self):
        """
        Copy appropriately
        """
        return
    def stroke(self, **kwargs):
        """
        
        """
        pass
    pass

#c _line
class _line(object):
    """
    """
    #f __init__
    def __init__(self,l):
        self.tl = (l[0],l[1])
        self.br = (l[2],l[3])
        if ((l[1] > l[3]) or
            ((l[1]==l[3]) and (l[0]>l[2]))):
            self.tl = (l[2],l[3])
            self.br = (l[0],l[1])
            pass
        self.dx = l[2]-l[0]
        self.dy = l[3]-l[1]
        pass
    #f x_at_y
    def x_at_y(self, y):
        if self.dy==0: return 0
        #print y, y-self.tl[1], ((y-self.tl[1]) * self.dx) / self.dy
        return ((y-self.tl[1]) * self.dx) / self.dy + self.tl[0]
    #f __repr__
    def __repr__(self):
        r = "( (%d,%d), (%d,%d) )"%(self.tl[0],self.tl[1], self.br[0],self.br[1])
        return r
    pass

#c draw_buffer
class draw_buffer(object):
    #f __init__
    def __init__(self, mode="RGB", size=(10,10), color=None, filename=None, image=None):
        self.image = image
        if image is None:
            if filename is not None:
                self.image = Image.open(png_filename)
                self.size = self.image.size
                self.mode = self.image.mode
                pass
            else:
                self.image = Image.new(mode,size,color)
                self.size = size
                self.mode = mode
                pass
            pass
        pass
    #f get_image
    def get_image(self):
        return self.image
    #f save
    def save(self, filename, format=None):
        return self.image.save(filename)
    #f getpixel - get pixel value at (x,y)
    def getpixel(self,x,y):
        if (x<0) or (y<0) or (x>=self.size[0]) or (y>=self.size[1]): return 0
        return self.image.getpixel((x,y))
    #f putpixel - set pixel value at (x,y)
    def putpixel(self,x,y,value=255):
        if (x<0) or (y<0) or (x>=self.size[0]) or (y>=self.size[1]): return
        self.image.putpixel((int(x),int(y)), value)
        return
    #f draw_line - draw zero-width line
    def draw_line(self,l,value=255):
        for (px,py) in l:
            self.putpixel(px,py,value)
            pass
        pass
    #f fill_paths
    def fill_paths(self, paths, resolution_bits=16, value=255, winding_rule=0):
        """
        paths is a set of lists of points
        Each path is implicitly closed

        The algorithm is to generate a set of lines from the paths
        Sort the lines so lowest top-left y is first; this is the 'ready list'
        Start with an empty 'active lines' set
        For each y pixel line (can start at y=pixel line of first in ready list)
        1. determine if the first of the ready list should be activated; if so, activate
        and move on to the next in the ready list
        2. for all the lines in the active set determine if the line:
        2a. is now inactive (i.e. pixel y >= bottom y), in which case deactivate
        2b. crosses at pixel y - and return its X coordinate
        Note that horizontal lines on a pixel y immediately deactivate
        Now sort the returned X coordinates, and draw rows of pixels according to the winding rule at pixel Y
        Move down a line
        Continue until ready list and active set are all empty
        """
        d = 1<<resolution_bits
        ready_list = []
        for p in paths:
            if len(p)<2: continue
            last_pt = (int(p[-1][0]*d), int(p[-1][1]*d))
            for pt in p:
                pt = (int(pt[0]*d), int(pt[1]*d))
                ready_list.append( _line((pt[0],pt[1],last_pt[0],last_pt[1])) )
                last_pt = pt
                pass
            pass
        if len(ready_list)<1:
            return
        def sort_lines(l0,l1):
            if (l0.tl[1]<=l1.tl[1]): return -1
            return 1
        ready_list.sort(cmp=sort_lines)
        active_set = set()
        py = (ready_list[0].tl[1])>>resolution_bits
        y = py << resolution_bits
        while (len(ready_list)>0) or (len(active_set)>0):
            while len(ready_list)>0:
                if ready_list[0].tl[1] > y:
                    break
                active_set.add(ready_list.pop(0))
                pass
            lines_complete = []
            x_crossings = []
            for l in active_set:
                if y >= l.br[1]:
                    lines_complete.append(l)
                    pass
                else:
                    x_crossings.append(l.x_at_y(y))
                    pass
                pass
            for l in lines_complete:
                active_set.remove(l)
                pass
            x_crossings.sort()
            rpx = None
            for i in range(len(x_crossings)):
                lpx = rpx
                rpx = x_crossings[i] >> resolution_bits
                if (i%2)==1: # odd winding rule
                    for x in range(rpx-lpx):
                        self.putpixel(lpx+x,py,value)
                        pass
                    pass
                pass

            #print py, x_crossings
            py += 1
            y += 1<<resolution_bits
            pass
        pass
    #f string_scale
    def string_scale(self,scale=1):
        w = self.size[0]/scale
        h = self.size[1]/scale
        r = ""
        for y in range(h):
            l = ""
            for x in range(w):
                v = 0
                for i in range(scale):
                    for j in range(scale):
                        v += self.getpixel(x*scale+i,y*scale+j)
                        pass
                    pass
                v = v / (scale*scale)
                if (v>255):v=255
                v = v/64
                l += " -+#"[v]
                pass
            r += l + "\n"
            pass
        return r
    #f __repr__
    def __repr__(self):
        r = ""
        for y in range(self.size[1]):
            l = ""
            for x in range(self.size[0]):
                v = self.getpixel(x,y)
                if (v>128):
                    l+="*"
                    pass
                elif (v>0):
                    l+="."
                    pass
                else:
                    l+=" "
                    pass
                pass
            r += l + "\n"
            pass
        return r
    #f Done
    pass
