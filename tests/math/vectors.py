#!/usr/bin/env python
#a Imports
import math
from gjslib.math.vectors import *
import unittest
epsilon = 1E-9

#a Test
#c Simple vector tests
class SimpleVectorTests(unittest.TestCase):
    """
    Functions to test:
    vector_scale - in test_scale
    vector_dot_product - covered by cos_angle_between, length tests, normalize
    vector_squared - in test_length
    vector_length  - in test_length
    vector_separation - in plane_points
    vector_point_on_plane - in plane_points
    vector_normalize - in test_normalize
    vector_add - test_add
    vector_min
    vector_max
    vector_cos_angle_between
    """
    #f check_scalar
    def check_scalar(self,d,value):
        self.assertTrue(abs(d-value)<epsilon, 'Scalars differ too much %s,%s'%(str(d),str(value)))
        pass
    #f check_vector
    def check_vector(self,d,value):
        self.assertEqual(len(value),len(d), 'Length of vectors differs')
        for i in range(len(d)):
            self.assertTrue(abs(value[i]-d[i])<epsilon, 'Coordinate %d mismatches'%i)
            pass
        pass
    #f test_length
    def test_length(self):
        """
        Test that the length of a vector is calculated correctly
        """
        for (v,l) in [((1,),1), 
                      ((1,1),math.sqrt(2)),
                      ((1,-1),math.sqrt(2)),
                      ((1,2,3,4,5,6),9.53939201417),
                      ]:
            self.check_scalar(vector_length(v),l)
            self.check_scalar(vector_squared(v),l*l)
            pass
        return
    #f test_normalize
    def test_normalize(self):
        """
        Test that vectors are normalized correctly
        """
        for v in [(1,),
                      (1,1),
                      (1,2,3,4,5,6),
                      (1,-2,3,-4,5,-6),
                      ]:
            vn = vector_normalize(v)
            self.check_scalar(vector_length(vn),1)
            self.check_scalar(vector_dot_product(vn,v),vector_length(v))
            pass
        return
    #f test_plane_points
    def test_plane_points(self):
        """
        Test points on a plane and separation between vectors
        """
        pts_lists = []
        pts_lists.append( ((0,0),(1,0),(0,1)) )
        pts_lists.append( ((10,10,10),(1,0,-1),(5,0,-5)) )
        for pts in pts_lists:
            (p0,p1,p2) = pts
            tp0 = vector_point_on_plane(p0,p1,p2,0,0)
            tp1 = vector_point_on_plane(p0,p1,p2,1,0)
            tp2 = vector_point_on_plane(p0,p1,p2,0,1)
            tp12m = vector_point_on_plane(p0,p1,p2,0.5,0.5)

            self.check_scalar(vector_separation(tp0,p0),0)
            self.check_scalar(vector_separation(tp1,p1),0)
            self.check_scalar(vector_separation(tp2,p2),0)
            self.check_scalar(vector_separation(tp12m,p1),vector_separation(p1,p2)/2)
            self.check_scalar(vector_separation(tp12m,p2),vector_separation(p1,p2)/2)
            pass
        return
    #f test_scale
    def test_scale(self):
        """
        Test scaling of vectors, by scalars and by lists
        """
        self.check_vector(vector_scale((3,4,5),(2,)),(6,8,10))
        self.check_vector(vector_scale((3,4,5),(1,2,3)),(3,8,15))
        self.check_vector(vector_scale((3,4,5),-1),(-3,-4,-5))
        return
    #f test_add
    def test_add(self):
        """
        Test addition of vectors including scaling
        """
        self.check_vector(vector_add((3,4,5),(1,0,-1)),(4,4,4))
        self.check_vector(vector_add((3,4,5),(1,0,-1),2.0),(5,4,3))
        self.check_vector(vector_add((3,4,5),(1,0,-1),(2.0,)),(5,4,3))
        self.check_vector(vector_add((3,4,5),(1,0,1),(2.0,0,-2.0)),(5,4,3))
        return
    #f test_vector_product
    def test_vector_product(self):
        """
        Test a variety of n-dimensional vector products
        """
        tests = { ((1,2),):(2,-1),
                  ((1,0,0),(0,1,0)):(0,0,1),
                  ((0,1,0),(1,0,0)):(0,0,-1),
                  ((1,0,0),(0,0,1)):(0,-1,0),
                  ((0,0,1),(1,0,0)):(0,1,0),
                  ((1,0,1),(0,0,1)):(0,-1,0),
                  ((1,0,1),(1,0,0)):(0,1,0),
                  ((1,4,6),(7,2,3)):(0,39,-26),
                  ((1,0,0,0),(0,1,0,0),(0,0,1,0)):(0,0,0,-1),
                  ((0,1,0,0),(0,0,1,0),(0,0,0,1)):(1,0,0,0),
                  ((1,2,3,4),(0,1,0,0),(0,0,1,0)):(4,0,0,-1),
                  ((1,2,3,4),(4,2,3,1),(1,1,1,1)):(-3,3,3,-3),
                  ((1,2,3,4),(1,2,2,1),(1,1,1,1)):(-1,3,-3,1),
                  ((1,1,1,1),(1,2,3,4),(1,2,2,1)):(-1,3,-3,1),
                  ((1,2,2,1),(1,1,1,1),(1,2,3,4)):(-1,3,-3,1),
                  ((1,1,1,1),(1,2,2,1),(1,2,3,4)):(1,-3,3,-1),
                  }
        for (vs,r) in tests.iteritems():
            vcp = vector_cross_product(vs)
            #print vs, vcp
            for v in vs:
                self.check_scalar(vector_dot_product(v,r),0)
                pass
            self.check_vector(vcp,r)
            pass
        pass
    #f test_scalar_vector_product
    def xtest_scalar_vector_product(self):
        """
        This is more playing rather than testing. Not part of the suite.
        """
        #(a,b,c) = (1,2,3),(4,0,1),(5,4,2)
        #print vector_add(vector_cross_product([vector_cross_product([a,b]),c]),c,scale=-vector_dot_product(a,b))
        #print vector_add(vector_cross_product([a,vector_cross_product([b,c])]),a,scale=-vector_dot_product(c,b))
        # scalar quadruple produce 4D
        (a4, b4, c4, d4) = (1,2,3,4),(4,2,3,1),(1,1,1,1),(0,5,3,2)
        #print vector_dot_product(a4,vector_cross_product([b4,c4,d4]))
        #print vector_dot_product(b4,vector_cross_product([a4,d4,c4]))
        #print vector_dot_product(c4,vector_cross_product([a4,b4,d4]))
        #print vector_dot_product(d4,vector_cross_product([a4,c4,b4]))
        print (a4, b4, c4, d4)
        print vector_dot_product(a4,vector_cross_product([vector_cross_product([a4,b4,c4]),vector_cross_product([a4,b4,d4]),vector_cross_product([a4,c4,d4])]))
        (a4, b4, c4, d4) = (b4,a4,c4,d4)
        print (a4, b4, c4, d4)
        print vector_dot_product(a4,vector_cross_product([vector_cross_product([a4,b4,c4]),vector_cross_product([a4,b4,d4]),vector_cross_product([a4,c4,d4])]))
        (a4, b4, c4, d4) = (c4,a4,b4,d4)
        print (a4, b4, c4, d4)
        print vector_dot_product(a4,vector_cross_product([vector_cross_product([a4,b4,c4]),vector_cross_product([a4,b4,d4]),vector_cross_product([a4,c4,d4])]))
        print
        (a4, b4, c4, d4, e4) = (1,2,3,4),(4,2,3,1),(1,1,1,1),(0,5,3,2),(7,2,1,3)
        print vector_dot_product(vector_cross_product([a4,b4,vector_cross_product([a4,b4,c4])]),c4)
        print vector_dot_product(vector_cross_product([b4,c4,vector_cross_product([b4,c4,a4])]),a4)
        print vector_dot_product(vector_cross_product([c4,a4,vector_cross_product([c4,a4,b4])]),b4)
        (a3, b3, c3) = (1,2,3),(4,2,3),(1,1,1)
        print vector_dot_product(vector_cross_product([a3,vector_cross_product([a3,b3])]),c3)
        print vector_dot_product(vector_cross_product([b3,vector_cross_product([b3,c3])]),a3)
        #print vector_dot_product(vector_cross_product([b3,vector_cross_product([b4,c4,a4])]),a4)
        #print vector_dot_product(vector_cross_product([c3,vector_cross_product([c4,a4,b4])]),b4)
        # In 3D a plane (2D) is defined by vn . p = k
        # In 3D a line (1D) is defined by vec(vn,p) = kv
        # consider p' = p + a.vn; vec(vn,p') = vec(vn,p) + a.vec(vn,vn) = vec(vn,p) + 0 = kv
        # hence any p describes any point on a line of direction vn
        # In 4D this defines a volume [effectively the dot product is a one-degree-of-freedom-reducer]
        # If one define two (vn,k) pairs one should get the intersection of two volumes, i.e. a plane
        # Hence a plane in 4D corresponds to vn0.p=k0, vn1.p=k1
        # What do we get if we define vec(v0,v1,p) = kv in 4D?
        # Well, consider p' = p + a.v0 + b.v1 we find that p must describe a plane with v0 and v1 in the plane
        # Hence we should find that vec(v0,v1,p) - vec(v2,v3,p) = kv' describes the intersection of two planes, a line
        # Now if p' = p + a.v0 + b.v1 is on the line then we know that:
        # vec(v2,v3,(a.v0+b.v1)) = 0
        # Or, that a(vec v2,v3,v0) = -bvec(v2,v3,v1); this requires b, a=0 since:
        # a.vec(v2,v3,v0).v0 = 0 = -b.vec(v2,v3,v1).v0 => b=0
        # Well, this is because two planes do not necessarily intersect in 4D space...
        # So what is a good vector equation of a line in 4D?
        # Consider in 3D a line defined by vn0.p=k0 and vn1.p=k1, and the direction of the line is vd
        # Then vn0.(p+k.vd) = vn0.p+k.vn0.vd = k0 => vn0.vd = 0, and similarly vn1.vd = 0
        # Hence vd = vec(vn0,vn1) works; note this is a vector perp to the normal of both planes, i.e. in both planes
        # Note that vec(vn0,vd) and vec(vn1,vd) are two independent vectors perpendicular to the line, i.e.
        # vec(vn0,vd).p and vec(vn1,vd).p are two different constants for every point on the line
        # So in 4d we can consider a line defined by vn0.p=k0, vn1.p=k1, vn2.p=k2
        # There is a vector vd = vec(vn0,vn1,vn2) which is in all three volumes, which will be a line
        # Qun:
        # What is vec(p,vn0,vd)? This is vec(p,vn0,vec(vn0,vn1,vn2))
        # Further qun: the second fundamental form for a surface in 4D presumably is a pair of 2x2 matrices?
        return
    # separation
    # min
    # max
    # dot_product
    # cos_angle_between
    pass

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(SimpleVectorTests),
           ]

if __name__ == '__main__':
    unittest.main()
