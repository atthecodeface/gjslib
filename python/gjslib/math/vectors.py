#a Imports
import math

#f Useful functions
#f _mklist
def _mklist(scale):
    """
    Internal function that converts a 'scale' argument to a tuple or list of scales

    @scale:    Argument to ensure it is a list

    In function calls that take a scale argument it can be provided as a vector or a single item.
    This function ensures that the scale argument is a list 
    """
    if type(scale)==tuple: return scale
    if type(scale)==list: return scale
    return [scale]

#f vector_scale
def vector_scale(v, scale=1.0):
    """
    Scale a vector; if scale is a list or tuple, then the elements of the vector are scaled
    by the respective elements of scale, otherwise all the elements are scaled by the single scale factor
    Returns a vector as a list

    @v:       Vector to scale
    @scale:   Scaling amount - list, tuple or int/float
    """
    scale = _mklist(scale)
    ls = len(scale)
    d = []
    for i in range(len(v)):
        d.append(v[i]*scale[i%ls])
        pass
    return d

#f vector_dot_product
def vector_dot_product(a, b):
    """
    Calculate the inner product (vector dot product) of two vectors
    Returns a scalar

    @a:       First vector
    @b:       Second vector
    """
    r = 0
    for i in range(len(a)):
        r += a[i]*b[i]
        pass
    return r

#f vector_squared
def vector_squared(v):
    """
    Calculate the length squared of a vector (v.v)
    Returns a scalar
    
    @v:       Vector whose length should be calculated
    """
    return vector_dot_product(v,v)

#f vector_length
def vector_length(v):
    """
    Calculate the length of a vector (sqrt[v.v])
    
    @v:       Vector whose length should be calculated
    """
    return math.sqrt(vector_dot_product(v,v))

#f vector_normalize
def vector_normalize(v, epsilon=1E-8):
    """
    Normalize a vector - turn it into a unit vector
    If the vector length is less epsilon then the vector is not touched (to avoid div by zero)
    Returns a vector as a list
    
    @v:       Vector to normalize
    @epsilon: Maximum length of vector to leave untouched
    """
    d = math.sqrt(vector_dot_product(v,v))
    if d<epsilon: d=1
    return vector_scale(v,1.0/d)

#f vector_separation
def vector_separation(a,b):
    """
    Determine the separation (distance between) two vectors
    Returns a float
    
    @a:       First vector
    @b:       Second vector
    """
    d = vector_add(a,b,scale=-1.0)
    return math.sqrt(vector_dot_product(d,d))

#f vector_min
def vector_min(a, b):
    """
    Calculate the vector whose coordinates are the individual minimums of the two arguments
    If an 'a' coordinate is given as 'None' then the coordinate from 'b' is used
    Returns a vector as a list

    @a:       First vector - may contain 'None' as coordinates
    @b:       Second vector

    This function can be used to find the minimum bounding box of sets of vectors, for example
    """
    r = []
    for i in range(len(a)):
        if a[i] is None:
            r.append(b[i])
            pass
        else:
            r.append(min(a[i],b[i]))
        pass
    return r

#f vector_max
def vector_max(a, b):
    """
    Calculate the vector whose coordinates are the individual maximums of the two arguments
    If an 'a' coordinate is given as 'None' then the coordinate from 'b' is used
    Returns a vector as a list

    @a:       First vector - may contain 'None' as coordinates
    @b:       Second vector

    This function can be used to find the maximum bounding box of sets of vectors, for example
    """
    r = []
    for i in range(len(a)):
        if a[i] is None:
            r.append(b[i])
            pass
        else:
            r.append(max(a[i],b[i]))
        pass
    return r

#f vector_add
def vector_add(a,b,scale=1.0):
    """
    Add two vectors, scaling the second vector by scale.
    For example, if scale is -1 then the result is the difference between the two vectors
    Returns a vector as a list

    @a:       First vector
    @b:       Second vector
    @scale:   Scaling factor to be applied to second vector prior to addition
    """
    scale = _mklist(scale)
    ls = len(scale)
    d = []
    for i in range(len(a)):
        d.append(a[i]+b[i]*scale[i%ls])
        pass
    return d

#f vector_cos_angle_between
def vector_cos_angle_between(a,b, epsilon=1E-16):
    """
    Calculate the cosine of the angle between two vectors
    If the vectors combine in length (through multiplication) to be less than 'epsilon', then
    approximately zero will be returned (actually just the dot product of a and b)
    Returns a float between -1 and 1

    @a:       First vector
    @b:       Second vector
    @scale:   Scaling factor to be applied to second vector prior to addition
    """
    l = vector_length(a) * vector_length(b)
    if l<epsilon: return 1.0
    return vector_dot_product(a,b)/l

#f vector_cross_product
def vector_cross_product(vs):
    """
    Cross product a list/tuple of vectors
    One fewer vector than the dimension is required
    The resultant vector is 'right-handed' normal to the input vectors and
    of length equal to the length/area/volume/hypervolume etc of the poly
    defined by the input vectors
    Returns a vector of same dimension as the input vectors

    @vs:   List of N-1 vectors of dimension N each
    """
    d = len(vs[0])
    if len(vs)!=(d-1):
        raise Exception("Cross product requires N-1 vectors of dimension N")
    res = []
    for i in range(d):
        s = 1
        if (i&1):s=-1
        def determinant(vs,index,use_cols,pop_index,rank=d):
            if len(use_cols)==2:
                return vs[index][use_cols[1-pop_index]]
            cols = use_cols[:]
            cols.pop(pop_index)
            #print "Here", vs, index, cols
            sum = 0
            s = 1
            for j in range(d-index-1):
                sum += s*vs[index][cols[j]]*determinant(vs,index+1,cols,j)
                s = -s
                pass
            #print vs, index,sum
            return sum
        cols=range(d)
        res.append(s * determinant(vs,0,cols,i))
        pass
    return res

#f vector_point_on_plane
def vector_point_on_plane(p0,p1,p2,k01,k02):
    """
    Return the coordinates of the point on a plane
    Returns vector equal to p0 + k01.(p1-p0) + k02.(p2-p0)

    @p0:     'Origin' point of a plane
    @p1:     Second point on the plane
    @p2:     Third point on the plane
    @k01:    Amount of P0->P1 direction of the point (from P0)
    @k02:    Amount of P0->P2 direction of the point (from P0)
    """
    # mp = p0 + k01.(p1-p0) + k02.(p2-p0)
    mp = vector_add(p0, p1, scale=k01 )
    mp = vector_add(mp, p2, scale=k02 )
    mp = vector_add(mp, p0, scale=(-k01-k02) )
    return mp

#a Closest meeting of two lines
def closest_meeting_of_two_lines(p0, d0, p1, d1, too_close=0.0001):
    """
    Points on the lines are p0+s.d0 and p1+t.d1
    The closest points are c0 and c1, with sc and tc the closest coefficients

    Consider a 3D space with the axes d0, d1 and d0 x d1
    Every point in space can be represented as (a,b,c) = a.d0 + b.d1 + c.(d0 x d1)
    for some a,b,c for the point

    Points on p0+s.d0 are expressed in this space as s'.d0 + P0b.d1 + P0c.(d0 x d1)
    Points on p1+t.d1 are expressed in this space as P1a.d0 + t'.d1 + P1c.(d0 x d1)

    A vector between these two points is then:
    (s'-P1a).d0 + (P0b-t').d1 + (P0c-P1c).(d0 x d1)

    This has minimum length when s'-P1a is zero and P0b-t' is zero (since d0 x d1 is perpendicular to d0 and d1)

    Now, p0 is at P0a.d0 + P0b.d1 + P0c.(d0 x d1), and s=s'-P0a (and t=t'-P1b)
    p0.d0 = P0a.(d0.d0) + P0b.(d1.d0)
    p0.d1 = P0a.(d0.d1) + P0b.(d1.d1)
    i.e. [d0.d0 d1.d0] [P0a]  = [p0.d0]
         [d0.d1 d1.d1] [P0b]    [p0.d1]
    and
         [d0.d0 d1.d0] [P1a]  = [p1.d0]
         [d0.d1 d1.d1] [P1b]    [p1.d1]
    =>  P0a = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) ( d1.d1 . p0.d0 - d1.d0 . p0.d1)
    and P0b = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) (-d1.d0 . p0.d0 + d0.d0 . p0.d1)
    and P1a = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) ( d1.d1 . p1.d0 - d1.d0 . p1.d1)
    and P1b = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) (-d1.d0 . p1.d0 + d0.d0 . p1.d1)

    Now s=s'-P0a = P1a-P0a, t=t'-P1b = P0b-P1b
    s = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) . (d1.d1 . d0.(p1-p0) - d1.d0 . d1.(p1-p0) )
    t = 1/(d0.d0 . d1.d1 - d1.d0 . d0.d1) . (d0.d0 . d1.(p1-p0) - d1.d0 . d0.(p1-p0) )
    
    If we set D = (d0.d0 . d1.d1 - d1.d0 . d0.d1) (determinant of our solution matrix)
    we can see when the solution is degenerate

    D = |d0|^2 . |d1|^2 - (|d0||d1|cos(d0d1) )^2
    D = sin^2(d0d1) . (|d0||d1|)^2
    If d0 and d1 are approximately unit vectors, D is then sin^2(angle) between
    i.e. D<epsilon implies the lines are too close to parallel

    We can also see how 'close' the lines are by |c1-c0|, or (c1-c0).(c1-c0)
    Indeed, we can have a measure of 'goodness' using (c1-c0).(c1-c0) / D

    """
    p1p0 = vector_add(p1,p0,scale=-1.0)
    d0d0 = vector_dot_product(d0,d0)
    d1d1 = vector_dot_product(d1,d1)
    d0d1 = vector_dot_product(d0,d1)

    d0p10 = vector_dot_product(d0,p1p0)
    d1p10 = vector_dot_product(d1,p1p0)

    D = d0d0*d1d1 - d0d1*d0d1

    if D<too_close:
        zero = vector_add(p0,p0,scale=-1.0)
        return ( zero, zero, 0.0, 1.0/too_close )

    s = (d1d1*d0p10 - d0d1*d1p10) / D
    t = (d0d1*d0p10 - d0d0*d1p10) / D

    c0 = vector_add(p0,d0,scale=s)
    c1 = vector_add(p1,d1,scale=t)

    dc = vector_add(c1,c0,scale=-1.0)
    dc2 = vector_dot_product(dc,dc)

    goodness = dc2/D
    if goodness>1.0/too_close: goodness=1.0/too_close
    return (c0, c1, dc2, goodness)

