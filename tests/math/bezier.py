#!/usr/bin/env python
#a Imports
import math
from gjslib.math.bezier import *
from gjslib.graphics import drawing
import unittest
epsilon = 1E-9

#a Test
#c Simple bezier tests
class SimpleBezierTests(unittest.TestCase):
    def check_scalar(self,d,value):
        self.assertTrue(abs(d-value)<epsilon, 'Scalars differ too much %s,%s'%(str(d),str(value)))
        pass
    def check_bezier(self,d,value):
        self.assertEqual(len(value),len(d), 'Length of beziers differs')
        for i in range(len(d)):
            self.assertTrue(abs(value[i]-d[i])<epsilon, 'Coordinate %d mismatches'%i)
            pass
        pass
    def test_bezier2(self):
        b = bezier_quad(pts=([0],[4],[4]))
        print b
        print b.straight_enough(0.1)
        b0 = bezier_quad(split_parent=b,first_split=True)
        print b0
        print b0.straight_enough(0.1)
        b1 = bezier_quad(split_parent=b,first_split=False)
        print b1
        print b1.straight_enough(0.1)
        print b.break_into_segments(0.1)

        b = bezier_quad(pts=([0,0],[0,100],[50,0]))
        print b
        print b.straight_enough(0.1)
        b0 = bezier_quad(split_parent=b,first_split=True)
        print b0
        print b0.straight_enough(0.1)
        b1 = bezier_quad(split_parent=b,first_split=False)
        print b1
        print b1.straight_enough(0.1)
        print b.break_into_segments(1)

        d = drawing.draw_buffer(mode="1",size=(50,50))
        lines = []
        for bez in b.break_into_segments(1):
            bez.draw_in_lines(lambda x,y:lines.append((x,y)))
            pass
        for l in lines:
            ln = drawing.line(l[0][0],l[0][1],l[1][0],l[1][1])
            d.draw_line(ln,value=255)
            pass
        b.draw_in_dots(lambda pt:d.putpixel(pt[0],pt[1]+4))
        print d
        pass
    pass

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(SimpleBezierTests),
           ]

if __name__ == '__main__':
    unittest.main()
