# -*- coding: utf-8 -*-

### MODULES

import sys
import os
sys.path.insert(0, os.getcwd() + "/lib")

# Importing GTL libraries
from txt_reader import *
from draw_bits import draw_bit_fnt
from shape_functions import *






### VARIABLES

# Absolute path of folder containing glyphs'txts
txt_path = "/Users/giovanniabbatepaolo/Desktop/SOS/generatore tipografico di libertà/assets/letters"

# Set baseline row (from bottom of txt)
baseline = 2

# Set width of unit
# h_step = 100

# Set name of set (".alt1", ".alt2", ...)
suffix = ""


col = 1 
row = 1







### INSTRUCTIONS

# Selecting font in robofont
fnt = CurrentFont()

# Creating the dictionary with all the instructions
fnt_dict = get_font_from_folder(txt_path)

# Getting number of lines
first_key = next(iter(fnt_dict))
first_val = fnt_dict[first_key]
line_num = len(first_val)

# Calculating vertical step (altezza del "pixelone")
v_step = 1000/line_num

# Calculating descender line
dsc_hgt = -v_step * baseline



h_step = v_step
sh = h_step/col
sv = v_step/row




### CALCOLO FATTORI DI SCALA E TRASLAZIONE
box = 186
box_scl_hor = sh/box
box_scl_ver = sv/box



### SYNTASSI

rectangle_properties = {
    "width": sh*.9,
    "height": sv*.9,
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

ellipse_properties = {
    "width": sh*.9,
    "height": sv*.9,
    "squaring": .6,
    "clockwise": True
    }


sintassi = {
    ".": (do_nothing, {"null": "null"}),
    "@": (random_function, [(rectangle, rectangle_properties), (ellipse, ellipse_properties)]),
    "#": (random_function, [(rectangle, rectangle_properties), (ellipse, ellipse_properties)]),
    "%": (do_nothing, {"null": "null"}),
    "&": (do_nothing, {"null": "null"}),
    "$": (do_nothing, {"null": "null"}),
    "£": (do_nothing, {"null": "null"})
}


# sintassi = {
#     "#": (do_nothing, {"null": "null"}),
#     ".": (rnd_draw, {"h_step": sh,
#                      "v_step": sv}),
#     "@": (do_nothing, {"null": "null"}),
#     "%": (rnd_draw, {"h_step": sh,
#                      "v_step": sv}),
#     "&": (rnd_draw, {"h_step": sh,
#                      "v_step": sv}),
#     "$": (rnd_draw, {"h_step": sh,
#                      "v_step": sv}),
#     "£": (rnd_draw, {"h_step": sh,
#                      "v_step": sv})
# }



# sintassi = {

#     ".": (do_nothing, {"null"  : "null"}),

#     "#": (selettore_valori, {"glyph"  : "null",
#                              "offset" : (0,0),
#                              "scale"  : (box_scl_hor, box_scl_ver),
#                              "font"   : fnt,
#                              "valori" : ["esplosivo", "utile", "cultura"],
#                              "persone": 2}),

#     "@": (selettore_valori, {"glyph"  : "null",
#                              "offset" : (0,0),
#                              "scale"  : (box_scl_hor, box_scl_ver),
#                              "font"   : fnt,
#                              "valori" : ["esplosivo", "utile", "cultura"],
#                              "persone": 2})
# }



# Iterating over the dictionary
draw_bit_fnt(fnt, fnt_dict, suffix, dsc_hgt, h_step, v_step, row, col, sintassi)
