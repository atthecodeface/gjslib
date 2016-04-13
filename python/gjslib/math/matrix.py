#!/usr/bin/env python
import math
import vectors
import polynomial
  
#a Classes
#c matrix
class matrix(object):
    """
    N x N matrix, held in a linear list in row-major order

    i.e. matrxi[1] is the second column, first row
    """
    order = 2
    #f multiply_matrix_data
    @classmethod
    def multiply_matrix_data( cls, n, m0, m1 ):
        m = []
        for r in range(n): # Row of result
            for c in range(n): # Col of result
                d = 0
                for k in range(n):
                    d += m0[r*n+k] * m1[k*n+c]
                    pass
                m.append(d)
                pass
            pass
        return m
    #f multiply_matrices
    @classmethod
    def multiply_matrices( cls, matrix_0, matrix_1 ):
        m = cls.multiply_matrix_data(matrix_0.order, matrix_0.matrix, matrix_1.matrix)
        return cls(data=m)
    #f lookat
    @classmethod
    def lookat(cls, eye, target, up):
        forward = vectors.vector_add(target, eye, scale=-1.0)
        forward = vectors.vector_normalize(forward)
        side    = vectors.vector_cross_product([forward,up])
        side    = vectors.vector_normalize(side)
        up      = vectors.vector_cross_product([side,forward])
        up      = vectors.vector_normalize(up)
        return cls(data= (side[0], side[1], side[2],
                          up[0], up[1], up[2],
                          -forward[0], -forward[1], -forward[2]))
    #f combine_lu
    @classmethod
    def combine_lu(cls, L, U):
        m = U.copy()
        for c in range(U.order):
            for r in range(U.order):
                if (c>r):
                    m[c,r] = L[c,r]
                    pass
                pass
            pass
        return m
    #f __init__
    def __init__(self, order=None, data=None):
        if order is None:
            if data is None:
                order=self.order
                pass
            else:
                order = [1,4,9,16,25,36].index(len(data))+1
                pass
            pass
        self.order = order
        if data is None:
            self.matrix = [0.]*(order*order)
            pass
        else:
            if len(data) != order*order:
                raise Exception("Bad data for order %d matrix"%order)
            self.matrix = list(data[:])
            pass
        pass
    #f __getitem__
    def __getitem__(self,key):
        if type(key)==tuple:
            key = self.order*key[0]+key[1]
        return self.matrix[key]
    #f __setitem__
    def __setitem__(self,key, value):
        if type(key)==tuple:
            key = self.order*key[0]+key[1]
        self.matrix[key] = value
    #f __repr__
    def __repr__(self):
        return str(self.matrix)
    #f set_identity
    def set_identity(self):
        n = self.order
        for r in range(n):
            for c in range(n):
                self[r,c] = ((r==c) and 1.0) or 0.0
                pass
            pass
        return self
    #f get_matrix
    def get_matrix(self, row_major=True):
        if row_major:
            return self.matrix
        m = self.copy()
        m.transpose()
        return m.matrix
    #f get_row
    def get_row(self, r):
        n = self.order
        return self.matrix[r*n:(r+1)*n]
    #f get_column
    def get_column(self, c):
        n = self.order
        return self.matrix[c:n*n+c:n]
    #f copy
    def copy(self):
        return matrix(data=self.matrix)
    #f expand
    def expand(self, order):
        if order<self.order:
            raise Exception("Attempt to shrink a matrix order with 'expand'")
        while self.order<order:
            n = self.order
            d = self.matrix
            self.matrix = [0]*(n+1)*(n+1)
            self.order = n+1
            self.matrix[-1] = 1.0
            for r in range(n):
                for c in range(n):
                    self.matrix[r*(n+1)+c] = d[r*n+c]
                pass
            pass
        return self
    #f shrink
    def shrink(self, order, r=0, c=0):
        if order+r>self.order:
            raise Exception("Attempt to shrink with data beyond the width of the matrix")
        if order+c>self.order:
            raise Exception("Attempt to shrink with data beyond the height of the matrix")
        data = [0]*order*order
        for i in range(order):
            for j in range(order):
                data[order*i+j] = self[r+i,c+j]
                pass
            pass
        self.matrix = data
        self.order = order
        return self
    #f set_perspective
    def set_perspective(self,fov,aspect,zFar,zNear):
        f = 1/math.tan(fov*3.14159265/180.0/2)
        self.matrix = [f/aspect, 0.0, 0.0, 0.0,
                       0.0, f, 0.0, 0.0,
                       0.0, 0.0, (zFar+zNear)/(zFar-zNear), 2.0*(zFar*zNear)/(zFar-zNear),
                       0.0, 0.0, -1.0, 0.0]
        pass
    #f scale
    def scale(self, scale=1.0):
        n = self.order
        if type(scale)==int:
            scale = float(scale)
        if type(scale)==float:
            scale = [scale]*n
        for r in range(n):
            for c in range(min(n,len(scale))):
                self[r,c] *= scale[c]
                pass
            pass
        return self
    #f translate
    def translate(self,v,scale=1.0):
        m = [0]*self.order*self.order
        for i in range(self.order):
            if i<self.order-1:
                m[i*self.order+self.order-1] = v[i]
                pass
            m[i*(self.order+1)] = 1
            pass
        self.premult(matrix(data=m))
        pass
    #f apply
    def apply(self, v):
        n = self.order
        r = []
        for i in range(n):
            d = 0
            for j in range(n):
                d += self.matrix[i*n+j]*v[j]
                pass
            r.append(d)
            pass
        return r
    #f transpose
    def transpose(self):
        n = self.order
        r = []
        for i in range(n):
            d = 0
            for j in range(n):
                r.append(self.matrix[j*n+i])
                pass
            pass
        self.matrix = r
        return self
    #f premult
    def premult(self, matrix=None, data=None):
        if matrix is not None: data=matrix.matrix
        self.matrix = matrix.multiply_matrix_data(self.order, data, self.matrix)
        return self
    #f postmult
    def postmult(self, matrix=None, data=None):
        if matrix is not None: data=matrix.matrix
        self.matrix = matrix.multiply_matrix_data(self.order, self.matrix, data)
        return self

    #f lup_decompose
    def lup_decompose(self):
        """
        Decompose into L and U matrices with a pivot P
        """
        n =  self.order
        P = []
        for i in range(n): P.append(i)

        LU = self.copy()
        # Run through the diagonal
        for d in range(n-1):
            # Find row with maximum (abs) value in c,r
            p = 0.
            r_max = None
            for r in range(d,n):
                t = LU[r, d]
                if t<0: t=-t
                if t>p:
                    p     = t
                    r_max = r
                    pass
                pass
            #print "Diagonal",d,"has max in row",p,r_max
            if p==0:
                return None
                raise Exception("Noninvertible matrix")

            # Swap row i with r_max and update the pivot list
            if r_max != d:
                (P[d], P[r_max]) = (P[r_max], P[d])
                for c in range(n):
                    (LU[d,c], LU[r_max,c]) = (LU[r_max,c], LU[d,c])
                    pass
                pass

            # Subtract out from rows below scaling down by LU[d][d] (in p) and up by LU[r][r]
            for r in range(d+1,n):
                scale = LU[r,d]/LU[d,d]
                LU[r,d] = scale
                for c in range(d+1,n):
                    LU[r,c] -= scale*LU[d,c]
                    pass
                pass

            # Next element on the diagonal...
            #print "After diagonal",d,LU
            pass
        return (LU, P)
    #f lup_invert
    def lup_invert(self, P):
        """
        self should be an LU matrix
        Note that LUP matrix is actually a matrix P.L.U
        If we find vectors 'x' such that L.U.x = P-1.Ic for the c'th column of the identity matrix
        we will find (with all 'n' x) the inverse
        """
        n = self.order
        R = matrix(order=n)

        # For each column in the identity matrix...
        for c in range(n):
            # We want to find vector x such that LU.x = Ic
            # First find a such that L.a = Ic
            # Note that as L is a lower, we can find the elements top down
            a = [0]*n
            a[c] = 1
            for r in range(n):
                # Would divide a[r] by Lrr, but that is 1 for L
                # a[r] = a[r]/1
                # For the rest of the column remove multiples of a[r] (Lir, n>i>r)
                for i in range(r+1,n):
                    a[i] -= self[i,r]*a[r]
                    pass
                pass

            # Now we have L.a = Ic
            # Hence a = U.x
            # Here we can work up from the bottom of x - we have to start with a...
            x = a
            for r in range(n-1,-1,-1):
                # Now divide a[r] by Urr, which is not 1
                if self[r,r]==0.0: return None
                x[r] = x[r]/self[r,r]
                # For the rest of the column remove multiples of x[r] (Uir, r>i>=0)
                for i in range(0,r):
                    x[i] -= self[i,r]*x[r]
                    pass
                pass

            # So we know that LU.x = Ic
            # Insert into R at the permuted column
            for r in range(n):
                R[P[c],r] = x[r]
                pass
   
            pass
        R.transpose()
        return R
    #f unpivot
    def unpivot(self, P):
        """
        'Unapply' the pivot P
        """
        n = self.order

        data = []
        for r in range(n):
            data.extend(self.get_row(P.index(r)))
            pass
        return matrix(data=data)
    #f determinant
    def determinant(self):
        """
        Decompose to LUP, then det(U).det(P)
        det(P) = +-1 depending on the number of swaps required
        """
        n = self.order
        lup = self.lup_decompose()
        if lup is None:
            return 0.0
        (LU, P) = lup
        det_P = 1
        for i in range(n):
            if P[i] != i:
                det_P = -det_P
                P_i = P.index(i)
                P[P_i] = P[i]
                P[i] = i
                pass
            pass
        det = 1.0 * det_P
        for rc in range(n):
            det *= LU[rc,rc]
            pass
        return det
    #f lu_split
    def lu_split(self):
        """
        Split an LU where L has diagonal of 1s and is stored in lower half, U is upper half
        """
        L = self.copy()
        U = self.copy()
        n = self.order

        for r in range(n):
            for c in range(n):
                if (r==c):
                    L[r,c] = 1.
                    pass
                elif (r<c):
                    L[r,c] = 0.
                    pass
                else:
                    U[r,c] = 0.
                    pass
                pass
            pass
        return (L, U)
    #f inverse
    def inverse(self):
        lup = self.lup_decompose()
        if lup is None:
            return None
        return lup[0].lup_invert(lup[1])
    #f invert
    def invert(self):
        m = self.inverse()
        self.matrix = m.matrix
        return self
    #f eigenvalues
    def eigenvalues(self, real=True):
        if self.order==1:
            return self.matrix[0]
        if self.order==2:
            (a,b,c,d) = self.matrix
            q = polynomial.c_quadratic(1,-(a+d),a*d-b*c)
            if real:
                return q.find_real_roots()
            return q.find_all_roots()
        if self.order!=3:
            raise Exception("Eigenvalues can only be found for matrices of order <=3 currently")
        (a,b,c, d,e,f, g,h,i) = self.matrix
        q = polynomial.c_cubic(-1, a+e+i, b*d-a*e + f*h-e*i + c*g-a*i, 
                                a*e*i + b*f*g + c*d*h - a*f*h - b*d*i - c*e*g)
        if real:
            return q.find_real_roots()
        return q.find_all_roots()
    #f eigenvector
    def eigenvector(self, eigenvalue):
        """
        We know that M.v = kv.
        If we try v=(1,_,_) then we get n equations with n-1 unknowns
        We can drop one equation (any) and attempt to resolve the other coordinates
        """
        n = self.order
        for c in range(n):
            m = self.copy()
            for i in range(n):
                if c!=i:
                    m[i,i] = m[i,i] - eigenvalue
                    pass
                pass
            m_i = m.inverse()
            if m_i is None:
                continue
            v = [0.0]*n
            v[c] = 1.0
            return m_i.apply(v)
            pass
        pass
    #f All done
    pass
#a Main
def main():
    print "Eigenvectors of (3,0, 2,1)"
    a = matrix(data=[3.,0.,2.,1.])
    print "Eigen values",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
    print "Eigenvectors of (1,0, -2,3)"
    a = matrix(data=[1.,0.,-2.,3.])
    print "Eigen values",a.eigenvalues()
    for e in a.eigenvalues():
        print a.eigenvector(e)
    print "Eigenvectors of (1,0,1, 4,3,1, -2,3,2)"
    a = matrix(data=[1.,0.,1., 4.,3.,1., -2.,3.,2.])
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
    a = matrix(data=[1.,2.,4.,3.])
    print "A", a
    lup = a.lup_decompose()
    print "LUP", lup
    a_i = lup[0].lup_invert(lup[1])
    print "A inverse", a_i
    print matrix.multiply_matrices(a,a_i)

    print
    print "More matrices"
    #a = matrix(data=[1.,0.,0.,1.])
    a = matrix(data=[1.,2.,3,4.,5.,4.,6.,3,2.])
    #L = matrix(data=[1.,0.,0.,2.,1.,0.,3.,4.,1.])
    #U = matrix(data=[3.,4.,6.,0.,2.,9.,0.,0.,1.])
    #LU = matrix.combine_lu(L,U)
    #print "LU", LU
    #lup = (LU, lup[1])
    print "A", a
    lup = a.lup_decompose()
    print "LUP", lup
    a_i = lup[0].lup_invert(lup[1])
    print "A inverse", a_i
    print matrix.multiply_matrices(a,a_i)

    for a in [matrix(data=[1.,0.,0.,0.,  0.,4.,2.,0., -5.,0.,0.,1., 0.,0.,1.,0.]),
              matrix(data=[-1.,3.,4.,5.,  0.,4.,2.,1., -5.,5.,2.,-3., -4.,3.,2.,1.]),
              matrix(data=[-8.780454382560094, 4.24389067150205, 4.057661342681895, 1.1304208758453387, 0.2038639118735965, 6.330794706227703, -5.484817504274374, -0.16412212696591522, 25.412595302329905, 26.87675575660128, 20.381364036786152, 11.636150566231086, -13.519396156451739, -14.71734561903741, -9.402934211915941, -2.2477595541890696])
              ]:
        print
        print "4 by 4..."
        print "A",a
        lup = a.lup_decompose()
        print "LUP", lup
        L,U = lup[0].lu_split()
        print "U",U
        print "L",L
        LU=matrix.multiply_matrices(L,U)
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

if __name__ == '__main__':
    main()

