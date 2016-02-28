#!/usr/bin/env python
# PYTHONPATH=`pwd`/../python:$PYTHONPATH ./mapping.py

#a Imports
import gjslib.graphics.obj
import gjslib.graphics.opengl
from gjslib.graphics import opengl_layer, opengl_widget

import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from gjslib.math.quaternion import c_quaternion
from gjslib.math import matrix, vectors, statistics
from image_point_mapping import c_point_mapping

#a c_edit_point_map_image
class c_edit_point_map_image(object):
    #f __init__
    def __init__(self, filename=None, image_name=None, epm=None, pm=None):
        self.filename = filename
        self.image_name = image_name
        self.texture = None
        self.object = None
        self.focus_object = None
        self.epm = epm
        self.point_mappings = pm
        self.center = (0.0,0.0)
        self.scale = (1.0,1.0)
        self.display_options = {}
        self.display_options["points"] = True
        self.display_options["focus"] = True
        self.display_options["focus_w"] = 0.01
        self.display_options["focus_h"] = 0.01
        pass
    #f set_focus
    def set_focus(self, focus=True):
        self.display_options["focus"] = focus
        pass
    #f focus_on_point
    def focus_on_point(self, pt_name):
        pt = self.point_mappings.get_xy(pt_name, self.image_name )
        if pt is None:
            self.center = (0,0)
            return
        self.center = (-pt[0],-pt[1])
        pass
    #f adjust
    def adjust(self, scale=(1.0,1.0), translate=(0.0,0.0), scaled=True ):
        if type(scale)==float:
            scale = (scale,scale)
            pass
        if scaled:
            translate = (translate[0]/self.scale[0], translate[1]/self.scale[1])
            pass
        self.center = (self.center[0] + translate[0],
                       self.center[1] + translate[1])
        self.scale = (self.scale[0]*scale[0], self.scale[1]*scale[1] )
        pass
    #f load_texture
    def load_texture(self):
        if (self.texture is None):
            self.texture = gjslib.graphics.opengl.texture_from_png(self.filename)
            pass
        if self.object is None:
            self.object = gjslib.graphics.obj.c_obj()
            self.object.add_rectangle( (-1.0,1.0,0.0), (2.0,0.0,0.0), (0.0,-2.0,0.0) )
            self.object.create_opengl_surface()
            pass
        if self.focus_object is None:
            self.focus_object = gjslib.graphics.obj.c_obj()
            fw = self.display_options["focus_w"]
            fh = self.display_options["focus_h"]
            self.focus_object.add_rectangle( (-1.0,-1.0,0.0), (2.0,0.0,0.0), (0.0,fh,0.0) )
            self.focus_object.add_rectangle( (-1.0,-1.0,0.0), (fw,0.0,0.0),  (0.0,2.0,0.0) )
            self.focus_object.add_rectangle(  (1.0,1.0,0.0),  (-2.0,0.0,0.0), (0.0,-fh,0.0) )
            self.focus_object.add_rectangle(  (1.0,1.0,0.0),  (-fw,0.0,0.0), (0.0,-2.0,0.0) )
            self.focus_object.create_opengl_surface()
            pass
        pass
    #f uniform_xy
    def uniform_xy(self, xy):
        """
        Return -1->1 xy for a view port xy 0->1
        """
        # Get xy in range -1 -> 1
        xy = (2.0*xy[0]-1.0, 2.0*xy[1]-1.0)
        xy = (xy[0]/self.scale[0], xy[1]/self.scale[1])
        xy = (xy[0]-self.center[0], xy[1]-self.center[1])
        return xy
    #f display
    def display(self):
        self.load_texture()
        if self.texture is None:
            return
        if self.display_options["focus"]:
            glMaterialfv(GL_FRONT,GL_DIFFUSE,[1.0,1.0,1.0,1.0])
            glMaterialfv(GL_FRONT,GL_AMBIENT,[1.0,1.0,1.0,1.0])
            glDisable(GL_TEXTURE_2D)
            self.focus_object.draw_opengl_surface()
            pass

        glPushMatrix()
        glScale(self.scale[0],self.scale[1],1.0)
        glTranslate(self.center[0],self.center[1],0.0)

        if self.display_options["points"]:
            c = self.epm.glow_colors[self.epm.glow_tick]
            glMaterialfv(GL_FRONT,GL_DIFFUSE,c)
            glMaterialfv(GL_FRONT,GL_AMBIENT,c)
            glDisable(GL_TEXTURE_2D)
            for m in self.epm.point_mapping_names:
                pt = self.point_mappings.get_xy(m, self.image_name )
                if pt is not None:
                    glPushMatrix()
                    glTranslate(pt[0],pt[1],-0.1)
                    sc = 0.01/self.scale[0]
                    if self.epm.point_mapping_names[self.epm.point_mapping_index]==m:
                        sc = sc*2
                        pass
                    glRotate(self.epm.tick,0.0,0.0,1.0)
                    glPushMatrix()
                    glScale(sc,4*sc,1.0)
                    glutSolidCube(1.0)
                    glPopMatrix()
                    glScale(4*sc,sc,1.0)
                    glutSolidCube(1.0)
                    glPopMatrix()
                    pass
                pass
            pass

        glMaterialfv(GL_FRONT,GL_DIFFUSE,[1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT,GL_AMBIENT,[1.0,1.0,1.0,1.0])
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.object.draw_opengl_surface()
        glPopMatrix()
        pass
    #f All done
    pass

#a c_edit_point_map_info
class c_edit_point_map_info(opengl_widget.c_opengl_container_widget):
    #f __init__
    def __init__(self, epm=None, pm=None, **kwargs):
        opengl_widget.c_opengl_container_widget.__init__(self, **kwargs)
        self.image_widget = opengl_widget.c_opengl_simple_text_widget(og=epm.og)
        self.mapping_widget = opengl_widget.c_opengl_simple_text_widget(og=epm.og)
        self.epm = epm
        self.point_mappings = pm
        self.add_widget(self.image_widget,  map_xywh=( (0.0,0.0,6000.0,4000.0), ( 0.0,1.0,2.0,-2*1.0) ) )
        self.add_widget(self.mapping_widget,map_xywh=( (0.0,0.0,6000.0,4000.0), (-1.0,1.0,2.0,-2*1.0) ) )
        pass
    #f update
    def update(self):
        import string
        image_list = self.point_mappings.get_images()
        image_list.sort()
        image_list = string.join(image_list,"\n")
        self.image_widget.replace_text(str(image_list), baseline_xy=(0.0,64.0), scale=(1.0,1.0))

        mapping_list = self.epm.point_mapping_names
        mapping_list.sort()
        mapping_list = string.join(mapping_list,"\n")
        self.mapping_widget.replace_text(mapping_list, baseline_xy=(0.0,64.0), scale=(1.0,1.0))
        pass
    #f All done
    pass

#a c_edit_point_map
class c_edit_point_map(object):
    glow_colors = []
    n = 10
    r = 0.5
    for i in range(3):
        for j in range(n):
            v = r*j/float(n)
            glow_colors.append((1-r+v, 1-v, r, 1-r+v, 1-v)[i:i+3])
            pass
        pass
    print glow_colors
    #f __init__
    def __init__(self, og):
        self.tick = 0
        self.og = og
        self.aspect = 1.0
        self.zNear=1.0
        self.zFar=40.0
        self.images = {}
        self.og.init_opengl()
        font_dir = "../../fonts/"
        self.og.load_font(font_dir+"cabin-bold")
        self.point_mappings = c_point_mapping()
        self.load_point_mapping("sidsussexbell.map")
        self.epm_info = c_edit_point_map_info(epm=self, pm=self.point_mappings)
        self.load_images()
        self.point_set_start_tick = None
        pass
    #f main_loop
    def main_loop(self):
        self.og.main_loop( display_callback=self.display,
                           keyboard_callback = self.keyboard_callback,
                           mouse_callback = self.mouse_callback,
                           menu_callback = self.menu_callback)
        pass
    #f load_point_mapping
    def load_point_mapping(self, point_map_filename):
        self.point_mappings.reset()
        self.point_mappings.load_data(point_map_filename)
        self.point_mapping_names = self.point_mappings.get_mapping_names()
        self.point_mapping_names.sort()
        self.point_mapping_index = 0
        pass
    #f load_images
    def load_images(self):
        image_names = self.point_mappings.get_images()
        for k in image_names:
            image_data = self.point_mappings.get_image(k)
            self.images[k] = c_edit_point_map_image(epm=self,
                                                    pm = self.point_mappings,
                                                    image_name=k,
                                                    filename=image_data["filename"])
            pass
        pass
    #f reset
    def reset(self):
        glutSetCursor(GLUT_CURSOR_CROSSHAIR)
        menus = self.og.build_menu_init()
        #gjslib.graphics.opengl.attach_menu("main_menu")
        self.og.build_menu_add_menu(menus,"images")
        image_keys = self.images.keys()
        for i in range(len(image_keys)):
            k = image_keys[i]
            self.og.build_menu_add_menu_item(menus,k,("image",k))
            pass
        self.og.build_menu_add_menu(menus,"main_menu")
        self.og.build_menu_add_menu_submenu(menus,"Images","images")
        print menus
        self.og.create_menus(menus)
        self.og.attach_menu("main_menu")

        self.epm_info.update()
        for i in self.images:
            self.images[i].camera = self.og.camera
            pass

        self.displayed_images = ["img_1", "img_2"]
        self.focus_image = 0
        self.layers = opengl_layer.c_opengl_layer_set()
        self.image_layers = (self.layers.new_layer( (0,500,500,500), depth=10),
                             self.layers.new_layer( (500,500,500,500), depth=10 ))
        self.info_layer = self.layers.new_layer( (0,0,1000,500), depth=1 )
        self.info_layer.add_contents(self.epm_info)

        for i in range(len(self.image_layers)):
            self.image_layers[i].add_contents(self.images[self.displayed_images[i]])
            self.images[self.displayed_images[i]].set_focus(False)
            pass
        self.images[self.displayed_images[self.focus_image]].set_focus(True)
        pass
    #f display_image_points
    def display_image_points(self):
        global faces
        for n in faces:
            f = faces[n]
            pts = []
            for pt in f:
                if pt in self.point_mappings.get_mapping_names():
                    pts.append(self.point_mappings.get_approx_position(pt))
                    pass
                pass
            if len(pts)>=3:
                i = 0
                j = len(pts)-1
                glBegin(GL_TRIANGLE_STRIP)
                while (j>=i):
                    glVertex3f(pts[i][0],pts[i][1],pts[i][2])
                    i += 1
                    if (i<=j):
                        glVertex3f(pts[j][0],pts[j][1],pts[j][2])
                        pass
                    j -= 1
                    pass
                glEnd()
                pass
            pass
        for n in self.point_mappings.get_mapping_names():
            (xyz) = self.point_mappings.get_approx_position(n)
            glPushMatrix()
            glMaterialfv(GL_FRONT,GL_AMBIENT,[1.0,0.3,0.3,1.0])
            glTranslate(xyz[0],xyz[1],xyz[2])
            glScale(0.03,0.03,0.03)
            glutSolidSphere(1,6,6)
            glPopMatrix()
            pass
        #for pt in ["clkcenter", "lspike", "rspike"]:
        for pt in ["rspike"]:
        #for pt in ["clkcenter", "lspike", "rspike", "belltl", "belltr"]:
            (r,g,b) = {"clkcenter":(1.0,0.3,1.0),
                   "rspike":(1.0,0.3,1.0),
                   "lspike":(1.0,0.3,1.0),
                   "belltl":(0.3,1.0,1.0),
                   "belltr":(0.3,1.0,1.0),}[pt]
            for k in self.image_projections:
                p = self.image_projections[k]
                xy = self.point_mappings.get_xy(pt, k)
                if xy is not None:
                    (p0,d0) = p.model_line_for_image(xy)
                    glMaterialfv(GL_FRONT,GL_AMBIENT,[r,g,b,1.0])
                    glLineWidth(2.0)
                    glBegin(GL_LINES);
                    glVertex3f(p0[0]+d0[0]*40.0,
                               p0[1]+d0[1]*40.0,
                               p0[2]+d0[2]*40.0)
                    glVertex3f(p0[0]-d0[0]*40.0,
                               p0[1]-d0[1]*40.0,
                               p0[2]-d0[2]*40.0)
                    glEnd()
                    pass
                pass
            pass
        pass
    #f display
    def display(self):
        self.tick += 1
        if self.point_set_start_tick is not None:
            if (self.tick - self.point_set_start_tick)==50:
                self.point_set_held()
                pass
            pass
        self.glow_tick = (self.tick/10) % len(self.glow_colors)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.og.camera["facing"] = c_quaternion.roll(self.og.camera["rpy"][0]).multiply(self.og.camera["facing"])
        self.og.camera["facing"] = c_quaternion.pitch(self.og.camera["rpy"][1]).multiply(self.og.camera["facing"])
        self.og.camera["facing"] = c_quaternion.yaw(self.og.camera["rpy"][2]).multiply(self.og.camera["facing"])
        self.layers.display()
        glutSwapBuffers()
        pass
    #f shift_focus
    def shift_focus(self, fwd=True, focus_image=None):
        self.images[self.displayed_images[self.focus_image]].set_focus(False)
        self.focus_image += 1
        if not fwd:
            self.focus_image += 2*len(self.displayed_images)-2
            pass
        if focus_image is not None:
            self.focus_image = focus_image
            pass
        self.focus_image = self.focus_image % len(self.displayed_images)
        self.images[self.displayed_images[self.focus_image]].set_focus(True)
        pass
    #f adjust_image
    def adjust_image(self,sxyg, scale=1.0):
        if sxyg[3]:
            for image_name in self.displayed_images:
                self.images[image_name].focus_on_point(self.point_mapping_names[self.point_mapping_index])
                pass
            pass
        scale_xy = (sxyg[0]*scale,sxyg[0]*scale)
        self.images[self.displayed_images[self.focus_image]].adjust(scale=scale_xy, translate=(scale*sxyg[1]/20,scale*sxyg[2]/20) )
        pass
    #f change_point
    def change_point(self, adjustment=None, point_name=None ):
        if adjustment is not None:
            l = len(self.point_mapping_names)
            self.point_mapping_index = (self.point_mapping_index + l + adjustment[0]) % l
            pass
        if point_name is not None:
            if point_name in self.point_mapping_names:
                self.point_mapping_index = self.point_mapping_names.index(point_name)
                pass
            pass
        self.adjust_image((1.0,0.0,0.0,1))
        pass
    #f point_set_start
    def point_set_start(self,image_name,xy,layer_xy,image_xy):
        self.point_set_start_tick = self.tick
        self.point_set_data = [False,image_name,xy,layer_xy,image_xy]
        pass
    #f point_set_held
    def point_set_held(self):
        self.point_set_data[0] = True
        pass
    #f point_set_end
    def point_set_end(self,image_name=None,xy=None,layer_xy=None,image_xy=None):
        if image_name is None:
            self.point_set_start_tick = None
        if self.point_set_start_tick is None:
            return
        if not self.point_set_data[0]:
            return
        if (self.point_set_data[1] != image_name):
            return
        pt_name = self.point_mapping_names[self.point_mapping_index]
        self.point_mappings.add_image_location(pt_name,image_name,image_xy,uniform=True,verbose=True)
        pass
    #f menu_callback
    def menu_callback(self, menu, value):
        if type(value)==tuple:
            if value[0]=="image":
                self.displayed_images[self.focus_image] = value[1]
                self.image_layers[self.focus_image].clear_contents()
                self.image_layers[self.focus_image].add_contents(self.images[value[1]])
                return True
            pass
        print menu, value
        return True
    #f keyboard_callback
    def keyboard_callback(self,k,m,x,y):
        sc = 1.0
        if (m & GLUT_ACTIVE_SHIFT): sc=4.0
        image_controls = {"D":(1.0,-sc,0.0,0),
                          "d":(1.0,-sc,0.0,0),
                          "a":(1.0,+sc,0.0,0),
                          "A":(1.0,+sc,0.0,0),
                          "w":(1.0,0.0,-sc,0),
                          "W":(1.0,0.0,-sc,0),
                          "s":(1.0,0.0,+sc,0),
                          "S":(1.0,0.0,+sc,0),
                          "=":(1.05*sc,0.0,0.0,0),
                          "+":(1.05*sc,0.0,0.0,0),
                          "-":(1/1.05/sc,0.0,0.0,0),
                          "_":(1/1.05/sc,0.0,0.0,0),
                          "g":(1.0,0.0,0.0,1),
                          }
        point_controls = {";":(-1,),
                          ".":(+1,),
                          }
        if ord(k)==27:
            self.point_set_end()
            return True
        if (k=='\t') or (ord(k)==25):
            fwd = True
            if (m & GLUT_ACTIVE_SHIFT): fwd=False
            self.shift_focus(fwd)
            return True
        if k in image_controls:
            self.adjust_image(image_controls[k])
            return True
        if k in point_controls:
            self.change_point(adjustment=point_controls[k])
            return True
        print ord(k),x,y
        pass
    #f mouse_callback
    def mouse_callback(self,b,s,m,x,y):
        xy = self.og.window_xy((x,y))
        layers = self.layers.find_layers_at_xy(xy)
        if len(layers)==0:
            self.point_set_end()
            return True
        l = layers[0]
        for i in range(len(self.image_layers)):
            if l==self.image_layers[i]:
                layer_xy = l.scaled_xy(xy)
                image_name = self.displayed_images[i]
                epmi = self.images[image_name]
                image_xy = epmi.uniform_xy(layer_xy)
                if (m & GLUT_ACTIVE_SHIFT) and (b=="left") and (s=="down"):
                    closest_pt = (1000000, None, None)
                    for p in self.point_mapping_names:
                        pt = self.point_mappings.get_xy(p, image_name)
                        if pt is not None:
                            dxy = (pt[0]-image_xy[0])*(pt[0]-image_xy[0]) + (pt[1]-image_xy[1])*(pt[1]-image_xy[1])
                            if dxy<closest_pt[0]:
                                closest_pt = (dxy, p, pt)
                                pass
                            pass
                        pass
                    if closest_pt[1] is not None:
                        self.shift_focus(focus_image=i)
                        self.change_point(point_name=closest_pt[1])
                        pass
                    self.point_set_end()
                    return True
                if (b=="left") and (s=="down"):
                    self.shift_focus(focus_image=i)
                    self.point_set_start(image_name,xy,layer_xy,image_xy)
                    return True
                if (b=="left") and (s=="up"):
                    self.point_set_end(image_name,xy,layer_xy,image_xy)
                    return True
                self.point_set_end()
                pass
            pass
        pass
    pass

#a Main
def main():
    og = gjslib.graphics.opengl.c_opengl(window_size = (1000,1000))
    m = c_edit_point_map(og)
    m.reset()
    m.main_loop()

if __name__ == '__main__':
    main()

