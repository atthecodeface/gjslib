#!/usr/bin/env python
import math
class complex(object):
    """
    A complex number class that provides +, -, *, /, and conjugate operations

    Infix variants are supported
    """
    #f __init__
    def __init__(self, real=None, imaginary=None, cartesian=None, polar=None):
        if cartesian is None:
            cartesian = (None,None)
        if real is not None:
            cartesian = (real, cartesian[0])
            pass
        if imaginary is not None:
            cartesian = (cartesian[0], imaginary)
            pass
        if polar is not None:
            cartesian = (None, None)
            self._polar = (float(polar[0]), float(polar[1]))
            self._cartesian = None
            pass
        if cartesian != (None,None):
            (a,b) = cartesian
            if a is None: a=0
            if b is None: b=0
            self._cartesian = (float(a), float(b))
            self._polar = None
            pass
        pass
    #f __add__ - infix add of complex with int/float/complex
    def __add__(self,a):
        s = self.copy()
        if type(a)==complex:
            s.add(a)
        else:
            s.add(other=complex(real=a))
        return s
    #f __sub__ - infix subtract of complex with int/float/complex
    def __sub__(self,a):
        s = self.copy()
        if type(a)==complex:
            s.add(a,scale=-1.0)
        else:
            s.add(other=complex(real=a),scale=-1.0)
        return s
    #f __mul__ - infix subtract of complex with int/float/complex
    def __mul__(self,a):
        s = self.copy()
        if type(a)==complex:
            s.multiply(a)
        else:
            s.multiply(other=complex(real=a))
        return s
    #f __div__ - infix division of complex by int/float/complex
    def __div__(self,a):
        s = self.copy().reciprocal()
        return (s*a).reciprocal()
    #f __neg__ - negation
    def __neg__(self):
        s = self.copy()
        return s.multiply(-1.0)
    #f __pow__ - power
    def __pow__(self,a):
        s = self.copy()
        return s.pow(a)
    #f __abs__ - absolute value, i.e. magnitude
    def __abs__(self):
        return self.modulus()
    #f __nonzero__ - return True if nonzero
    def __nonzero__(self):
        if self._polar is not None: return (self._polar[0]!=0)
        if self._cartesian[0]!=0: return True
        if self._cartesian[1]!=0: return True
        return False
    #f copy - return copy of the complex number
    def copy(self):
        return complex(cartesian=self._cartesian, polar=self._polar)
    #f cartesian
    def cartesian(self):
        self.to_cartesian()
        return self._cartesian
    #f polar
    def polar(self):
        self.to_polar()
        return self._polar
    #f add - add complex with other complex scaled
    def add(self, other, scale=1.0):
        self.to_cartesian()
        other.to_cartesian()
        self._cartesian = (self._cartesian[0]+scale*other._cartesian[0], self._cartesian[1]+scale*other._cartesian[1])
        return self
    #f multiply - multiply one complex number by another
    def multiply(self, other):
        if self._cartesian is not None and other._cartesian is not None:
            (r0,i0) = self._cartesian
            (r1,i1) = other._cartesian
            r = r0*r1 - i0*i1
            i = r0*i1 + r1*i0
            self._cartesian = (r,i)
            return self
        self.to_polar()
        other.to_polar()
        self._polar = (self._polar[0]*other._polar[0], self._polar[1]+other._polar[1])
        return self
    #f reciprocal - find the multiplicative inverse of self
    def reciprocal(self):
        c = self.copy()
        if c._cartesian is not None:
            (r,i) = c._cartesian
            m = r*r+i*i
            c._cartesian = (r/m,-i/m)
            return c
        c.to_polar()
        c._polar = (1.0/c._polar[0], -c._polar[1])
        return c
    #f modulus - calculate the absolute value
    def modulus(self):
        if self._polar is not None:
            return self._polar[0]
        (r,i) = self._cartesian
        return math.sqrt(r*r+i*i)
    #f conjugate - return conjugate of this object
    def conjugate(self):
        if self._cartesian is None:
            self.to_cartesian()
            pass
        return complex(cartesian = (self._cartesian[0], -self._cartesian[1]))
    #f to_polar - convert complex number to a polar representation
    def to_polar(self):
        if self._polar is None:
            (r,i) = self._cartesian
            self._polar = (self.modulus(), math.atan2(i,r))
            self._cartesian = None
            pass
        return self
    #f sqrt - square root the number
    def sqrt(self):
        a = self.copy().to_polar()
        a._polar = (math.sqrt(a._polar[0]), a._polar[1]/2)
        return a
    #f pow - raise complex number to a complex/integer/float power
    def pow(self,p):
        """
        Raises a complex number to the power 'p'

        If p=a+ib then x^(a+ib) = x^a.x^ib
        If x is expressed as Re^(i.theta) then x^a = R^a.e^(i.theta.a),
        i.e. for the real part 'a' of p we need a new polar of x with modulus R^a and angle a*theta
        Similarly, x^(ib) = R^(ib).(e^(i.theta)^(ib)) = R^(ib).e^(b.theta.(i^2)) = e^(ib.ln(R)).e^(-b.theta)
        Hence x^ib is a polar complex number of modululs e^(-b.theta) and angle b.ln(R)
        Finally, x^p is these two numbers multiplied together, i.e.
        modulus e^(-b.theta).R^a and angle a*theta+b.ln(R)
        """
        x = self.copy().to_polar()
        (R, theta) = x._polar
        if type(p)!=complex:
            p = complex(real=p)
            pass
        p = p.copy().to_cartesian()
        (a, b) = p._cartesian
        x._polar = (math.pow(R,a) / math.exp(b*theta),
                    theta*a + b*math.log(R))
        x = x.to_cartesian() # to ensure a consistent representation - otherwise theta could be outside the range -pi,pi
        return x
    #f to_cartesian - convert to cartesian variant
    def to_cartesian(self):
        if self._cartesian is None:
            (r,theta) = self._polar
            self._cartesian = (r*math.cos(theta), r*math.sin(theta))
            self._polar = None
            pass
        return self
    #f real - return real part of value
    def real(self):
        self.to_cartesian()
        return self._cartesian[0]
    #f imaginary - return imaginary part of value
    def imaginary(self):
        self.to_cartesian()
        return self._cartesian[1]
    #f __repr__ - return string representation
    def __repr__(self):
        if self._cartesian is not None:
            return "%6f + %6fi"%self._cartesian
        return "c(%6f, %6f)"%(self._polar[0], 180.0/3.14159265*self._polar[1])
    #f All done
    pass

def main():
    c = complex(cartesian=(2,3))
    print c*3+4 - 2 - complex(imaginary=2)
    print c*c / 2 + 0
    print c*c/c+0
    for (r,i) in [(1,0),(0,1),(1,1),(2,3),(4,5),(3,-1)]:
        c = complex(cartesian=(r,i))
        print (r,i), c/c/c*c.modulus()*c.modulus()+0
        print c/c

if __name__=="__main__":
    main()
