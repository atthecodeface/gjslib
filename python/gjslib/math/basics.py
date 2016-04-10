#!/usr/bin/env python
#a Documentation
r"""
Bezier curve and patch classes
----------------------------------------

Consider the equation

:math:`p(t,A,B) = (1-t)*A + t*B`

This provides for a linear interpolation as t varies from 0 to 1 of
the values A and B. In particular :math:`p(0,A,B)=A`, :math:`p(1,A,B)=B`,
:math:`p(\frac{1}{2},A,B)=\frac{A+B}{2}`

This equation is wonderful for providing, for example, the points on a
straight line between two *vectors* A and B:
:math:`\mathbf{p} (t,\mathbf{A},\mathbf{B}) = (1-t) * \mathbf{A} + t * \mathbf{B}`

Now consider the equation

:math:`q(t,A,B,C) = (1-t)*p(t,A,B) + t*p(t,B,C)`

This is effectively interpolating between a first 'value' between A and
B, and a second 'value' betwen B and C. Here, similar to p,
:math:`Q(0,A,B,C)=A` and :math:`Q(1,A,B,C)=C` - which means that the
interpolation starts at the 'left' (or A) and ends at the 'right' (or
B) as t goes from 0 to 1.

If we expand out the equation for 'p' in 'q', we get:

.. math::
 \begin{align}
 q(t,A,B,C) &= (1-t)*p(t,A,B) + t*p(t,B,C) \\
 &= (1-t)(1-t)A + t(1-t)tB + t(1-t)B + t*t*C \\
 &= (1-t)^2A + 2t(1-t)B + t^2C
 \end{align}
"""
__docformat__ = "restructuredtext"

#a Imports
import math
import vectors

#a Globals
epslion=1E-9

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
            self.set_coords(coords)
            pass
        pass
    #f get
    def get(self, scale=(1.0,), offset=(0.0,)):
        cs = []
        i = 0
        ls = len(scale)
        lo = len(offset)
        for c in self.coords:
            cs.append(c*scale[i%ls]+offset[i%lo])  
            i += 1
            pass
        return cs
    #f length
    def length(self):
        return vectors.length(self.coords)
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
    #f mult_by_matrix
    def mult_by_matrix(self, m):
        """
        """
        c = []
        for i in range(len(self.coords)):
            c.append(0)
            for j in range(len(m[i])):
                c[-1] += m[i][j]*self.coords[j]
                pass
            pass
        die
        return c_point(c)
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
    #f distance
    def distance(self, other):
        return vectors.vector_separation(self.coords, other.coords)
    #f normal_2d
    def normal_2d(self):
        return c_point( coords=(-self.coords[1], self.coords[0]) )
    #f dot_product
    def dot_product(self, other):
        return vectors.vector_dot_product(self.coords, other.coords)
    #f cross_product_3d
    def cross_product_3d( self, other ):
        c = []
        for i in range(3):
            c.append( self.coords[(i+1)%3]*other.coords[(i+2)%3] -
                      other.coords[(i+1)%3]*self.coords[(i+2)%3] )
            pass
        if verbose:
            print "result",c
        return c_point(c)
    #f __repr__
    def __repr__( self ):
        result = "("
        for c in self.coords:
            result += "%6.4f "%c
        result += ")"
        return result

#f test_cross_product
def test_cross_product():
    vectors = { "zero":(0,0,0),
                "x":(1,0,0),    "y":(0,1,0), "z":(0,0,1),
                "-x":(-1,0,0), "-y":(0,-1,0), "-z":(0,0,-1),
                "xyz":(1,1,1),
                "-yz":(0,-1,1),
                "-y-z":(0,-1,-1),
                "x-z":(1,0,-1),
                "-xy":(-1,1,0),
                }
    tests = ( ("zero","x","zero"),("zero","y","zero"),("zero","z","zero"),
              ("zero","-x","zero"),("zero","-y","zero"),("zero","-z","zero"),
              ("x","y","z"), ("y","z","x"), ("z","x","y"),
              ("y","x","-z"), ("z","y","-x"), ("x","z","-y"),
              ("x","xyz","-yz"), ("x","-yz","-y-z"),
              ("y","xyz","x-z"), ("z","xyz","-xy"),
              )
    epsilon = 0.000001
    pts = {}
    for (k,v) in vectors.iteritems():
        pts[k] = c_point( coords=v )
        pass
    for (a,b,r) in tests:
        dut = pts[a].cross_product(pts[b])
        d = dut.distance(pts[r])
        if (d>epsilon):
            print "Test failed (a x b)",a,b,r
            print pts[a], pts[b], dut, pts[r], d
            pass
        pass
    # Try b x 2a = -2r
    for (a,b,r) in tests:
        p = pts[a].add(1.0,pts[a])
        dut = pts[b].cross_product(p)
        minus_r = pts[b].add(-1.0,pts[b]).add(-2.0,pts[r])
        d = dut.distance(minus_r)
        if (d>epsilon):
            print "Test failed (b x 2a)",b,a,minus_r
            print pts[a], pts[b], dut, minus_r, d
            pass
        pass
    # Note that if a x b1 = r1
    # And a x b2 = r2
    # Then a x (b1+b2) = (r1+r2)
    for (a,b1,r1) in tests:
        for (ap, b2, r2) in tests:
            if (a==ap):
                b1b2 = pts[b1].add(1.0,pts[b2])
                dut = pts[a].cross_product(b1b2)
                r1r2 = pts[r1].add(1.0,pts[r2])
                d = dut.distance(r1r2)
                if (d>epsilon):
                    print "Test failed (a x (b1+b2))",a,b1,b2,r1,r2
                    print pts[a], b1b2, dut, r1r2, d
                    pass
                pass
            pass
        pass

#a Toplevel
def main():
    pass

if __name__ == '__main__': main()
