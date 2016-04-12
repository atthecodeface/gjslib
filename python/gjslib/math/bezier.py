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
from gjslib.math.vectors import *

#a Bezier classes
#c bezier_base
class bezier_base(object):
    """
    An arbitrary bezier curve class - should it be derived from a 'curve' class?
    """
    n = 100
    fmt = "%6.2f"

    #f __init__
    def __init__(self, pts=None, controls_relative=False, subdivision_level=0, split_parent=None, first_split=True, **kwargs):
        """
        Create a Bezier curve object directly from points or from a subdivision of another Bezier curve
        
        Invoke with pts to create a Bezier curve from scratch
        Invoke with split_parent and first_split=True/False to create a subdivision of a parent Bezier
        In the latter case split_parent may have properties to inherit, particularly if this
        class is subclassed

        Control points may be relative to the start/end points if required
        (they are relative to the closest start/end point; those closest to the end point are subtracted from the end)
        """
        self._subdivision_level = subdivision_level
        self._parent = split_parent
        self.pts = pts
        if controls_relative:
            p = list(pts)
            l = len(pts)
            for i in range(l/2-1):
                p[i+1]   = vector_add(p[0],p[i+1])
                p[l-2-i] = vector_add(p[1],p[l-2-i],scale=-1)
                pass
        if split_parent is not None:
            self._subdivision_level = split_parent._subdivision_level+1
            self.pts = split_parent.pts
            self.pts = self.split(first_split)
            pass
        pass
    #f break_into_segments
    def break_into_segments(self, straightness):
        """
        Break the Bezier curve into segments, until the segments are straight enough
        """
        lines = [self]
        i = 0
        while i<len(lines):
            if not lines[i].straight_enough(straightness):
                l = lines.pop(i)
                lines.insert(i,self.__class__(split_parent=l,first_split=False))
                lines.insert(i,self.__class__(split_parent=l,first_split=True))
                pass
            else:
                i+=1
                pass
            pass
        return lines
    #f draw_in_dots
    def draw_in_dots(self, dot_fn, steps=100):
        """
        Draw the Bezier curve in dots
        """
        for t in range(steps+1):
            dot_fn(self.evaluate(t/(steps+0.0)))
            pass
        pass
    #f draw_in_lines
    def draw_in_lines(self, line_fn):
        line_fn(self.pts[0], self.pts[-1])
        pass
    #f __repr__
    def __repr__(self ):
        import string
        pts = []
        for p in self.pts:
            pts.append(str(p))
            pass
        pts = string.join(pts, ", ")
        return "bezier(%s)"%pts
    #f All done
    pass

#c bezier_quad
class bezier_quad(bezier_base):
    """
    A quadratic bezier curve class

    Here a point is defined by p(t) = (1-t)^2 * p0 + 2t(1-t) * c0 + t^2 * p1
    If we subdivide, we need p(0)=p0, p(1/2)=p0/4 + c0/2 + p1/4, and p(1)=p1
    And we need new control points

    We will end up with a q(u) (0<=u<=1) where q(u)=p(u/2) - this is the first half of the subdivide
    Now if we express q(u) as (1-u)^2 * p0 + 2u(1-u) * C0 + u^2 * (p0/4 + c0/2 + p1/4)
    q(0) = p0; q(1) = p0/4 + c0/2 + p1/4 ; q(1/2) = p0/4 + C0/2 + p0/16 + c0/8 + p1/16
    Note that p(1/4) should be the same as q(1/2), and p(1/4) = 9/16*p0 + 6/16*c0 + 1/16*p1
    So we can deduce that C0 = 8/16*p0 + 8/16*c0 = p0/2 + c0/2

    For the second half of the subdivide we have r(u)
    Now if we express r(u) as (1-u)^2 * (p0/4 + c0/2 + p1/4) + 2u(1-u) * C1 + u^2 * p1
    r(0) = p0/4 + c0/2 + p1/4 ; r(1) = p1; r(1/2) = p0/16 + c0/8 + p1/16 + C1/2 + p1/4
    Note that p(3/4) should be the same as q(1/2), and p(3/4) = 1/16*p0 + 6/16*c0 + 9/16*p1
    So we can deduce that C1 = 8/16*c0 + 8/16*p1 = c0/2 + p1/2
    """
    n = 100
    fmt = "%6.2f"
    #f split
    def split(self, first_split):
        """
        Split this Bezier as either the first or second half
        This is invoked by the class instance function to set the points based on splitting the
        parent. self.pts is already copied from the parent
        """
        (p0, c0, p1) = self.pts
        if first_split:
            return (p0,
                        vector_scale(vector_add(p0,c0),0.5),
                        vector_scale(vector_add(p1,vector_add(p0,c0,scale=2)),0.25),
                        )
        else:
            return (vector_scale(vector_add(p1,vector_add(p0,c0,scale=2)),0.25),
                        vector_scale(vector_add(p1,c0),0.5),
                        p1 )
        pass
    #f evaluate
    def evaluate(self, t):
        """
        Return a vector of the Bezier curve evaluates at parameter 't'
        """
        (p0, c0, p1) = self.pts
        u = 1-t
        v = vector_scale(p0,u*u)
        v = vector_add(v,c0,2*t*u)
        v = vector_add(v,p1,t*t)
        return v
    #f straight_enough
    def straight_enough(self, straightness):
        """
        Return True if the Bezier approximates closely enough to a straight line
        If the cosine of the angle between the control point and either end of the line
        is less than 1-straightness then the line is not straight enough
        """
        p10u = vector_normalize(vector_add(self.pts[-1], self.pts[0], scale=-1))
        cp1u = vector_normalize(vector_add(self.pts[1], self.pts[0], scale=-1))
        cp0u = vector_normalize(vector_add(self.pts[-1], self.pts[1], scale=-1))
        c_alpha_p0 = vector_dot_product(p10u, cp1u)
        c_alpha_p1 = vector_dot_product(p10u, cp0u)
        if c_alpha_p0 < 1-straightness:return False
        if c_alpha_p1 < 1-straightness:return False
        return True
    #f straight_enough
    def straight_enough(self, straightness):
        """
        Return True if the Bezier approximates closely enough to a straight line
        If the cosine of the angle between the control point and either end of the line
        is less than 1-straightness then the line is not straight enough
        """
        max_excursion = vector_squared(vector_add(vector_add(self.pts[0],self.pts[2]),self.pts[1],scale=-2))/16
        print max_excursion
        return max_excursion<straightness
    #f All done
    pass

#c bezier_cubic
class bezier_cubic( object ):
    """
    A cubic bezier curve class

    Here a point is defined by p(t) = (1-t)^3*p0 + 3t(1-t)^2*c0 + 3t^2*(1-t)*c1 + t^3*p1
    If we subdivide, we need p(0)=p0, p(1/2)=(p0+p1)/8 + 3/8*(c0+c1), and p(1)=p1
    And we need new control points
    """
    n = 100
    fmt = "%6.2f"
    #f split
    def split(self, first_split):
        """
        Split this Bezier as either the first or second half
        This is invoked by the class instance function to set the points based on splitting the
        parent. self.pts is already copied from the parent
        """
        (p0, c0, c1, p1) = self.pts
        if first_split:
            self.pts = ( p0,
                         vector_scale(vector_add(p0,c0),1/2.0),
                         vector_scale(vector_add(vector_add(p0,c0,scale=2),c1),1/4.0),
                         vector_scale(vector_add(vector_add(vector_add(p0,c0,scale=3),c1,scale=3),p1),1/8.0),
                         )
        else:
            self.pts = ( vector_scale(vector_add(vector_add(vector_add(p0,c0,scale=3),c1,scale=3),p1),1/8.0),
                         vector_scale(vector_add(vector_add(p1,c1,scale=2),c0),1/4.0),
                         vector_scale(vector_add(p1,c1),1/2.0),
                         p1,
                         )
        pass
    #f evaluate
    def evaluate(self, t):
        """
        Return a vector of the Bezier curve evaluates at parameter 't'
        """
        (p0, c0, c1, p1) = self.pts
        u = 1-t
        v = vector_scale(p0,u*u*u)
        v = vector_add(v,c0,3*t*u*u)
        v = vector_add(v,c1,3*t*t*u)
        v = vector_add(v,p1,t*t*t)
        return v
    #f straightness
    def straightness(self):
        """
        Evaluate the straightness of the Bezier curve
        """
        p10n = (self.pts[3][1]-self.pts[0][1], self.pts[0][0]-self.pts[3][0])
        c0p10n = (self.pts[1][0]-self.pts[0][0])*p10n[0] + (self.pts[1][1]-self.pts[0][1])*p10n[1]
        c1p10n = (self.pts[2][0]-self.pts[3][0])*p10n[0] + (self.pts[2][1]-self.pts[3][1])*p10n[1]
        max = c0p10n
        if (max<0): max=-max
        if (c1p10n<0) and (-c1p10n>max): max=c1p10n
        if (c1p10n>max): max=c1p10n
        len_p10n = p10n[0]*p10n[0] + p10n[1]*p10n[1]
        print c0p10n, c1p10n, len_p10n, max*max, (max*max)*10/len_p10n
        return (max*max)/len_p10n
    #f straight_enough
    def straight_enough(self, straightness):
        """
        Calculate if the Bezier curve meets the 'straightness' criterion
        """
        p10n = (self.pts[3][1]-self.pts[0][1], self.pts[0][0]-self.pts[3][0])
        len_p10n = p10n[0]*p10n[0] + p10n[1]*p10n[1]
        v_len_p10n = straightness*len_p10n
        c0p10n = (self.pts[1][0]-self.pts[0][0])*p10n[0] + (self.pts[1][1]-self.pts[0][1])*p10n[1]
        if c0p10n*c0p10n>v_len_p10n: return False
        c1p10n = (self.pts[2][0]-self.pts[3][0])*p10n[0] + (self.pts[2][1]-self.pts[3][1])*p10n[1]
        if c1p10n*c1p10n>v_len_p10n: return False
        return True
    #f split
    def split( self ):
        return ( self.__class__(split_parent=self, first_split=True),
                 self.__class__(split_parent=self, first_split=False) )
    #f All done
    pass

#c bezier_cubic_patch
class bezier_cubic_patch(object):
    """
    A class for an arbitrary dimension cubic Bezier patch

    A bezier patch here has 16 values - this is 4 corner points, and for each corner 3 control points
    The points are supplied in a 16-entry array
    The corners are points 0, 3, 12, 15
    """
    factors = [ 1.0, 3.0, 3.0, 1.0,
                3.0, 9.0, 9.0, 3.0,
                3.0, 9.0, 9.0, 3.0,
                1.0, 3.0, 3.0, 1.0 ]
    #f __init__
    def __init__( self, pts ):
        self.pts = pts
        self._dimension = len(pts[0])
        pass
    #f _bezier_gradient
    def _bezier_gradient(self, ofs=0, stride=1, t=0):
        """
        Calculate the gradient of a cubic Bezier given by points ofs,ofs+stride,ofs+2*stride,ofs+3*stride
        at parameter value 't'
        """
        tis = [ -3*(1-t)*(1-t), 3*(1-t)*(1-3*t), 3*(2-3*t)*t, 3*t*t ]
        pt = [0]*self._dimension
        for i in range(4):
            pt = vector_add(pt, self.pts[ofs+i*stride], scale=tis[i])
            pass
        return pt
    #f normal
    def normal(self, t, u):
        """
        Find normal to a bicubic patch at parameters t, u

        This requires points in 3 dimensional space as that is the only geometry which has a single normal to a plane
        """
        tis = [ (1-t)*(1-t)*(1-t), 3*(1-t)*(1-t)*t, 3*(1-t)*t*t, t*t*t ]
        uis = [ (1-u)*(1-u)*(1-u), 3*(1-u)*(1-u)*u, 3*(1-u)*u*u, u*u*u ]
        dt_vec = [0]*self._dimension
        du_vec = [0]*self._dimension
        for i in range(4):
            dt_vec = vector_add(dt_vec, self._bezier_gradient( ofs=4*i, stride=1, t=t ), scale=uis[i])
            du_vec = vector_add(du_vec, self._bezier_gradient( ofs=i,   stride=4, t=u ), scale=tis[i])
            pass
        return vector_cross_product([dt_vec,du_vec])
    #f coord
    def coord( self, t, u ):
        """
        Calculate the bezier patch coordinate given by parameters t and u
        0<=t<=1, 0<=u<=1
        """
        pt = [0]*self._dimension
        tis = [ (1-t)*(1-t)*(1-t), (1-t)*(1-t)*t, (1-t)*t*t, t*t*t ]
        uis = [ (1-u)*(1-u)*(1-u), (1-u)*(1-u)*u, (1-u)*u*u, u*u*u ]
        for i in range(4):
            for j in range(4):
                pt = vector_add(pt, self.pts[i+4*j], scale=self.factors[i+4*j]*tis[i]*uis[j])
                pass
            pass
        return pt
    #f All done
    pass
