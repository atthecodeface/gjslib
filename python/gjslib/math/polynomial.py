#!/usr/bin/env python
import math
import fractions

from complex import complex

#a Classes
#c quadratic
class quadratic(object):
    """
    Quadratic class, with solution - convenience really
    """
    #f __init__
    def __init__(self, a,b,c, notes=None):
        self._coeffs = (a+0.0, b+0.0, c+0.0)
        self._notes = notes
        pass
    #f coeffs
    def coeffs(self):
        return self._coeffs
    #f discriminant
    def discriminant(self):
        # Note use a*a*4 rather than 4*a*a so that if a is complex it still works
        (a,b,c) = self._coeffs
        return b*b/(a*a*4)-c/a
    #f find_all_roots
    def find_all_roots(self):
        """
        Find all roots of f(x)==0 as complex numbers
        """
        (a,b,c) = self._coeffs
        d = self.discriminant()
        if type(d)!=complex: d=complex(real=d)
        r = pow(d,0.5)
        return (r-b/(a*2), -r-b/(a*2))
    #f find_real_roots
    def find_real_roots(self,epsilon=1E-6):
        """
        Find real roots if coefficients are real
        """
        (a,b,c) = self._coeffs
        d = self.discriminant()
        if d<0:
            return []
        r = math.sqrt(d)
        return [-b/(2*a) + r, -b/(2*a) - r]
    #f __repr__
    def __repr__(self):
        r = "%6fx^2 + %6fx + %6f"%self._coeffs
        return r+str(self.notes)
    #f All done
    pass

#c cubic
class cubic(object):
    """
    Cubic class, with solution and number of real roots

    A cubic is f(x)= a.x^3 + b.x^2 + c.x + d
    Finding the root of a cubic is finding what value of x leads to f(x)=0.

    A depressed cubic for f(x)=0 has a=1, b=0 (i.e. y^3+C.y+D=0)
    A substitution of y=x+b/3a, hence x=y-b/3a, into the initial equation yields

    a.y^3 -a.3.b/3a.y^2 + 3.a.b*b/(9a.a).y - a.b*b*b/(27.a.a.a) +
          b.y^2 - b.2.b/3a.y + b.b.b/(9a.a) +
          cy - c.b/3a + d
    = a.y^3 -b.y^2 + b.b/3a.y   - b.b.b/(27.a.a) 
            +b.y^2 - 2.b.b/3a.y + b.b.b/(9.a.a) +
                            c.y - c.b/3a + d
    = a.y^3 + (c-b.b/3a).y - c.b/3a + d + 2b.b.b/(27.a.a) = 0

    Hence, 
    y^3 + (c/a-b.b/3a.a).y  - c/a.b/3a    + d/a + 2b.b.b/(27.a.a.a) = 0
    y^3 + (c/a-3(b/3a)^2).y - c/a.(b/3a) + d/a + 2(b/3a)^3 = 0

    Hence we have:
    C = c/a - 3.(b/3a)^2
    D = c/a . (b/3a) + d/a + 2.(b/3a)^3

    Cardano started with a depressed cubic
    y^3 + Cx + D = 0
    and substituted in y=u+v, hence y^3 = u^3 + v^3 + 3uv(u+v)

    u^3 + v^3 + 3uv(u+v) + C(u+v) + D = 0
    u^3 + v^3 + (u+v)(C+3uv) + D = 0

    Now, setting also uv = -C/3 we get:
    u^3 + v^3 + D = 0
    u^6 + v^3.u^3 + D.u^3 = 0

    But v=-C/3u, or v^3 = -C^3/27u^3, hence:
    u^6 + v^3.u^3 + D.u^3 = 0
    u^6 + D.u^3 - C^3/27 = 0

    If w = u^3, then w^2 + D.w - C^3/27 = 0
    and w = -D/2 +- sqrt( D^2/4 - C^3/27) (by the quadratic formula)
    Hence w can be found, hence u, hence v, hence y, hence x

    Note that if w = 0 then we must have C=0,
    and if C=0 we can go back as we have x^3 + D = 0,
    and hence X=cube_root(-D)
    """
    #f __init__
    def __init__(self, a,b,c,d, notes=None):
        self._coeffs = (a+0.0, b+0.0, c+0.0, d+0.0)
        self._notes = notes
        pass
    #f coeffs
    def coeffs(self):
        return self._coeffs
    #f discriminant
    def discriminant(self):
        (a,b,c,d) = self._coeffs
        return  ( a*b*c*d*18 + 
                  -b*b*b*d*4 + 
                  b*b*c*c +
                  -a*c*c*c*4 +
                  -a*a*d*d*27 )
    #f get_depressed_cubic
    def get_depressed_cubic(self):
        (a,b,c,d) = self._coeffs
        ba3 = b/(a*3)
        ca = c/a
        p = ca - ba3*ba3*3
        q = ba3*ba3*ba3*2 - ba3*ca + d/a
        if type(ba3)!=complex:
            ba3 = complex(real=ba3)
        return cubic(a=1, b=0, c=p, d=q, notes=(self, -ba3, "+y"))
    #f cardano_u3
    def cardano_u3(self):
        """
        """
        (a,b,c,d) = self._coeffs
        # a should be 1, b should be 0
        #print "a,b,c,d",(a,b,c,d)
        if type(d)!=complex:
            d = complex(real=d)
            pass
        #print d, -d/2
        #print d*d/4, c*c*c/27
        return (-d/2, d*d/4 + c*c*c/27)
    #f find_all_roots
    def find_all_roots(self):
        cube_root_1 = complex(polar=(1,math.pi*2/3))
        roots = []

        dc = self.get_depressed_cubic()
        #print dc
        (C,D) = dc._coeffs[2:]
        if not bool(C):
            for i in range(3):
                sel_cube_root_1 = pow(cube_root_1,i)
                x = complex(real=-D)*sel_cube_root_1+dc._notes[1]
                roots.append(x)
                pass
            return roots

        u3 = dc.cardano_u3()
        #print "u3",u3
        # u3 for one root is cubert(u3[0] + sqrt(u3[1]))
        s = pow(u3[1],0.5)
        #print "s",s
        u3 = u3[0] + s
        #print "should be zero", u3*u3 + u3*D - C*C*C/27
        for i in range(3):
            sel_cube_root_1 = pow(cube_root_1,i)
            u = pow(u3,1/3.0)*sel_cube_root_1
            if type(C)!=complex:
                C=complex(real=C)
                pass
            v = -C/(u*3.0)
            #print "u, v",u, v
            mu = u+v
            #print "mu",mu
            x = mu + dc._notes[1]
            #print "x", x
            roots.append(x)
            pass
        return roots
    #f find_real_roots
    def find_real_roots(self,epsilon=1E-6):
        roots = self.find_all_roots()
        real_roots = []
        for r in roots:
            if abs(r.cartesian()[1])<epsilon:
                real_roots.append(r.cartesian()[0])
            pass
        return real_roots
    #f num_real_roots
    def num_real_roots(self):
        d = self.discriminant()
        if d>=0:
            return 3
        return 1
    #f __repr__
    def __repr__(self):
        if (type(self._coeffs[0])==complex or
            type(self._coeffs[1])==complex or
            type(self._coeffs[2])==complex or
            type(self._coeffs[3])==complex):
            r = "%sx^3 + %sx^2 + %sx + %s"%(str(self._coeffs[0]),str(self._coeffs[1]),str(self._coeffs[2]),str(self._coeffs[3]))
            pass
        else:
            r = "%6fx^3 + %6fx^2 + %6fx + %6f"%self._coeffs
            pass
        return r+str(self._notes)

#c polynomial
class polynomial(object):
    """
    A polynomial class that supports real polynomial coefficients, with differentiation
    """
    #f __init__
    def __init__( self, coeffs=[0] ):
        self._coeffs=[]
        for c in coeffs:
            self._coeffs.append(c+0.0)
            pass
        self.normalize()
        pass
    #f __repr__
    def __repr__( self ):
        return str(self._coeffs)
    #f __add__ - infix add of complex with int/float/complex
    def __add__(self,a):
        return self.copy().add(a)
    #f __sub__ - infix subtract of complex with int/float/complex
    def __sub__(self,a):
        return self.copy().add(a,scale=-1)
    #f __mul__ - infix subtract of complex with int/float/complex
    def __mul__(self,a):
        return self.copy().multiply(a)
    #f __neg__ - negation
    def __neg__(self):
        return polynomial([-1.0]).multiply(self)
    #f is_constant
    def is_constant( self ):
        return len(self._coeffs)==1
    #f is_linear
    def is_linear( self ):
        return len(self._coeffs)==2
    #f coeff
    def coeff( self, n ):
        return self._coeffs[n]
    #f coeffs
    def coeffs(self):
        return self._coeffs
    # pretty
    def pretty(self, var):
        fmt = ""
        if len(self._coeffs)==0: return "0"
        result = ""
        needs_plus = False
        for i in range(len(self._coeffs)):
            if self._coeffs[i]==0:
                pass
            elif self._coeffs[i]==1:
                if needs_plus: result+=" + "
                if i==0: fmt="1"
                result+=fmt
                needs_plus = True
                pass
            elif (self._coeffs[i]>0):
                if needs_plus: result+=" + "
                result += str(self._coeffs[i])+fmt
                needs_plus = True
                pass
            else:
                if needs_plus: result+=" - "
                else: result+="-"
                if self._coeffs[i]==-1:
                    if i==0: fmt="1"
                    result += fmt
                else:
                    result += str(-self._coeffs[i])+fmt
                needs_plus = True
                pass
            if i==0:
                fmt = var
                pass
            else:
                fmt = var+("^%d"%(i+1))
                pass
            pass
        return result
    #f pretty_factors
    def pretty_factors( self, var ):
        result = ""
        factors = self.factorize()
        needs_mult = False
        for f in factors:
            if needs_mult:
                result += " * "
                pass
            result += "("+f.pretty(var)+")"
            needs_mult = True
            pass
        return result
    #f factorize
    def factorize( self ):
        import fractions
        factors = []
        poly = self
        while len(poly._coeffs)>1:
            for attempt in (0.01, -1.0, -5.0, -10.0, 1.0, 5.0, 10.0):
                x = poly.find_root(attempt)
                if x is not None:
                    x=x[0]
                    break
                pass
            if x is None:
                factors.append(poly)
                return factors
            f = fractions.Fraction(x).limit_denominator(1000)
            xx = float(f)
            p = polynomial([-f,1])
            p = polynomial([-x,1])
            factors.append(p)
            poly = poly.divide(p)[0]
            pass
        if len(poly._coeffs)==1:
            f = fractions.Fraction(poly.evaluate(0)).limit_denominator(1000)
            factors.append(polynomial([f]))
            pass
        return factors
    #f normalize
    def normalize( self ):
        """
        A normalized polynomial has its top coefficient non-zero

        The normalization process is to pop the top coefficient off while it is zero...
        """
        while (len(self._coeffs)>0) and (not bool(self._coeffs[-1])):
            self._coeffs.pop()
            pass
        return self
    #f add
    def add(self, other, scale=1):
        """
        Add a second polynomial to this polynomial
        """
        r = []
        sl = len(self._coeffs)
        ol = len(other._coeffs)
        for i in range(sl):
            if i>=ol:
                r.append(self._coeffs[i])
                pass
            else:
                r.append(self._coeffs[i]+scale*other._coeffs[i])
                pass
            pass
        for i in range(ol-sl):
            r.append(scale*other._coeffs[i+sl])
            pass
        self._coeffs = r
        return self.normalize()
    #f multiply
    def multiply( self, other ):
        r = []
        sl = len(self._coeffs)
        ol = len(other._coeffs)
        for i in range(sl):
            v = self._coeffs[i]
            n = i
            for j in range(ol):
                while n>=len(r): r.append(0)
                r[n] += v*other._coeffs[j]
                n+=1
                pass
            pass
        self._coeffs = r
        return self.normalize()
    #f differentiate
    def differentiate( self ):
        r = []
        sl = len(self._coeffs)
        for i in range(sl-1):
            r.append(self._coeffs[i+1]*(i+1))
            pass
        return polynomial(coeffs=r)
    #f evaluate
    def evaluate(self, x):
        v = None
        xn = 1
        sl = len(self._coeffs)
        for i in range(sl):
            nv = xn*self._coeffs[i]
            if v is None: v=nv
            else: v=nv+v
            xn = x*xn
            pass
        return v
    #f evaluate_poly
    def evaluate_poly( self, poly ):
        """
        self(n) = Sum( coeff[i].n^i )
        Apply to a polynomial 'poly'
        i.e. return self(poly)
        """
        result = c_polynomial()
        pn = c_polynomial(coeffs=[1])
        sl = len(self._coeffs)
        for i in range(sl):
            result = result.add( pn, scale=self._coeffs[i] )
            pn = pn.multiply(poly)
            pass
        return result
    #f find_root
    def find_root( self, attempt ):
        """
        Use newton-raphson...
        """
        epsilon = 0.000001
        df = self.differentiate()
        x1 = attempt
        for i in range(40):
            x0 = x1
            dx = df.evaluate(x0)
            #print x1, dx
            if dx==0:
                return None
            x1 = x0 - self.evaluate(x0)/dx
            pass
        if -epsilon<self.evaluate(x1)<epsilon:
            return (x1, x0)
        return None
    #f divide
    def divide( self, other ):
        sl = len(self._coeffs)
        remainder = self._coeffs[:]
        result = []
        ol = len(other._coeffs)
        for i in range(1+sl-ol):
            shift = sl-ol-i
            m = remainder[shift+ol-1]/other._coeffs[-1]
            result.append(m)
            for j in range(ol):
                remainder[shift+j] -= m * other._coeffs[j]
                pass
            #print remainder
            remainder.pop()
            pass
        result.reverse()
        return (polynomial(coeffs=result),polynomial(coeffs=remainder))

#f find_eqn            
def find_eqn( x ):
    epsilon = 0.00001
    tests = {}
    for i in range(30):
        tests["sqrt(%d)"%(i+2)]=math.sqrt(i+2)
        pass
    #tests = {"sqrt(21)":math.sqrt(21)}
    tests = {"sqrt(2)":math.sqrt(2)}
    def fred(x,a,b,n=100,approx=4):
        print x,a,b,n
        for i in range(n):
            if ((x-i*a)%b) < approx: return i,(x-i*a)/b
            pass
        (a,b)=(b,a)
        for i in range(n):
            if ((x-i*a)%b) < approx: return (x-i*a)/b,i
            pass
        return None
    def check( t, x, f, num, denom, mult=720 ):
        y = int(round(denom*x))
        r = fred(y*mult,num,denom,n=1000)
        #print r
        if r is not None:
            # int(x*denom)*mult = r[0]*num + r[1]*denom
            # So x*mult approx= r[0]*num/denom + r[1]
            # Or x = r[0]*num/denom/mult + r[1]/mult
            gr0 = fractions.gcd(r[0],mult)
            gr1 = fractions.gcd(r[1],mult)
            rr = ( (r[0]/gr0, mult/gr0), (r[1]/gr1,mult/gr1) )
            v = f*(0.+rr[0][0])/rr[0][1] + (0.+rr[1][0])/rr[1][1]
            if -epsilon<(x-v)<epsilon:
                print "%d/%d %s + %d/%d = %f (should be %f, diff %f)"%(rr[0][0],rr[0][1],t,rr[1][0],rr[1][1],v,x,x-v)
                pass
            pass
        pass
    for t,v in tests.iteritems():
        f = fractions.Fraction(v).limit_denominator(1000)
        check( t, x, f, num=f.numerator, denom=f.denominator )
        pass
    pass

#a Toplevel
def main():

    for coeffs in [ (1,-5,3,9),
                    (1,3,3,2),
                    (1,6,11,6),
                    (1,0,-1,0),
                    (1,2,3,4),
                    (5,4,3,2),
                    (1,0,0,0),
                    (-1,-2,-3,-4),
                    ]:
        print "-"*80
        c = cubic(coeffs[0], coeffs[1], coeffs[2], coeffs[3])
        print "Cubic", c
        print "Discriminant", c.discriminant()
        print "Should have %d real roots"%c.num_real_roots()
        dc = c.get_depressed_cubic()
        print "Depressed cubic version",dc
        print "All roots",c.find_all_roots()
        print "Real roots",c.find_real_roots()
        for x in c.find_real_roots():
            r = coeffs[0]*x*x*x + coeffs[1]*x*x + coeffs[2]*x + coeffs[3]
            print "Poly result",r 
            if (r<-1E-6) or (r>1E-6):
                raise Exception("Cubic solving failed")
            pass
        for c in c.find_all_roots():
            c3 = c.copy().pow(3.0)
            c2 = c.copy().pow(2.0)
            c3 = c3.multiply(complex(real=coeffs[0]))
            c2 = c2.multiply(complex(real=coeffs[1]))
            c  = c.multiply(complex(real=coeffs[2]))
            r = complex(real=coeffs[3]).add(c).add(c2).add(c3)
            print "Poly result",r
            r = r.real()
            if r is None or (r<-1E-6) or (r>1E-6):
                raise Exception("Cubic solving failed")
            pass
        pass

    a = polynomial( [1] )
    b = a.multiply( polynomial([0, 1]) )
    c = b.multiply( polynomial([1, 1]) )
    d = c.multiply( polynomial([2, 1]) )
    e = d.multiply( polynomial([3, 1]) )
    f = e.multiply( polynomial([4, 1]) )
    g = f.multiply( polynomial([5, 1]) )
    h = g.multiply( polynomial([6, 1]) )

    print a
    print b
    print c
    print d
    print e
    print f
    print g
    print h

    print a.differentiate(), b.differentiate(), c.differentiate()

    print d.divide(b)
    print f.divide(d)

    print f.pretty_factors('n')

    for i in range(10):
        print i, d.evaluate(i)

    x = polynomial([0,1])
    x_p_1 = polynomial([1,1])
    x_m_1 = polynomial([-1,1])
    print c.evaluate_poly(x_p_1).pretty("x")
    print c.evaluate_poly(x_m_1).pretty("x")

    d_i     = d.evaluate_poly(x)
    d_i_m_1 = d.evaluate_poly(x_m_1)
    d_diff = d_i.add(d_i_m_1,scale=-1)
    print "d_diff",d_diff.pretty("i"),"   OR   ",d_diff.pretty_factors("i")

    e_i     = e.evaluate_poly(x)
    e_i_m_1 = e.evaluate_poly(x_m_1)
    e_diff = e_i.add(e_i_m_1,scale=-1)
    print "e_diff",e_diff.pretty("i"),"   OR   ",e_diff.pretty_factors("i")


    sum_i_0 = polynomial([0,1])
    sum_i_1 = polynomial([0,1/2.0]).multiply(polynomial([1,1]))
    sum_i_2 = d.add(sum_i_1,scale=-3)
    #
    # sum_i_2 = polynomial d MINUS d_diff.coeff[1]*sum_i_1
    # and divide by d_diff.coeff[2]
    # sum_i_3 = polynomial e MINUS e_diff.coeff[1]*sum_i_1
    #                        MINUS e_diff.coeff[2]*sum_i_2
    # and divide by e_diff.coeff[3]
    # etc
    # Actually we can keep the sums as (divisor, sum_poly)

    print sum_i_0.pretty_factors('n')
    print sum_i_1.pretty_factors('n')
    print sum_i_2.pretty_factors('n')

    print sum_i_0.pretty('n')
    print sum_i_1.pretty('n')
    print sum_i_2.pretty('n')

    x = polynomial([-3,3,1])
    print x.pretty('n') ,"=", x.pretty_factors('n')

    x = polynomial([165.0,-55.0,18.0,-6.0,-3.0,1.0])
    print x.pretty('n') ,"=", x.pretty_factors('n')

    print "\nLooking for ",610/987.0
    find_eqn( 610/987.0 )
    print "\nLooking for ",1597/987.0
    find_eqn( 1597/987.0 )
    print "\nLooking for ",math.sqrt(2)+3
    find_eqn( math.sqrt(2)+3 )
    print "\nLooking for ",154/949.0
    find_eqn( 154/949.0 )
    print "\nLooking for ",91/919.0
    find_eqn( 91/919.0 )
    print "\nLooking for ",251/829.0
    find_eqn( 251/829.0 )
    print "\nLooking for ",436/551.0
    find_eqn( 436/551.0 )
    print "\nLooking for ",-1.5+math.sqrt(21)/2
    find_eqn( 0*-1.5+math.sqrt(21) )
    print "\nLooking for ",-2378/985.0
    find_eqn( -2378/985.0 )

if __name__=="__main__": main()
