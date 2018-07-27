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
# and returns the drawn contour

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



# make_clockwise

# RGlyph, boolean -> RGlyph
def make_clockwise(gly, cw):

    # Contour operations - Selecting last drawn contour
    c = gly[-1]

    # Contour direction
    d = c.clockwise

    # Making clockwise or anticlockwise
    if (d and cw) or not (d and cw):
        pass
    else:
        c.reverseContour()

    return gly






### FUNCTIONS - SHAPES

# do_nothing
# Does nothing - Used to leave blank space

# Pen, float, float, dict -> Pen
def do_nothing(gly, position, size, properties):
    pass



# rectangle
# Draw a square of a given side

# RGlyph, float, float, dict ->
def rectangle(gly, position, size, properties):

    # Getting rectangle properties
    scl = properties["scale"]
    rot = properties["rotation"]
    cw  = properties["clockwise"]

    # Coordinates
    x, y = position

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Drawing contour
    drawer(gly,
           [(x-w, y-h), (x-w, y+h), (x+w, y+h), (x+w, y-h)])

    make_clockwise(gly, cw)



# ellipse
# Draws an ellipse

# RGlyph, float, float, dict ->
def ellipse(gly, position, size, properties):

    # Getting ellipse properties
    s   = properties["squaring"]
    cw  = properties["clockwise"]

    # Coordinates
    x, y = position

    # Useful shortcut
    w = size[0]/2
    h = size[1]/2

    # Drawing contour
    drawer(gly,
           [(x-w, y), ((x-w, y+h), (x, y+h), s), ((x+w, y+h), (x+w, y), s), ((x+w, y-h), (x, y-h), s), ((x-w, y-h), (x-w, y), s)])

    make_clockwise(gly, cw)



# quarter
# Draws a quarter of circumference

# RGlyph, float, float, dict ->
def quarter(gly, position, size, properties):

    # Getting quarter properties
    sqr = properties["squaring"]
    orn = properties["orientation"]
    cw  = properties["clockwise"]

    # Coordinates
    x, y = position

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

    # Rotating
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

    make_clockwise(gly, cw)
    c.move((x, y))
    gly.update()



# quarter
# Draws a quarter of circumference

# RGlyph, float, float, dict ->
def semiellipse(gly, position, size, properties):

    # Getting quarter properties
    wdt = properties ['width']
    hgt = properties ['height']
    sqr = properties ['squaring']
    orn = properties ["orientation"]
    cw  = properties ['clockwise']

    # Coordinates
    x, y = position

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

    # Rotating
    if   "N" == orn:
        pass
    elif "S" == orn:
        c.scale((1, -1))
    elif "W" == orn:
        c.rotate(90)
    elif "E" == orn:
        c.rotate(90)

    make_clockwise(gly, cw)
    c.move((x, y))
    gly.update()






### FUNCTIONS - APPLY COMPONENT
def copy_glyph(gly, position, size, properties):

    # Unpacking
    x, y = position
    w, h = size 

    # Getting font reference
    f      = properties["font"]

    # Getting glyph-to-copy name
    g_name = properties["glyph"]

    # Getting glyph-to-copy reference
    g      = f[g_name]

    # Getting glyph size
    w = (g.box[2] - g.box[0])*scl[0]
    h = (g.box[3] - g.box[1])*scl[1]

    print w, h

    gly.appendComponent(g_name, offset=(x-w/2,y-h/2), scale=scl)



def selettore_valori(gly, position, size, properties):

    val = properties["valori"]
    per = properties["persone"]

    gly_name = choice(val) + str(per)

    properties["glyph"] = gly_name

    copy_glyph(gly, position, size, properties)






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