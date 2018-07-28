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
txt_path = "/Users/giovanniabbatepaolo/Desktop/SOS/generatore-tipografico-di-liberta/assets/letters"

# Set glyphs'baseline row (counting from bottom of txt)
gly_baseline = 2

# Set the ratio between width of "pixelone" and its height:
# width_ratio = 2 means the module width will be twice its height
width_ratio = 1

# Set number of "pixelone" sub-units
box_col = 1 
box_row = 1

# Set name of set (".alt1", ".alt2", ...)
set_suffix = ""






### SHAPE PROPERTIES

p_rectangle = {
    "scale": (1.05,1.05),
    "rotation": 0,
    "clockwise": True
    }

p_ellipse = {
    "squaring": .6,
    "scale": (1,1),
    "rotation": 30,
    "clockwise": True
    }

p_el_quarter = {
    "squaring": .6,
    "orientation": "NW",
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
}

p_el_half = {
    "squaring": .6,
    "orientation": "N",
    "scale": (1, 1),
    "rotation": 0,
    "clockwise": True
}

p_random = [
    (rectangle      , p_rectangle),
    (ellipse        , p_ellipse),
    (ellipse_quarter, p_el_quarter),
    (ellipse_half   , p_el_half)
]



### SINTASSI

sintassi = {
    ".": (do_nothing, {"null": "null"}),
    "@": (rectangle, p_rectangle),
    "#": (rectangle, p_rectangle),
    "%": (do_nothing, {"null": "null"}),
    "&": (do_nothing, {"null": "null"}),
    "$": (do_nothing, {"null": "null"}),
    "£": (do_nothing, {"null": "null"})
}






### INSTRUCTIONS

# Selecting font in robofont
fnt = CurrentFont()

# Creating the dictionary with all the instructions
fnt_dict = get_font_from_folder(txt_path)

# Getting number of lines
first_key = next(iter(fnt_dict))
first_val = fnt_dict[first_key]
line_num = len(first_val)

# Calculating box height
box_hgt = 1000/line_num

# Calculating box width
box_wdt = box_hgt * width_ratio

# Calculating descender line
dsc_hgt = -box_hgt * gly_baseline






### DRAWING FONT

draw_bit_fnt(fnt = fnt,
             fnt_dict = fnt_dict,
             suffix = set_suffix,
             dsc_hgt = dsc_hgt,
             box_size = (box_wdt, box_hgt),
             box_layout = (box_row, box_col),
             syntax = sintassi)
