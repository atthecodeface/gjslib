#!/usr/bin/env python
#a Imports
import math
from gjslib.math.matrix import *
from gjslib.math.quaternion import *
import unittest
epsilon = 1E-9

#a Test
#c Simple matrix tests
class SimpleMatrixTests(unittest.TestCase):
    """
    Methods to test:
    accessors - in basics
    set_identity - in basics
    get_matrix (row_major True/False) - in basics, transpose
    scale - in scale
    get_row - in transpose
    get_column - in transpose
    transpose - in transpose
    copy
    expand
    shrink
    set_perspective
    translate
    apply
    premult
    postmult
    lup_decompose
    lup_invert
    unpivot
    determinant
    lu_split
    inverse
    invert
    eigenvalues
    eigenvector
    """
    #f check_scalar
    def check_scalar(self,d,value):
        self.assertTrue(abs(d-value)<epsilon, 'Scalars differ too much %s,%s'%(str(d),str(value)))
        pass
    #f check_vector
    def check_vector(self,d,value):
        self.assertEqual(len(value),len(d), 'Length of vectors differs')
        for i in range(len(d)):
            self.assertTrue(abs(value[i]-d[i])<epsilon, 'Coordinate %d mismatches (%s,%s)'%(i,str(value[i]),str(d[i])))
            pass
        pass
    #f check_matrix
    def check_matrix(self,m,values):
        d = m.get_matrix(row_major=True)
        self.assertEqual(len(values),len(d), 'Length of data differs')
        for i in range(len(d)):
            self.assertTrue(abs(values[i]-d[i])<epsilon, 'Matrix data %d mismatches'%i)
            pass
        pass
    #f test_basics
    def test_basics(self):
        """
        Test creation of 2x2 to 5x5, get_matrix row major, accessors
        """
        # Test creation from list and read accessor
        data = range(5*5)
        for i in range(1,6):
            m = matrix(data=data[:i*i])
            self.check_matrix(m,data[:i*i])
            for j in range(i*i):
                self.check_scalar(m[j],j)
                pass
            for r in range(i):
                for c in range(i):
                    self.check_scalar(m[r,c],r*i+c)
                    pass
                pass
            pass
        # Test creation from order and write accessor
        for i in range(1,6):
            m = matrix(order=i)
            self.check_matrix(m,[0]*(i*i))
            for r in range(i):
                for c in range(i):
                    m[r,c] = r*i+c
                    pass
                pass
            self.check_matrix(m,range(i*i))
            pass
        # Test identity
        for i in range(1,6):
            m = matrix(order=i).set_identity()
            for r in range(i):
                for c in range(i):
                    self.check_scalar(m[r,c],(r==c) and 1 or 0)
                    pass
                pass
            pass
        return
    #f test_scale
    def test_scale(self):
        """
        Test scaling
        """
        for i in range(1,6):
            m = matrix(order=i).set_identity()
            m.scale(2)
            for r in range(i):
                for c in range(i):
                    self.check_scalar(m[r,c],(r==c) and 2 or 0)
                    pass
                pass
            m.scale(range(i))
            for r in range(i):
                for c in range(i):
                    self.check_scalar(m[r,c],(r==c) and (2*r) or 0)
                    pass
                pass
            pass
            m.scale([3,2])
            for r in range(i):
                for c in range(i):
                    if r==1:
                        self.check_scalar(m[r,c],(r==c) and (2*r*2) or 0)
                        pass
                    else:
                        self.check_scalar(m[r,c],(r==c) and (2*r) or 0)
                        pass
                    pass
                pass
            pass
        pass
    #f test_transpose
    def test_transpose(self):
        """
        Test transpose and get_row/col/matrix'es
        """
        for i in range(1,6):
            m = matrix(data=range(i*i))
            for r in range(i):
                d = m.get_row(r)
                self.check_vector(d,range(r*i,r*i+i))
                d = m.get_column(r)
                self.check_vector(d,range(r,i*i+r,i))
                m.transpose()
                d = m.get_row(r)
                self.check_vector(d,range(r,i*i+r,i))
                d = m.get_column(r)
                self.check_vector(d,range(r*i,r*i+i))
                m.transpose()
                pass
            d1 = m.get_matrix(row_major=False)
            m.transpose()
            d2 = m.get_matrix(row_major=True)
            self.check_vector(d1,d2)
            pass
        pass
    #f All done
    pass
#a Main
def main():
    print "Eigenvectors of (3,0, 2,1)"
    a = c_matrixNxN(data=[3.,0.,2.,1.])
    print "Eigen values",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
    print "Eigenvectors of (1,0, -2,3)"
    a = c_matrixNxN(data=[1.,0.,-2.,3.])
    print "Eigen values",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
    print "Eigenvectors of (1,0,1, 4,3,1, -2,3,2)"
    a = c_matrixNxN(data=[1.,0.,1., 4.,3.,1., -2.,3.,2.])
    print "Eigen values",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
        pass
    a.invert()
    print "Eigen values of a_inverse",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
        pass
    die
    print "LU decompose of 1,2 4,3 should be U=4,3 0,1.25  L= 1,0 0.25,1, P = 2,1; as one matrix this is 4,3, 0.25,1.25"
    a = c_matrixNxN(data=[1.,2.,4.,3.])
    print "A", a
    lup = a.lup_decompose()
    print "LUP", lup
    a_i = lup[0].lup_invert(lup[1])
    print "A inverse", a_i
    print c_matrixNxN.multiply_matrices(a,a_i)

    print
    print "More matrices"
    #a = c_matrixNxN(data=[1.,0.,0.,1.])
    a = c_matrixNxN(data=[1.,2.,3,4.,5.,4.,6.,3,2.])
    #L = c_matrixNxN(data=[1.,0.,0.,2.,1.,0.,3.,4.,1.])
    #U = c_matrixNxN(data=[3.,4.,6.,0.,2.,9.,0.,0.,1.])
    #LU = c_matrixNxN.combine_lu(L,U)
    #print "LU", LU
    #lup = (LU, lup[1])
    print "A", a
    lup = a.lup_decompose()
    print "LUP", lup
    a_i = lup[0].lup_invert(lup[1])
    print "A inverse", a_i
    print c_matrixNxN.multiply_matrices(a,a_i)

    for a in [c_matrixNxN(data=[1.,0.,0.,0.,  0.,4.,2.,0., -5.,0.,0.,1., 0.,0.,1.,0.]),
              c_matrixNxN(data=[-1.,3.,4.,5.,  0.,4.,2.,1., -5.,5.,2.,-3., -4.,3.,2.,1.]),
              c_matrixNxN(data=[-8.780454382560094, 4.24389067150205, 4.057661342681895, 1.1304208758453387, 0.2038639118735965, 6.330794706227703, -5.484817504274374, -0.16412212696591522, 25.412595302329905, 26.87675575660128, 20.381364036786152, 11.636150566231086, -13.519396156451739, -14.71734561903741, -9.402934211915941, -2.2477595541890696])
              ]:
        print
        print "4 by 4..."
        print "A",a
        lup = a.lup_decompose()
        print "LUP", lup
        L,U = lup[0].lu_split()
        print "U",U
        print "L",L
        LU=c_matrixNxN.multiply_matrices(L,U)
        print "L.U", LU
        print "L.U.P which should be A", LU.unpivot(lup[1])

        print 
        print "Continuing"
        print "A inverse"
        a_i = a.inverse()
        print a_i
        b = a.copy()
        print "B = copy of A",b
        b.invert()
        print "B inverted"
        print b
        b.postmult(a)
        print "B inverted . A = Identity?"
        print b

        print
        print "Continuing"
        print "Determinant of A", a.determinant()
        print "Determinant of A_inverse", a_i.determinant()
        print "1?", a.determinant() *a_i.determinant()

        pass
    return
    a = c_matrix4x4((1.0,0.0,0.0,0.0),
              (0.0,1.0,0.0,0.0),
              (0.0,0.0,1.0,0.0),
              (0.0,0.0,0.0,1.0))
    a.perspective(90.0,1.0,1.0,40.0)
    a.mult3x3( (1.0,0.0,0.0, 0.0,1.0,0.0, 0.0,0.0,1.0) )    
    a.translate( (-2.0,-3.0,-4.0) )
    a.mult3x3( (0.5,0.866,0.0, -0.866,0.5,0.0, 0.0,0.0,1.0) )    
    a.mult3x3( (0.5,-0.866,0.0, 0.866,0.5,0.0, 0.0,0.0,1.0) )    
    a.translate( (2.0,3.0,4.0) )
    print a

    a = c_matrix2x2( (0.0,2.0,-2.0,0.0) )
    print a.matrix
    a.invert()
    print a.matrix
    pass

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(SimpleMatrixTests),
           ]

if __name__ == '__main__':
    unittest.main()
