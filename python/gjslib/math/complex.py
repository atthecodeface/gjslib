#!/usr/bin/env python
import math
class complex(object):
    """
    A complex number class that provides +, -, *, /, and conjugate operations

    Infix variants are supported
    """
    #f __init__
    def __init__(self, real=None, imaginary=None, cartesian=None, polar=None):
        if real is not None:
            cartesian = (real, 0)
            pass
        if imaginary is not None:
            cartesian = (0,imaginary)
            pass
        if polar is not None:
            self._polar = (float(polar[0]), float(polar[1]))
            self._cartesian = None
            pass
        if cartesian is not None:
            self._cartesian = (float(cartesian[0]), float(cartesian[1]))
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
    #f pow - raise complex number to an integer/float power
    def pow(self,p):
        a = self.copy().to_polar()
        a._polar = (math.pow(a._polar[0],p), a._polar[1]*p)
        return a
    #f to_cartesian - convert to cartesian variant
    def to_cartesian(self):
        if self._cartesian is None:
            (r,theta) = self._polar
            self._cartesian = (r*math.cos(theta), r*math.sin(theta))
            self._polar = None
            pass
        return self
    #f real - return real value or None if imaginary coefficient exceeds epsilon
    def real(self, epsilon=1E-6):
        self.to_cartesian()
        (r,i) = self._cartesian
        if i<-epsilon or i>epsilon: return None
        return r
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
