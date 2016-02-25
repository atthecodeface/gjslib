#a Imports
from gjslib.math import vectors, matrix

#a c_set_of_lines
class c_set_of_lines(object):
    def __init__(self):
        self.lines = []
        pass
    def add_line(self, pt, drn):
        drn = list(drn)
        matrix.normalize(drn)
        self.lines.append( (pt,drn) )
        pass
    def generate_meeting_points(self, too_close=0.0001):
        self.line_meetings = []
        self.posn = (0.0,0.0,0.0)
        for i in range(len(self.lines)):
            (p0,d0) = self.lines[i]
            for j in range(len(self.lines)):
                if (i>j):
                    (p1,d1) = self.lines[j]
                    meet = vectors.closest_meeting_of_two_lines(p0,d0,p1,d1,too_close)
                    self.line_meetings.append(meet)
                    pass
                pass
            pass
        if len(self.line_meetings)==0:
            return
        posn = (0.0,0.0,0.0)
        total_weight = 0
        for (c0,c1,dist,goodness) in self.line_meetings:
            weight = 1/(5.0+goodness)
            posn = vectors.vector_add(posn, c0, scale=0.5*weight)
            posn = vectors.vector_add(posn, c1, scale=0.5*weight)
            total_weight += weight
            #print c0,c1,weight,total_weight,posn
            pass
        #print posn, total_weight
        self.posn = vectors.vector_add((0.0,0.0,0.0), posn, scale=1/total_weight)
        pass

#a Top level
if __name__=="__main__":
    c = c_set_of_lines()
    c.add_line( (0.0,0.0,0.0), (0.0,0.0,1.0) )    
    c.add_line( (0.0,0.1,1.1), (1.0,0.0,1.0) )    
    c.generate_meeting_points()
    print c.line_meetings
