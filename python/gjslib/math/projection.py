#!/usr/bin/env python
#a Imports
import math
from matrix import matrix
from quaternion import quaternion

#a projection
class projection(object):
    def __init__(self):
        pass

class camera(object):
    """
    Camera projection is from world to (-aspect_ratio*width/2,-width/2) to (aspect_ratio*width/2,width/2) such that
    the width*aspect_ratio is the horizontal field-of-view

        offset is 0.0 to 1.0 indicating center to right-hand edge of frame
        for an 'equidistant' lens projection the result is offset/focal_length
        offset*atan(frame_width/(2*focal_length))
        Stereographic angle=2*atan(offset/(2*focal_length))
        Equidistant/equiangular angle=offset/focal_length
        for rectilinear lenses there has to be a distortion applied
        See also http://michel.thoby.free.fr/Fisheye_history_short/Projections/Models_of_classical_projections.html
    """
    projections={}
    def __init__(self, width=1024.0, aspect_ratio=1.0, height=None, frame_width=36.0, focal_length=35.0, projection="rectilinear"):
        if height is None:
            height = float(width)/float(aspect_ratio)
            pass
        self.height = float(height)
        self.width = float(width)
        self.frame_width = float(frame_width)
        self.focal_length = float(focal_length)
        self.projection = projection
        pass
    def offset_to_angle(self, offset):
        """
        offset is 0.0 to 0.5 indicating center to right-hand edge of frame
        for an 'equidistant' lens projection the result is offset/focal_length
        Stereographic angle=2*atan(offset/(2*focal_length))
        Equidistant/equiangular angle=offset/focal_length
        Rectilinear angle = atan(offset,focal_length)
        See also http://michel.thoby.free.fr/Fisheye_history_short/Projections/Models_of_classical_projections.html

        May also need to have pincushion, barrel or mustache distortion removed
        """
        angle = offset*self.frame_width/self.focal_length
        if self.projection=="rectilinear":
            angle = math.atan2(offset*self.frame_width,self.focal_length)
        elif self.projection=="stereographic":
            angle = 2*math.atan2(offset*self.frame_width,2*self.focal_length)
        return angle
    def angle_to_offset(self, angle):
        """
        angle is in radians; it is the off-axis angle whose offset (on the x-axis of the image)
        we want to find
        """
        offset = angle*self.focal_length/self.frame_width
        if self.projection=="rectilinear":
            offset = self.focal_length*math.tan(angle)/self.frame_width
        elif self.projection=="stereographic":
            offset = 2*self.focal_length*math.tan(angle/2)/self.frame_width
        return offset
    def xy_to_roll_yaw(self, xy):
        r = math.sqrt(xy[0]*xy[0]+xy[1]*xy[1])
        roll = math.atan2(xy[1],xy[0])
        yaw = self.offset_to_angle(r/self.width)
        return (roll, yaw)
    def roll_yaw_to_xy(self, ry):
        r = self.width*self.angle_to_offset(ry[1])
        return (r*math.cos(ry[0]), r*math.sin(ry[0]))

src = camera(width=5184.0, height=3456.0, focal_length=20.0)
dst = camera(width=1024.0, height=1024.04, focal_length=100.0)
dst = camera(width=5184.0, height=3456.0, focal_length=20.0)

if False:
    print src.xy_to_roll_yaw((0,0))
    print src.xy_to_roll_yaw((2592,0))
    print src.xy_to_roll_yaw((0,1728))
    print src.roll_yaw_to_xy((math.radians(90),0.1))
    print src.roll_yaw_to_xy((math.radians(180),0.1))
    print src.roll_yaw_to_xy((math.radians(45),0.1))
    print src.roll_yaw_to_xy(src.xy_to_roll_yaw((100,200)))

# Want src_orientation and dst_orientation to be quaternions giving the center of the image
# Then I want to know src xy for any dst xy
# Note that dst xy is (roll,yaw)=dst.xy_to_roll_yaw(xy)
# How about we want to know the (x,y,z) of dst xy.
# This should be something like dst_orientation*roll(yaw(dst.xy_to_roll_yaw(xy))) applied to (0,0,1)
# Then we can apply src_orientation' to this to get an (x,y,z) relative to the source
# This has to be converted to a roll,yaw, then to an (x,y)

def conjugation(q,p):
    qc = q.copy().conjugate()
    print p[0], p[1], p[2]
    pq = quaternion(r=0,i=p[0],j=p[1],k=p[2])
    r = q*pq*qc
    print r
    return r.get()[1:]

# Orientation assumes that the camera axis is the z-axis with x-axis up, and orientation is applied to that
dst_orientation = quaternion.yaw(-60,degrees=True) * quaternion.pitch(-30,degrees=True)
src_orientation = quaternion.yaw(-60,degrees=True) * quaternion.pitch(-30,degrees=True)
#dst_orientation = quaternion.of_spherical_polar(0,10,degrees=True) # looking at 10 degrees 'to the right'
#src_orientation = quaternion.of_spherical_polar(0,0,degrees=True)  # looking straight on
xy=(100.0,0) # 100 pixels to the right of center out of 512.0 to the right of center - i.e. center+20%
xy=(0,100.0) # 100 pixels above the center out of 512.0
dst_ry = dst.xy_to_roll_yaw(xy)
print dst_ry
q = dst_orientation * quaternion.roll(dst_ry[0]) * quaternion.yaw(dst_ry[1])
q.repr_fmt = "euler"
print q
q = src_orientation.copy().conjugate() * q
print q
mapped_xyz = conjugation(q,(0,0,1))
print mapped_xyz
yaw = math.acos(mapped_xyz[2])
roll = math.atan2(mapped_xyz[0], mapped_xyz[1]) # [0],[1] because X is up in quaternion universe
src_ry = (-roll,-yaw) # - because we are inverting the transformation
print src_ry
print src.roll_yaw_to_xy(src_ry)

#q=quaternion.roll(30,degrees=True)
#q=quaternion.pitch(30,degrees=True) * quaternion.roll(30,degrees=True)
#q=quaternion.pitch(30,degrees=True)
#conjugation(q,(0,0,1))
