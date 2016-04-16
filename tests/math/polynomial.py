#!/usr/bin/env python
#a Imports
import math
from gjslib.math.complex import *
from gjslib.math.polynomial import *
import unittest
epsilon = 1E-6
sqrt2 = math.sqrt(2)
pi = math.pi

#a Test
#c Base test class
class TestBase(unittest.TestCase):
    def check_scalar(self,d,value):
        self.assertTrue(abs(d-value)<epsilon, 'Scalars differ too much %s,%s'%(str(d),str(value)))
        pass
    def check_vector(self,d,value):
        self.assertEqual(len(value),len(d), 'Length mismatch in vector')
        for i in range(len(d)):
            self.assertTrue(abs(d[i]-value[i])<epsilon, 'Element %d mismatches (%s)'%(i,str(d)))
            pass
        pass
    def check_complex(self,q,value):
        (r,i,j,k) = q.get()
        d = (r,i,j,k)
        self.assertEqual(len(value),len(d), 'BUG: Length of quaternion test value is not 4!!')
        for i in range(len(d)):
            self.assertTrue(abs(d[i]-value[i])<epsilon, 'Coordinate %d mismatches (%s)'%(i,str(d)))
            pass
        pass

#c Quadratic tests
class QuadraticTests(TestBase):
    """
    """
    def test_real_coeffs(self):
        q_xsq_m_1 = quadratic(1,0,-1)
        q_xsq_p_1 = quadratic(1,0,1)
        self.check_vector(q_xsq_m_1.coeffs(),(1,0,-1))
        r = q_xsq_m_1.find_real_roots()
        self.check_vector(r,(1,-1))
        r = q_xsq_p_1.find_real_roots()
        self.check_vector(r,[])
        q = quadratic(1,-2,1)
        self.check_vector(q.find_real_roots(),(1,1))
        q = quadratic(1,2,1)
        self.check_vector(q.find_real_roots(),(-1,-1))
        q = quadratic(4,4,1)
        self.check_vector(q.find_real_roots(),(-0.5,-0.5))
        r = q_xsq_p_1.find_all_roots()
        self.check_vector(r,[complex(imaginary=1),complex(imaginary=-1)])
    def test_complex_coeffs(self):
        i = complex(imaginary=1)
        z = complex()
        r = complex(real=1)
        rt2 = pow(2,0.5)
        q_xsq_m_i = quadratic(r,z,i)
        self.check_vector(q_xsq_m_i.coeffs(),(r,z,i))
        self.check_vector(q_xsq_m_i.find_all_roots(),(complex(1/rt2,-1/rt2),
                                                      complex(-1/rt2,1/rt2)))
        q_ixsq_m_1 = quadratic(i,z,r)
        self.check_vector(q_ixsq_m_1.coeffs(),(i,z,r))
        self.check_vector(q_ixsq_m_1.find_all_roots(),(complex(1/rt2,1/rt2),
                                                      complex(-1/rt2,-1/rt2)))
        q = quadratic(1,2,1)
        self.check_vector(q.find_all_roots(),(complex(-1),complex(-1)))
        q = quadratic(i,i*2,i)
        self.check_vector(q.find_all_roots(),(complex(-1),complex(-1)))
        q = quadratic(r,i*2,r)
        self.check_vector(q.find_all_roots(),(i*(rt2-1),-i*(rt2+1)))
    pass

#c Cubic tests
class CubicTests(TestBase):
    def test_real_coeffs(self):
        i = complex(imaginary=1)
        z = complex()
        r = complex(real=1)
        rt2 = pow(2,0.5)
        rt3 = pow(3,0.5)

        c_x3_m_1 = cubic(1,0,0,-1)
        self.check_vector(c_x3_m_1.coeffs(),(1,0,0,-1))
        self.check_vector(c_x3_m_1.find_real_roots(),[1])

        c = cubic(1,0,0,1)
        self.check_vector(c.find_real_roots(),[-1])

        c = cubic(1,3,3,1)
        self.check_vector(c.find_real_roots(),[-1, -1, -1])

        c = cubic(1,-3,3,-1)
        self.check_vector(c.find_real_roots(),[1, 1, 1])

        c = cubic(1,-6,11,-6)
        self.check_vector(c.find_real_roots(),[3,1,2])

        c = cubic(1,0,0,1)
        self.check_vector(c.find_all_roots(),[-r, r/2-i*rt3/2, r/2+i*rt3/2])
        c = cubic(1,-6,11,-6)
        self.check_vector(c.find_all_roots(),[r*3,r*1,r*2])
    pass

#c Polynomial tests
class PolynomialTests(TestBase):
    pass

#a Toplevel
loader = unittest.TestLoader().loadTestsFromTestCase
suites = [ loader(QuadraticTests),
           ]

if __name__ == '__main__':
    unittest.main()
