# -*- coding: utf-8 -*-

# Run with Robofont 1.8.x

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
fnt_path = os.getcwd() + "/project.ufo"

# Absolute path of folder containing glyphs'txts
txt_path = os.getcwd() + "/assets/txt-letters/liberta/roman/Letter/Lowercase"

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
# This is an example of loading a symbol from ufo file

# Absolute path of symbols font
font_symbols_path = os.getcwd() + "/assets/symbols/test-symbols.ufo"

# Opening font containing symbols
font_symbols = OpenFont(font_symbols_path)

## Now you can:

# A) USE SYMBOL FUNCTION - You can choose a specific symbol glyph from font
gly_symbol = font_symbols["test_symbol-0"]

# B) USE SYMBOL_LIST FUNCTION - You can create a list of symbols that will be randomly chosen
gly_lst = [
    font_symbols["test_symbol-0"],
    font_symbols["test_symbol-1"],
    font_symbols["test_symbol-2"],
    font_symbols["test_symbol-3"],
    ]






"""
AVAILABLE FUNCTIONS

Here's a list of available functions for drawing:

- do_nothing

- rectangle
- ellipse
- ellipse_half
- ellipse_half_ro (randomly chooses the orientation)
- ellipse_quarter
- ellipse_quarter_ro (randomly chooses the orientation)

- symbol (draws a symbol taken from another glyph)
- symbol_list (draws a random symbol taken from a list of glyphs)

- random_function (draws a random function from the ones specified)
"""






"""
SHAPE PROPERTIES

All the functions accept an argument which is called "properties":
it is a dictionary consisting of several properties that can be used to modify the shapes
Below, there's a list of all the possible properties for each function,
plus some extras.
"""

# do_nothing
p_do_nothing = {
    "null": "null"
    }

# rectangle
p_rectangle = {
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# ellipse
p_ellipse = {
    "squaring": .56,
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# ellipse_half (Possible orientations: N, S, E, W) AND ellipse_half_ro
p_ellipse_half = {
    "squaring": .56,
    "orientation": "N",
    "scale": (1, 1),
    "rotation": 0,
    "clockwise": True
}

# ellipse_quarter (Possible orientations: NE, NW, SE, SW) AND ellipse_quarter_ro
p_ellipse_quarter = {
    "squaring": .56,
    "scale": (1,1),
    "rotation": 0,
    "orientation": "NW",
    "clockwise": True
}

# symbol
p_symbol = {
    "source_glyph": gly_symbol,
    "scale": (1,1),
    "rotation": 5,
    "proportions_keep": False,
    "proportions_mode": "X"
    }

# symbol_list
p_symbol_list = {
    "source_glyph_list": gly_lst,
    "scale": (1,1),
    "rotation": 5,
    "proportions_keep": False,
    "proportions_mode": "X"
    }

## EXTRAS 1 - Rhombus, triangles

# rhombus == an ellipse with zero squaring
p_ellipse_0 = {
    "squaring": 0,
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
    }

# isosceles triangle = half ellipse with zero squaring (Possible orientations: N, S, E, W)
p_ellipse_half_0 = {
    "squaring": 0,
    "orientation": "N",
    "scale": (1, 1),
    "rotation": 0,
    "clockwise": True
}

# right triangle = a quarter of ellipse with zero squaring (Possible orientations: NE, NW, SE, SW)
p_ellipse_quarter_0 = {
    "squaring": 0,
    "orientation": "NW",
    "scale": (1,1),
    "rotation": 0,
    "clockwise": True
}

## EXTRAS 2 - Ready-made corners

p_ellipse_quarter_NW = p_ellipse_quarter.copy()
p_ellipse_quarter_NW["orientation"] = "NW"

p_ellipse_quarter_NE = p_ellipse_quarter.copy()
p_ellipse_quarter_NE["orientation"] = "NE"

p_ellipse_quarter_SW = p_ellipse_quarter.copy()
p_ellipse_quarter_SW["orientation"] = "SW"

p_ellipse_quarter_SE = p_ellipse_quarter.copy()
p_ellipse_quarter_SE["orientation"] = "SE"

## EXTRAS 3 - Random

# random_function
p_random_function = [
    (rectangle         , p_rectangle        ),
    (ellipse           , p_ellipse          ),
    (ellipse           , p_ellipse_0        ),
    (ellipse_half_ro   , p_ellipse_half     ),
    (ellipse_half_ro   , p_ellipse_half_0   ),
    (ellipse_quarter_ro, p_ellipse_quarter  ),
    (ellipse_quarter_ro, p_ellipse_quarter_0)
]






"""
SYNTAX

Here we decide what function goes with which symbol.
The following syntax is the one made for libertà font.
"""

sintassi = {
    # Do nothing
    ".": (do_nothing, p_do_nothing),
    # Main structure
    "#": (symbol_list, p_symbol_list),
    # Serifs
    "@": (do_nothing, p_do_nothing),
    # Corners
    "%": (do_nothing, p_do_nothing),
    "&": (do_nothing, p_do_nothing),
    "+": (do_nothing, p_do_nothing),
    "$": (do_nothing, p_do_nothing),
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
