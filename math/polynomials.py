#!/usr/bin/env python
# PYTHONPATH=`pwd`/../python:$PYTHONPATH ./polynomials.py
from gjslib.graphics import drawing
from gjslib.math import polynomial, complex
import math

#a Documentation
"""
"""

#a Globals

#a Main
def main():
    size = 200
    size = size/2
    scale = 1.0/size
    scale *= 3.0
    color_by_direction = False
    #color_by_direction = True
    squash_by_modulus = False
    #squash_by_modulus = True
    differentiate = False
    #differentiate = True
    suffix = ""
    if differentiate: suffix="_d"
    d = drawing.draw_buffer(mode="RGB",size=(2*size+1,2*size+1))
    imaginary = complex.complex(imaginary=1)
    m_min, m_max, p = [0,2.2,polynomial.polynomial([1,0,2,1])]
    m_min, m_max, p = [0,2.2,polynomial.polynomial([1,0,imaginary*2,1])]
    m_min, m_max, p = [0,1.9,polynomial.polynomial([0,-0.1,imaginary*2,-imaginary,0,0.25,0.1,imaginary*0.02+0.01,imaginary*0.4])]
    if differentiate:
        p = p.differentiate()
        m_min, m_max = [0,3.5]
        m_min, m_max = [0,5.3]
    m_range = m_max-m_min
    new_min=1E9
    new_max=-1E9
    max_power = len(p.coeffs())
    for r in range(-size,size+1):
        x = complex.complex(real=r)*scale
        for i in range(-size,size+1):
            z = x+imaginary*i*scale
            fz = p.evaluate(z)
            (m,th) = fz.polar()
            if squash_by_modulus:
                m /= 1+pow(z.modulus(),max_power)
            new_min = min(m,new_min)
            new_max = max(m,new_max)
            m = (m-m_min)/m_range
            if color_by_direction:
                m = 0.3+m*0.7
                th = 0.5+th/math.pi
                th = 0.5*th
                d.putpixel(r+size,i+size,drawing.hsv(th,m,m))
                pass
            else:
                if (m<0):m=0
                if (m>1):m=1
                d.putpixel(r+size,i+size,drawing.hsv(m,1,1))
                pass
            pass
        pass
    print new_min, new_max
    if color_by_direction:
        d.save("polynomial%s_direction.png"%suffix)
        pass
    else:
        d.save("polynomial%s_modulus.png"%suffix)
        pass
    pass

if __name__ == '__main__':
    main()

