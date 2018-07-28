# -*- coding: utf-8 -*-

### MODULES
from random import choice






### FUNCTIONS - UTILITY

# interpolate_points
# Interpolation of two tuples

# tuple, tuple, float -> tuple
def interpolate_points(pA, pB, f):
    return tuple([pA[i]+(pB[i]-pA[i])*f for i in (0, 1)])



# drawer
# A general function that links any given points

# RGlyph, list, boolean -> RGlyph
def drawer(gly, pts):

    # Getting glyph pen
    pen = gly.getPen()

    # Moving pen to first point of the list
    pen.moveTo(pts[0])

    # Drawing lines to the rest of the points
    for i in range(1, len(pts)):

        # Current point
        pt = pts[i]

        # If next point is expressed as tuple, that's a line point
        if len(pt) == 2:
            pen.lineTo(pt)

        # If next point is expressed as (tuple, tuple, float), that's a curve point
        elif len(pt) == 3:

            # Previous point
            if len(pts[i-1]) == 2:
                pt_previous = pts[i-1]
            elif len(pts[i-1]) == 3:
                pt_previous = pts[i-1][1]

            # Control point out
            cpt_o = interpolate_points(pt_previous, pt[0], pt[2])

            # Control point in
            cpt_i = interpolate_points(pt[1], pt[0], pt[2])

            # Drawing curve
            pen.curveTo(cpt_o, cpt_i, pt[1])

    pen.closePath()
    return gly



# make_clockwise
# does what it says

# RContour, boolean -> RContour
def make_clockwise(c, cw):

    # Making clockwise anyways
    if c.clockwise == 0:
        c.reverseContour()

    # Inverting if necessary
    if cw == False:
        c.reverseContour()

    return c






### FUNCTIONS - SHAPES

# do_nothing
# Does nothing - Used to leave blank space

# RGlyph, tuple, tuple, dict ->
def do_nothing(gly, position, size, properties):
    pass



# rectangle

# RGlyph, (float, float), (float, float), dict ->
def rectangle(gly, position, size, properties):

    # Getting rectangle properties
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points (ideally, we draw at (0,0), then we translate)
    p0 = -w, -h
    p1 = -w,  h
    p2 =  w,  h
    p3 =  w, -h

    # Drawing contour
    drawer(gly, [p0, p1, p2, p3])

    # Contour operations: scale, rotate, translate, clockwise, round points
    c = gly[-1]
    c.scale(scl)
    c.rotate(rot)
    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# ellipse
# Draws an ellipse

# RGlyph, (float, float), (float, float) dict ->
def ellipse(gly, position, size, properties):

    # Getting rectangle properties
    sqr = properties["squaring"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points (ideally, we draw at (0,0), then we translate)
    p0 = -w,  0
    p1 = -w,  h
    p2 =  0,  h
    p3 =  w,  h
    p4 =  w,  0
    p5 =  w, -h
    p6 =  0, -h
    p7 = -w, -h

    # Drawing contour
    drawer(gly,
           [p0, (p1, p2, sqr), (p3, p4, sqr), (p5, p6, sqr), (p7, p0, sqr)])

    # Contour operations: scale, rotate, translate, clockwise, round points
    c = gly[-1]
    c.scale(scl)
    c.rotate(rot)
    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# quarter
# Draws a quarter of circumference

# RGlyph, (float, float), (float, float), dict ->
def ellipse_quarter(gly, position, size, properties):

    # Getting quarter properties
    sqr = properties["squaring"]
    orn = properties["orientation"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points
    p0 = -w, -h
    p1 = -w,  h
    p2 =  w,  h
    p3 =  w, -h

    # Drawing contour
    drawer(gly, [p0, p1, (p2, p3, sqr)])

    # Contour operations - Selecting contour
    c = gly[-1]

    c.scale(scl)

    # Mirroring
    if "N" in orn:
        if "W" in orn:
            c.scale((-1,  1))
        elif "E" in orn:
            pass
    if "S" in orn:
        if "W" in orn:
            c.scale((-1, -1))
        elif "E" in orn:
            c.scale(( 1, -1))

    c.move(position)
    make_clockwise(c, clw)
    c.round()
    gly.update()



# quarter
# Draws a quarter of circumference

# RGlyph, (float, float), (float, float), dict ->
def ellipse_half(gly, position, size, properties):

    # Getting quarter properties
    sqr = properties["squaring"]
    orn = properties["orientation"]
    scl = properties["scale"]
    rot = properties["rotation"]
    clw = properties["clockwise"]

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Points
    p00 = -w,  0
    p01 = -w,  h
    p02 =  0,  h
    p03 =  w,  h
    p04 =  w,  0
    p05 =  0,  0
    p06 = p04
    p07 =  w, -h
    p08 = -w, -h
    p09 = p00
    p10 = p05

    drawer(gly, [p00, (p01, p02, sqr), (p03, p04, sqr), p05, (p06, p07, sqr), p08, (p09, p10, sqr)])

    # Contour operations - Selecting contour
    c = gly[-1]

    # Orientating
    if   "N" == orn:
        pass
    elif "S" == orn:
        c.scale((1, -1))
    elif "W" == orn:
        c.rotate(-90)
        c.scale((size[0]/size[1], size[1]/size[0]))
    elif "E" == orn:
        c.rotate(90)
        c.scale((size[0]/size[1], size[1]/size[0]))

    make_clockwise(c, clw)
    c.move(position)
    c.round()
    gly.update()






### FUNCTIONS - APPLY COMPONENT
def apply_comp(gly, position, size, properties):

    # Unpacking
    x, y = position
    w, h = size 

    # Getting font reference
    f      = properties["font"]

    # Getting component name
    c_name = properties["glyph"]

    # Getting component reference
    c      = f[c_name]

    # Getting component size
    c_wdt = c.box[2] - c.box[0]
    c_hgt = c.box[3] - c.box[1]

    # Getting scale factors
    if c_wdt > w:
        scl_x = w/c_wdt
    else:
        scl_x = c_wdt/w
    if c_hgt > h:
        scl_y = h/c_hgt
    else:
        scl_y = c_hgt/h

    gly.appendComponent(c_name, offset=(x - w/2, y - h/2), scale=(scl_x, scl_y))



def selettore_valori(gly, position, size, properties):

    val = properties["valori"]
    per = properties["persone"]

    gly_name = choice(val) + str(per)

    properties["glyph"] = gly_name

    apply_comp(gly, position, size, properties)






### FUNCTIONS - COMPOSITION
def random_function (gly, position, size, properties):
    function = choice(properties)
    function[0](gly=gly, position=position, size=size, properties=function[1])






# ### TEST
# fnt = CurrentFont()
# gly = fnt["A"]
# gly.clear()
# pen = gly.getPen()

# semiellipse(gly, 100, 100,
#         {
#         "width": 50,
#         "height": 50,
#         "squaring": .6,
#         "orientation": "N",
#         "clockwise": True
#         })