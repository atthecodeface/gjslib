#! /usr/bin/env python
##
## Copyright (C) 2016,  Gavin J Stark.  All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
import xml.dom.minidom

class base(object):
    def __init__(self):
        self.coords = None
        pass
    def bbox_max(self):
        

class node(base):
    def __init__(self, coords):
        base.__init__(self)
        self.coords = coords
        pass
    def svg_node_add(self, layout, parent):
        g_attr = {"id":"pc0",
                  "class":"node ctx_swap etc",
                  }
        link_attr = {("xlink", "href"): "ref",
                     ("xlink", "title"): "some title",
                     }
        poly_attr = {"fill":"#fffff0",
                     "stroke":"black",
                     "points":("%d,%d "*5)%(self.coords[0],self.coords[1],
                                            self.coords[0],self.coords[3],
                                            self.coords[2],self.coords[3],
                                            self.coords[2],self.coords[1],
                                            self.coords[0],self.coords[1], )
                     }
        xml = layout.svg_node_add(parent, "g", g_attr)
        link = layout.svg_node_add(xml, "a", link_attr)
        polygon = layout.svg_node_add(link, "polygon", poly_attr)
        #<text text-anchor="middle" x="651.216" y="-12747.1" font-family="Times,serif" font-size="14.00">PC0</text>
        pass

class edge(base):
    def __init__(self):
        base.__init__(self)
        self.points = []
        pass
    def points_str(self, blah):
        r = ""
        i = 0
        for p in self.points:
            r += "%s%d,%d"%(blah[i],p[0],p[1])
            i+=1
            pass
        return r
    def svg_node_add(self, layout, parent):
        g_attr = {"id":"pc0_pc1",
                  "class":"edge fall_through etc",
                  }
        path_attr = {"fill":"none",
                     "stroke":"black",
                     "d":self.points_str("M"+("C"*30))
                     }
        xml = layout.svg_node_add(parent, "g", g_attr)
        link = layout.svg_node_add(xml, "a", link_attr)
        path = layout.svg_node_add(xml, "path", path_attr)
        # <polygon fill="black" stroke="black" points="654.716,-11278.8 651.216,-11268.8 647.716,-11278.8 654.716,-11278.8"/>
        #<text text-anchor="middle" x="651.216" y="-12747.1" font-family="Times,serif" font-size="14.00">PC0</text>
        pass

class layout2D(object):
    """A single-layer 2D-layout graph consisting of nodes and edges
    Edges are directional, and hence are expected to have arrows at one end
    Each node may have additional properties
    """
    def __init__(self):
        self._nodes = []
        self._edges = []
        pass
    def add_node(self, node):
        self._nodes.append(node)
        pass
    def nodes(self):
        return self._nodes
    def edges(self):
        return self._edges
    def bbox(self):
        bbox = None
        for n in self._nodes:
            bbox = n.bbox_max()
            pass
        for e in self._edges:
            bbox = e.bbox_max()
            pass
        return bbox
    def svg_node_set_attributes(self, node, attributes):
        for (k,v) in attributes.iteritems():
            if type(k)!=tuple:
                k=(None,k)
                pass
            if k[0] is None:
                node.setAttribute(k[1],v)
                pass
            else:
                node.setAttributeNS(k[0],k[0]+":"+k[1],v)
                pass
            pass
        return node
    def svg_node_add(self, parent, node_type, attributes):
        xml = self.svg_doc.createElement(node_type)
        self.svg_node_set_attributes(xml, attributes)
        parent.appendChild(xml)
        return xml
    def to_svg(self):
        svg_attr = {"xmlns:xlink":"http://www.w3.org/1999/xlink",
                    "xmlns":"http://www.w3.org/2000/svg",
                    "width":"6991pt",
                    "height":"12858pt",
                    "viewBox":"0.00 0.00 6990.80 12858.05", }
        graph_attr = {"id":"graph0",
                      "class":"graph",
                      "transform":"scale(1 1) rotate(0) translate(4 12854)", # possibly add translate
                      }
        impl = xml.dom.minidom.getDOMImplementation()
        doctype = impl.createDocumentType("svg","-//W3C//DTD SVG 1.1//EN""", "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd")
        self.svg_doc = impl.createDocument("http://www.w3.org/2000/svg","svg", doctype)
        svg = self.svg_doc.getElementsByTagName("svg")[0]
        self.svg_node_set_attributes(svg, svg_attr)
        graph = self.svg_node_add(svg, "g", graph_attr)
        for n in self._nodes:
            n.svg_node_add(self,graph)
            pass
        for e in self._edges:
            e.svg_node_add(self,graph)
            pass
        return self.svg_doc

# Rebuild SVG as node (PCs for original CFs, {}[color] type, xywh) and arrows path+triangle
# We may get a request for a graph
# with 'exec start' of X
# with 'dont merge fallthroughs' of [pc]s
# with 'merge function calls' of [pcs]
# Export must provide for exported nodes having an ID with a list of PC ranges [(start, end inc),]
    
