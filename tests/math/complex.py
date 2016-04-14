#!/usr/bin/env python
#a Imports
import math
from gjslib.math.complex import *
import unittest
epsilon = 1E-6
sqrt2 = math.sqrt(2)
pi = math.pi

#a Test
#c Simple complex number tests
class SimpleComplexTests(unittest.TestCase):
    """
    Methods to test:
    __add_ - in math
    __sub__ - in math
    __mul_ - in math
    __div__ - in math
    copy - in make
    cartesian - in make
    add - in math
    multiply - in math
    reciprocal - in math
    modulus - in math
    conjugate - in math
    to_cartesian
    sqrt - in math
    pow - in math
    to_polar
    polar
    real
    """
    def check_scalar(self,d,value):
        self.assertTrue(abs(d-value)<epsilon, 'Scalars differ too much %s,%s'%(str(d),str(value)))
        pass
    def check_complex(self,q,value):
        (r,i,j,k) = q.get()
        d = (r,i,j,k)
        self.assertEqual(len(value),len(d), 'BUG: Length of quaternion test value is not 4!!')
        for i in range(len(d)):
            self.assertTrue(abs(value[i]-d[i])<epsilon, 'Coordinate %d mismatches (%s)'%(i,str(d)))
            pass
        pass
    def test_make(self):
        for (r,i) in [(1,0),(0,1),(1,1),(2,3),(4,5),(3,-1)]:
            c = complex(cartesian=(r,i))
            self.check_scalar(c.cartesian()[0],r)
            self.check_scalar(c.cartesian()[1],i)
            self.check_scalar(c.polar()[0],math.sqrt(i*i+r*r))
            d = c.copy()
            c += complex(cartesian=(1,1))
            self.check_scalar(d.cartesian()[0],r)
            self.check_scalar(d.cartesian()[1],i)
            self.check_scalar(d.polar()[0],math.sqrt(i*i+r*r))
            self.check_scalar(c.cartesian()[0],r+1)
            self.check_scalar(c.cartesian()[1],i+1)
            pass
        pass
    def test_math(self):
        for (r,i) in [(1,0),(0,1),(1,1),(2,3),(4,5),(3,-1)]:
            c = complex(cartesian=(r,i))
            d = c.conjugate()
            self.check_scalar(c.cartesian()[0],r)
            self.check_scalar(c.cartesian()[1],i)
            self.check_scalar(d.cartesian()[0],r)
            self.check_scalar(d.cartesian()[1],-i)
            e = c*d
            m = c.modulus()
            self.check_scalar(e.cartesian()[0],m*m)
            self.check_scalar(e.cartesian()[1],0)
            ci = c.reciprocal()
            f = ci*c
            self.check_scalar(f.cartesian()[0],1)
            self.check_scalar(f.cartesian()[1],0)
            f = c*c/c
            self.check_scalar(f.cartesian()[0],r)
            self.check_scalar(f.cartesian()[1],i)
            f = (c+c)/2
            self.check_scalar(f.cartesian()[0],r)
            self.check_scalar(f.cartesian()[1],i)
            f = (c+c)/c
            self.check_scalar(f.cartesian()[0],2)
            self.check_scalar(f.cartesian()[1],0)
            f = (c-c)
            self.check_scalar(f.cartesian()[0],0)
            self.check_scalar(f.cartesian()[1],0)
            f = ((c*2)*c-(c*c))/c
            self.check_scalar(f.cartesian()[0],r)
            self.check_scalar(f.cartesian()[1],i)
            f = c.sqrt()
            g = f*f
            self.check_scalar(g.cartesian()[0],c.cartesian()[0])
            self.check_scalar(g.cartesian()[1],c.cartesian()[1])
            self.check_scalar(g.cartesian()[0],r)
            self.check_scalar(g.cartesian()[1],i)
            f = c.pow(0.25)
            g = f*f
            g = g*g
            self.check_scalar(g.cartesian()[0],c.cartesian()[0])
            self.check_scalar(g.cartesian()[1],c.cartesian()[1])
            self.check_scalar(g.cartesian()[0],r)
            self.check_scalar(g.cartesian()[1],i)
            pass
        pass

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(SimpleComplexTests),
           ]

if __name__ == '__main__':
    unittest.main()
