#!/usr/bin/env python
#a Imports
import math
from matrix import matrix

#a quaternion
class quaternion( object ):
    # +y to right, +x up, +z in front
    # roll + = roll clkwise inside looking forward
    # pitch + = nose up inside looking forward
    # yaw + = nose left inside looking forward
    # when given roll, pitch, yaw the order applies is roll(pitch(yaw())) - i.e. yaw is applied first
    fmt = "%7.4f"
    default_fmt = "euler"
    default_fmt = "quat"
    #f classmethod identity - return identity quarternion
    @classmethod
    def identity( cls ):
        return cls()
    #f classmethod pitch
    @classmethod
    def pitch( cls, angle, degrees=False ):
        return cls().from_euler( pitch=angle, degrees=degrees )
    #f classmethod yaw
    @classmethod
    def yaw( cls, angle, degrees=False ):
        return cls().from_euler( yaw=angle, degrees=degrees )
    #f classmethod roll
    @classmethod
    def roll( cls, angle, degrees=False ):
        return cls().from_euler( roll=angle, degrees=degrees )
    #f classmethod from_sequence
    @classmethod
    def from_sequence( cls, rotations, degrees=False ):
        q = cls()
        for (t,n) in rotations:
            r = {"roll":cls.roll, "pitch":cls.pitch, "yaw":cls.yaw}[t](n,degrees=degrees)
            q = r.multiply(q)
            pass
        return q
    #f classmethod of_euler
    @classmethod
    def of_euler( cls, roll=0, pitch=0, yaw=0, rpy=None, degrees=False ):
        return cls().from_euler( rpy=rpy, roll=roll, pitch=pitch, yaw=yaw, degrees=degrees )
    #f classmethod of_rotation
    @classmethod
    def of_rotation( cls, angle, axis, degrees=False ):
        return cls().from_rotation( angle=angle, axis=axis, degrees=degrees )
    #f __init__
    def __init__( self, quat=None, euler=None, degrees=False, r=1, i=0, j=0, k=0, repr_fmt=None ):
        self.quat = {"r":float(r), "i":float(i), "j":float(j), "k":float(k)}
        self.matrix = None
        if repr_fmt is None:
            repr_fmt = self.default_fmt
        self.repr_fmt = repr_fmt
        if quat is not None:
            self.quat["r"] = quat["r"]
            self.quat["i"] = quat["i"]
            self.quat["j"] = quat["j"]
            self.quat["k"] = quat["k"]
            pass
        if euler is not None:
            self.from_euler(roll=euler[0], pitch=euler[1], yaw=euler[2], degrees=degrees)
            pass
        pass
    #f copy
    def copy(self):
        return quaternion(quat=self.quat)
    #f __repr__
    def __repr__( self ):
        if self.repr_fmt=="euler":
            result = ("quaternion(euler=("+self.fmt+","+self.fmt+","+self.fmt+"),degrees=True)") % self.to_euler(degrees=True)
            return result
        elif self.repr_fmt=="euler_mod":
            result = ("quaternion(euler=("+self.fmt+","+self.fmt+","+self.fmt+"),length="+self.fmt+",degrees=True)") % self.to_euler(degrees=True,include_modulus=True)
            return result
        result = ("quaternion({'r':"+self.fmt+", 'i':"+self.fmt+", 'j':"+self.fmt+", 'k':"+self.fmt+"})") % (self.quat["r"],
                                                                                       self.quat["i"],
                                                                                       self.quat["j"],
                                                                                       self.quat["k"] )
        return result
    #f __add__ - infix add of quaternion with int/float/quaternion
    def __add__(self,a):
        s = self.copy()
        if type(a)==quaternion:
            s.add(a)
        else:
            s.add(other=quaternion(r=a))
        return s
    #f __sub__ - infix subtract of quaternion with int/float/quaternion
    def __sub__(self,a):
        s = self.copy()
        if type(a)==quaternion:
            s.add(a, scale=-1.0)
        else:
            s.add(other=quaternion(r=a), scale=-1.0)
        return s
    #f __mul__ - infix subtract of quaternion with int/float/quaternion
    def __mul__(self,a):
        s = self.copy()
        if type(a)==quaternion:
            s.multiply(a)
        else:
            s.multiply(other=quaternion(r=a))
        return s
    #f __div__ - infix division of quaternion by int/float/quaternion
    def __div__(self,a):
        s = self.copy().reciprocal()
        return (s*a).reciprocal()
    #f __neg__ - negation
    def __neg__(self):
        s = self.copy()
        return s.scale(-1.0)
    #f __abs__ - absolute value, i.e. magnitude
    def __abs__(self):
        return self.modulus()
    #f __nonzero__ - return True if nonzero
    def __nonzero__(self):
        if self.quat["r"]!=0: return True
        if self.quat["i"]!=0: return True
        if self.quat["j"]!=0: return True
        if self.quat["k"]!=0: return True
        return False
    #f get
    def get( self ):
        return (self.quat["r"],
                self.quat["i"],
                self.quat["j"],
                self.quat["k"],
                )
    #f get_matrix_values
    def get_matrix_values( self ):
        if self.matrix is None: self.create_matrix()
        return self.matrix
    #f get_matrix
    def get_matrix( self, order=3 ):
        m = self.get_matrix()
        if order==3:
            return c_matrixNxN(data=(m[0][0], m[0][1], m[0][2],
                                     m[1][0], m[1][1], m[1][2],
                                     m[2][0], m[2][1], m[2][2],))
        if order==4:
            return c_matrixNxN(data=(m[0][0], m[0][1], m[0][2], 0.0,
                                     m[1][0], m[1][1], m[1][2], 0.0,
                                     m[2][0], m[2][1], m[2][2], 0.0,
                                     0.0,0.0,0.0,1.0))
        raise Exception("Get matrix of unsupported order")
    #f create_matrix
    def create_matrix( self ):
        # From http://www.gamasutra.com/view/feature/131686/rotating_objects_using_quaternions.php?page=2
        # calculate coefficients
        l = self.modulus()

        x2 = self.quat["i"] + self.quat["i"]
        y2 = self.quat["j"] + self.quat["j"] 
        z2 = self.quat["k"] + self.quat["k"]
        xx = self.quat["i"] * x2
        xy = self.quat["i"] * y2
        xz = self.quat["i"] * z2
        yy = self.quat["j"] * y2
        yz = self.quat["j"] * z2
        zz = self.quat["k"] * z2
        wx = self.quat["r"] * x2
        wy = self.quat["r"] * y2
        wz = self.quat["r"] * z2
        m = [[0,0,0,0.],[0,0,0,0.],[0,0,0,0.],[0.,0.,0.,1.]]

        m[0][0] = l - (yy + zz)/l
        m[1][0] = (xy - wz)/l
        m[2][0] = (xz + wy)/l

        m[0][1] = (xy + wz)/l
        m[1][1] = l - (xx + zz)/l
        m[2][1] = (yz - wx)/l

        m[0][2] = (xz - wy)/l
        m[1][2] = (yz + wx)/l
        m[2][2] = l - (xx + yy)/l

        self.matrix = m
        pass
    #f from_euler
    def from_euler( self, rpy=None, pitch=0, yaw=0, roll=0, modulus=None, degrees=False ):
        """
        Euler angles are roll, pitch and yaw. (Z, Y then X axis rotations)

        The yaw is done in the middle

        Roll is around Z
        Pitch is around Y
        Yaw is around X
        """
        if rpy is not None:
            if len(rpy)==4:
                (roll, pitch, yaw, modulus) = rpy
            else:
                (roll, pitch, yaw) = rpy
            pass
        if modulus is None:
            modulus = 1.0
        if degrees:
            roll  = 3.14159265/180.0 * roll
            pitch = 3.14159265/180.0 * pitch
            yaw   = 3.14159265/180.0 * yaw
            pass

        (pitch,yaw)=(yaw,pitch)
        cr = math.cos(roll/2)
        cp = math.cos(pitch/2)
        cy = math.cos(yaw/2)
        sr = math.sin(roll/2)
        sp = math.sin(pitch/2)
        sy = math.sin(yaw/2)

        crcy = cr * cy
        srsy = sr * sy
        self.quat["r"] = cp * crcy + sp * srsy
        self.quat["i"] = sp * crcy - cp * srsy
        self.quat["j"] = cp * cr * sy + sp * sr * cy
        self.quat["k"] = cp * sr * cy - sp * cr * sy
        self.scale(modulus)
        self.matrix = None
        return self
    #f to_euler
    def to_euler( self, include_modulus=False, degrees=False ):
        """
        Euler angles are roll, pitch and yaw.
        The rotations are performed in the order 
        """
        r = self.quat["r"]
        i = self.quat["i"]
        j = self.quat["j"]
        k = self.quat["k"]
        l = math.sqrt(r*r+i*i+j*j+k*k)
        if (l>1E-9):
            r=r/l
            i=i/l
            j=j/l
            k=k/l
            pass
        yaw   = math.atan2(2*(r*i+j*k), 1-2*(i*i+j*j))
        if 2*(r*j-i*k)<-1 or 2*(r*j-i*k)>1:
            pitch = math.asin( 1.0 )
            pass
        else:
            pitch = math.asin( 2*(r*j-i*k))
            pass
        roll  = math.atan2(2*(r*k+i*j), 1-2*(j*j+k*k))
        if degrees:
            roll  = 180.0/3.14159265 * roll
            pitch = 180.0/3.14159265 * pitch
            yaw   = 180.0/3.14159265 * yaw
            pass
        if include_modulus:
            return (roll, pitch, yaw, self.modulus())
        return (roll, pitch, yaw)
    #f from_matrix
    def from_matrix( self, matrix, epsilon=1E-6 ):
        """
        """
        d = matrix.determinant()
        if (d>-epsilon) and (d<epsilon):
            raise Exception("Singular matrix supplied")
        m = matrix.copy()
        if d<0: d=-d
        m.scale(1.0/math.pow(d,1/3.0))

        yaw   = math.atan2(m[1,2],m[2,2])
        roll  = math.atan2(m[0,1],m[0,0])
        if m[0,2]<-1 or m[0,2]>1:
            pitch=-math.asin(1)
        else:
            pitch = -math.asin(m[0,2])
        q0 = quaternion.of_euler(roll=roll, pitch=pitch, yaw=yaw, degrees=False)

        yaw   = math.atan2(m[2,1],m[2,2])
        roll  = math.atan2(m[1,0],m[0,0])
        if m[2,0]<-1 or m[2,0]>1:
            pitch=-math.asin(1)
        else:
            pitch = -math.asin(m[2,0])
        q1 = quaternion.of_euler(roll=roll, pitch=pitch, yaw=yaw, degrees=False)
        self.quat["r"] = (q0.quat["r"] + q1.quat["r"])/2.0
        self.quat["i"] = (q0.quat["i"] - q1.quat["i"])/2.0
        self.quat["j"] = (q0.quat["j"] - q1.quat["j"])/2.0
        self.quat["k"] = (q0.quat["k"] - q1.quat["k"])/2.0
        self.normalize()
        self.matrix = None
        return self
    #f from_rotation
    def from_rotation(self, angle, axis, degrees=False):
        """
        """
        if degrees:
            angle  = math.radians(angle)
            pass
        s = math.sin(angle/2)
        c = math.cos(angle/2)
        self.quat["r"] = c
        self.quat["i"] = s*axis[0]
        self.quat["j"] = s*axis[1]
        self.quat["k"] = s*axis[2]
        self.matrix = None
        return self
    #f to_rotation
    def to_rotation(self, degrees=False):
        """
        """
        m = self.modulus()
        angle = 2*math.acos(self.quat["r"]/m)
        sm = m*math.sin(angle/2)
        axis = (self.quat["i"]/sm,
                self.quat["j"]/sm,
                self.quat["k"]/sm)
        if degrees:
            angle  = math.degrees(angle)
            pass
        return (angle, axis)
    #f conjugate
    def conjugate( self ):
        self.quat["i"] = -self.quat["i"]
        self.quat["j"] = -self.quat["j"]
        self.quat["k"] = -self.quat["k"]
        self.matrix = None
        return self
    #f reciprocal
    def reciprocal( self ):
        self.conjugate()
        self.scale(1.0/self.modulus_squared())
        return self
    #f invert_rotation
    def invert_rotation( self ):
        self.reciprocal()
        return self
    #f modulus_squared
    def modulus_squared( self ):
        r = self.quat["r"]
        i = self.quat["i"]
        j = self.quat["j"]
        k = self.quat["k"]
        return (r*r+i*i+j*j+k*k)
    #f modulus
    def modulus( self ):
        return math.sqrt(self.modulus_squared())
    #f add
    def add( self, other, scale=1.0 ):
        self.quat["r"] += other.quat["r"] *scale
        self.quat["i"] += other.quat["i"] *scale
        self.quat["j"] += other.quat["j"] *scale
        self.quat["k"] += other.quat["k"] *scale
        self.matrix = None
        return self
    #f scale
    def scale( self, scale ):
        self.quat["r"] *= scale
        self.quat["i"] *= scale
        self.quat["j"] *= scale
        self.quat["k"] *= scale
        self.matrix = None
        return self
    #f normalize
    def normalize( self, epsilon=1E-9 ):
        l = self.modulus()
        if (l>-epsilon) and (l<epsilon):
            return self
        return self.scale(1.0/l)
    #f multiply
    def multiply( self, other ):
        (r1,i1,j1,k1) = self.quat["r"],self.quat["i"],self.quat["j"],self.quat["k"]
        (r2,i2,j2,k2) = other.quat["r"],other.quat["i"],other.quat["j"],other.quat["k"]
        r = r1*r2 - i1*i2 - j1*j2 - k1*k2
        i = r1*i2 + i1*r2 + j1*k2 - k1*j2
        j = r1*j2 + j1*r2 + k1*i2 - i1*k2
        k = r1*k2 + k1*r2 + i1*j2 - j1*i2
        self.quat={"r":r, "i":i, "j":j, "k":k }
        return self
    #f rotation_multiply
    def rotation_multiply( self, other ):
        A = (self.quat["r"] + self.quat["i"])*(other.quat["r"] + other.quat["i"])
        B = (self.quat["k"] - self.quat["j"])*(other.quat["j"] - other.quat["k"])
        C = (self.quat["r"] - self.quat["i"])*(other.quat["j"] + other.quat["k"]) 
        D = (self.quat["j"] + self.quat["k"])*(other.quat["r"] - other.quat["i"])
        E = (self.quat["i"] + self.quat["k"])*(other.quat["i"] + other.quat["j"])
        F = (self.quat["i"] - self.quat["k"])*(other.quat["i"] - other.quat["j"])
        G = (self.quat["r"] + self.quat["j"])*(other.quat["r"] - other.quat["k"])
        H = (self.quat["r"] - self.quat["j"])*(other.quat["r"] + other.quat["k"])
        r = B + (-E - F + G + H) /2
        i = A - (E + F + G + H)/2 
        j = C + (E - F + G - H)/2 
        k = D + (E - F - G + H)/2
        return quaternion( quat={"r":r, "i":i, "j":j, "k":k } )
    #f interpolate
    def interpolate( self, other, t ):
        cosom = ( self.quat["i"] * other.quat["i"] +
                  self.quat["j"] * other.quat["j"] +
                  self.quat["k"] * other.quat["k"] +
                  self.quat["r"] * other.quat["r"] )
        abs_cosom = cosom
        sgn_cosom = 1
        if (cosom <0.0): 
            abs_cosom = -cosom
            sgn_cosom = -1
            pass

        # calculate coefficients
        if ( (1.0-abs_cosom) > epsilon ):
            #  standard case (slerp)
            omega = math.acos(abs_cosom);
            sinom = math.sin(omega);
            scale0 = math.sin((1.0 - t) * omega) / sinom;
            scale1 = math.sin(t * omega) / sinom;
            pass
        else:
            # "from" and "to" quaternions are very close 
            #  ... so we can do a linear interpolation
            scale0 = 1.0 - t;
            scale1 = t;
            pass

        # calculate final values
        i = scale0 * self.quat["i"] + scale1 * sgn_cosom * other.quat["i"]
        j = scale0 * self.quat["j"] + scale1 * sgn_cosom * other.quat["j"]
        k = scale0 * self.quat["k"] + scale1 * sgn_cosom * other.quat["k"]
        r = scale0 * self.quat["r"] + scale1 * sgn_cosom * other.quat["r"]
        return quaternion( quat={"r":r, "i":i, "j":j, "k":k } )

