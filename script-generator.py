# -*- coding: utf-8 -*-

### Run with Robofont 1.8.x

### MODULES

import sys
import os
sys.path.insert(0, os.getcwd() + "/lib")

# Importing GTL libraries
from txt_reader import *
from draw_bits import draw_bit_fnt
from shape_functions import *






### VARIABLES

# Absolute path of project font
fnt_path = os.getcwd() + "/Untitled.ufo"

# Absolute path of folder containing glyphs'txts
txt_path = os.getcwd() + "/assets/txt-letters/test"

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



### SYMBOL CHOICE

# Absolute path of symbols font
font_symbols_path = os.getcwd() + "/assets/symbols/symbols-ode.ufo"

# Opening font containing symbols
font_symbols = OpenFont(font_symbols_path)

# Choosing symbol glyph from font
gly_symbol = font_symbols["cultura0"]

# Making a glyph list
gly_lst = [
    font_symbols["cultura0"],
    font_symbols["cultura1"],
    font_symbols["cultura2"],
    font_symbols["esplosivo0"],
    ]





### SHAPE PROPERTIES

# Symbol
p_symbol = {
    "source_glyph": gly_symbol,
    "scale": (1,1),
    "rotation": 5,
    "proportions_keep": False,
    "proportions_mode": "X"
    }

p_symbol_list = {
    "source_glyph_list": gly_lst,
    "scale": (1,1),
    "rotation": 5,
    "proportions_keep": False,
    "proportions_mode": "X"
    }

# Rectangle
p_rectangle = {
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# Ellipse
p_ellipse = {
    "squaring": .56,
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# Rhombus (== ellipse with zero squaring)
p_ellipse_t = {
    "squaring": 0,
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# Ellipse quarter
# Possible orientations: NE, NW, SE, SW
p_el_quarter = {
    "squaring": .56,
    "orientation": "NW",
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
}

# Rhombus (== ellipse with zero squaring) quarter
# Possible orientations: NE, NW, SE, SW
p_el_quarter_t = {
    "squaring": 0,
    "orientation": "NW",
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
}

# Ellipse half
# Possible orientations: N, S, E, W
p_el_half = {
    "squaring": .56,
    "orientation": "N",
    "scale": (1, 1),
    "rotation": 0,
    "clockwise": True
}

# Rhombus (== ellipse with zero squaring) half
# Possible orientations: N, S, E, W
p_el_half_t = {
    "squaring": 0,
    "orientation": "N",
    "scale": (1, 1),
    "rotation": 0,
    "clockwise": True
}

# Random function selector
p_random = [
    (rectangle         , p_rectangle),
    (ellipse           , p_ellipse),
    (ellipse           , p_ellipse_t),
    (ellipse_quarter_ro, p_el_quarter),
    (ellipse_quarter_ro, p_el_quarter_t),
    (ellipse_half_ro   , p_el_half),
    (ellipse_half_ro   , p_el_half_t)
]

# Do nothing
p_do_nothing = {"null": "null"}

### SINTASSI

sintassi = {
    ".": (do_nothing, p_do_nothing),
    "@": (do_nothing, p_do_nothing),
    "#": (symbol_list, p_symbol_list),
    #"#": (rectangle , p_rectangle),
    "%": (do_nothing, p_do_nothing),
    "&": (do_nothing, p_do_nothing),
    "$": (do_nothing, p_do_nothing),
    "+": (do_nothing, p_do_nothing)
}






### INSTRUCTIONS
fnt = OpenFont(fnt_path)

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
