#!/usr/bin/env python
#a Imports
from gjslib.graphics import drawing
import unittest

#a Test
#c PointTests
class PointTests(unittest.TestCase):
    def check_point(self,d,value):
        self.assertEqual(len(value),len(d), 'Length of vectors differs')
        for i in range(len(d)):
            self.assertEqual(value[i],d[i], 'Coordinate %d mismatches'%i)
        pass
    def test_single(self):
        p = drawing.point((1,2,3,4))
        return self.check_point(p,(1,2,3,4))
    def test_iter(self):
        p = drawing.point((1,2,3,4))
        r = 0
        for x in p:
            r += x
            pass
        return self.assertEqual(r,10, 'Failed to iterate cleanly')
    def test_get(self):
        p = drawing.point((1,2,3,4))
        r = p[0] + p[1] + p[2] + p[3]
        self.assertEqual(r,10, 'Failed to get indices')
        pass
    def test_set(self):
        p = drawing.point((1,2,3,4))
        r = p[0] + p[1] + p[2] + p[3]
        p[0] = 5
        p[1] = 4
        p[2] = 3
        p[3] = 2
        r += p[0] + p[1] + p[2] + p[3]
        self.assertEqual(r,24, 'Failed to set or get cleanly')
        self.check_point(p,(5,4,3,2))
        pass
    def test_get2(self):
        p = drawing.point((1,2,3,4))
        c = p.get()
        c = list(c)
        c.reverse()
        m = drawing.point(c)
        self.check_point(m,(4,3,2,1))
        pass
    def test_get_offset(self):
        p = drawing.point((1,2,3,4))
        c = p.get(offset=(4,3,2,1))
        m = drawing.point(c)
        self.check_point(m,(5,5,5,5))
        c = p.get(offset=(1,))
        m = drawing.point(c)
        self.check_point(m,(2,3,4,5))
        c = p.get(offset=2)
        m = drawing.point(c)
        self.check_point(m,(3,4,5,6))
        pass
    def test_get_scale(self):
        p = drawing.point((1,2,3,4))
        c = p.get(scale=2)
        m = drawing.point(c)
        self.check_point(m,(2,4,6,8))
        c = p.get(scale=(3,))
        m = drawing.point(c)
        self.check_point(m,(3,6,9,12))
        c = p.get(scale=(2,3,-1,1))
        m = drawing.point(c)
        self.check_point(m,(2,6,-3,4))
        pass
#c LineTests
class line(object):
    def __init__(self,x0,y0,x1,y1,resolution_bits=16):
        if y1<y0: (x0,y0,x1,y1) = (x1,y1,x0,y0)
        if y1==y0 and x1<x0: (x0,y0,x1,y1) = (x1,y1,x0,y0)
        self.p0 = (x0,y0)
        self.p1 = (x1,y1)
        self.dx = x1-x0
        self.dy = y1-y0
        self.res = resolution_bits
        self.is_steep = (self.dy>abs(self.dx))
        pass
    def floor(self,v):
        return (v>>self.res)<<self.res
    def __iter__(self):
        self.x = self.floor(self.p0[0])
        self.y = self.floor(self.p0[1])

        self.xplus = 1<<self.res
        if self.dx<0: self.xplus=-self.xplus

        self.xerr = self.dy<<self.res
        self.yerr = abs(self.dx)<<self.res

        # The error term is held at a fixed-point resolution of self.res+1
        # This means that self.xerr, self.yerr are for _half_ a pixel of dx, dy
        error  = ((self.x-self.p0[0]) * self.xerr)
        error -= ((self.y-self.p0[1]) * self.yerr)
        if self.res==0:
            error=error<<1
            pass
        else:
            error=error>>(self.res-1)
            pass
        self.error = error
        return self
    def next(self):
        if self.is_steep: return self.next_steep()
        return self.next_shallow()
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
        self.error += self.xerr<<1
        if self.error-self.yerr>0:
            self.error-=self.yerr<<1
            self.y+=1<<self.res
            pass
        return r
    def next_steep(self):
        if self.y>self.p1[1]:
            raise StopIteration()
        r = self.x,self.y
        self.y += 1<<self.res
        self.error -= self.yerr<<1
        if self.error+self.xerr<0:
            self.error += self.xerr<<1
            self.x     += self.xplus
            pass
        return r

class LineTests(unittest.TestCase):
    line_pts = {}
    line_pts[0,0,4,4,0] = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    line_pts[0,0,4,2,0] = [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]
    line_pts[0,0,10,1,0] = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)]
    line_pts[10,10,14,14,0] = [(10, 10), (11, 11), (12, 12), (13, 13), (14, 14)]
    line_pts[0,0,4,4,2] = [(0, 0), (4, 4)]
    line_pts[0,0,4,4,1] = [(0, 0), (2,2), (4, 4)]
    line_pts[0,0,4,0,1] = [(0, 0), (2,0), (4, 0)]
    line_pts[1,1,5,1,1] = [(0, 0), (2,0), (4, 0)]
    line_pts[1,1,5,1,0] = [(1, 1), (2,1), (3,1), (4,1), (5, 1)]
    line_pts[5,1,1,1,0] = [(1, 1), (2,1), (3,1), (4,1), (5, 1)]
    line_pts[5,1,1,5,0] = [(5, 1), (4,2), (3,3), (2,4), (1, 5)]
    def check_points(self,d,value):
        self.assertEqual(len(value),len(d), 'Length of vectors differs %s'%(str(d)))
        for i in range(len(d)):
            self.assertEqual(value[i],d[i], 'Coordinate %d mismatches %s'%(i,str(d)))
        pass
    def check_lines(self,line_pts):
        print
        for l in line_pts:
            (x0,y0,x1,y1,r) = l
            ln = line(x0,y0,x1,y1,r)
            lp=[]
            for p in ln:
                lp.append(p)
                pass
            print l, lp, line_pts[l]
            self.check_points(lp,line_pts[l])
            pass
        print
        pass
    def swap_xy_in_lines(self, line_pts):
        k = line_pts.keys()
        res = {}
        for l in k:
            (x0,y0,x1,y1,r) = l
            np = []
            for (x,y) in line_pts[l]:
                np.append((y,x))
                pass
            if np[0][1]>np[-1][1]:
                np.reverse()
            res[y0,x0,y1,x1,r] = np
            pass
        return res
    def test_bresenham_oct_shallow_xp(self):
        self.check_lines(self.line_pts)
        pass
    def test_bresenham_oct_steep_xp(self):
        line_pts = self.swap_xy_in_lines(self.line_pts)
        self.check_lines(line_pts)
        pass
#c DrawBufferTests
class DrawBufferTests(unittest.TestCase):
    def check_buffer(self,d,value):
        dl = d.__repr__().split("\n")
        for i in range(len(dl)):
            self.assertEqual(value[i],dl[i], 'Bad draw buffer data')
        pass
    def test_from_image(self):
        import PIL.Image
        a = PIL.Image.new(mode="RGB",size=(20,20))
        d = drawing.draw_buffer(image=a)
        self.assertEqual(a,d.get_image(),'Images do not match')
        pass
    def test_tiny_dot(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.putpixel(1,1)
        return self.check_buffer(d,['    ', ' *  ', '    ', '    ', ''])
    def test_tiny_horiz(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,4,0), value=64 )
        d.draw_line( (0,1,4,1), value=255 )
        d.draw_line( (0,2,4,2), value=128 )
        d.draw_line( (0,3,4,3), value=192 )
        return self.check_buffer(d,['....', '****', '....', '****', ''])
    def test_tiny_vert(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,0,4), value=64 )
        d.draw_line( (1,0,1,4), value=255 )
        d.draw_line( (2,0,2,4), value=128 )
        d.draw_line( (3,0,3,4), value=192 )
        return self.check_buffer(d,['.*.*', '.*.*', '.*.*', '.*.*', ''])
    def test_tiny_diag_dr(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (0,0,4,4), value=64 )
        d.draw_line( (1,0,5,4), value=255 )
        d.draw_line( (2,0,6,4), value=128 )
        d.draw_line( (3,0,7,4), value=192 )
        return self.check_buffer(d,['.*.*', '.*.*', ' .*.', '  .*', ''])
    def test_tiny_diag_dl(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.draw_line( (4,0,0,4), value=64 )
        d.draw_line( (3,0,0,3), value=255 )
        d.draw_line( (2,0,0,2), value=128 )
        d.draw_line( (1,0,0,1), value=192 )
        return self.check_buffer(d,[' *.*', '**.*', '..*.', '**. ', ''])
    def test_tiny_diag_fill_center(self):
        d = drawing.draw_buffer(mode="1",size=(4,4))
        d.fill_paths( [((0.9,0.9), (0.9,2.1), (2.1,2.1), (2.1,0.9),),
                   ],value=255 )
        return self.check_buffer(d,['    ', '**  ', '**  ', '    ', ''])
    def test_tiny_diag_fill_rings(self):
        d = drawing.draw_buffer(mode="1",size=(8,8))
        p = []
        for i in [1,2,3,4]:
            p.append( ( (i-0.1, i-0.1), (i-0.1, 8.1-i), (8.1-i, 8.1-i), (8.1-i, i-0.1)) )
            pass
        d.fill_paths( p, value=64 )
        return self.check_buffer(d,['        ', '....... ', '.     . ', '. ... . ', '. . . . ', '. ... . ', '.     . ', '....... ', ''])

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(DrawBufferTests),
           loader(PointTests),
           ]

if __name__ == '__main__':
    unittest.main()
