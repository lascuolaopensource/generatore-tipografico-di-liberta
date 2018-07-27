# -*- coding: utf-8 -*-

### FUNCTIONS

# draw_bit_chr
# This function reads a character at a given position (px, py)
# and invokes a drawing function specified in the syntax dictionary - paired with that character.
# The function draws (with a RPen) in the glyph in a box of width h_step and height v_step.

# string, RPen, float, float, float, float, dictionary
def draw_bit_chr(gly, char, px, py, h_step, v_step, row, col, syntax):

    # Try to execute the matching...
    try:

        # Cell size
        cell_w = h_step/col
        cell_h = v_step/row

        # Starting point
        sx = px + cell_w/2
        sy = py + cell_h/2

        # Iteraring over the cells
        for i in range(row):
            for j in range(col):

                # Center of new box
                cell_x = sx + j*cell_w
                cell_y = sy + i*cell_h

                syntax[char][0](gly=gly, position=(cell_x, cell_y), size=(cell_w, cell_h), properties=syntax[char][1])

    # ...unless there's no matching function
    except KeyError:
        pass



# draw_bit_lin
# This function iterates draw_bit_chr over a string (line) of characters.

# string, RPen, float, float, float, float, dictionary
def draw_bit_lin(gly, line, px, py, h_step, v_step, row, col, syntax):

    for char in line:
        draw_bit_chr(gly, char, px, py, h_step, v_step, row, col, syntax)

        # Translating the x position by the width of the module
        px += h_step



# draw_bit_gly
# This function iterates draw_bit_lin over the full glyph ascii description.
# (So it draws the full glyph)

# dictionary, RPen, float, float, float, dictionary
def draw_bit_gly(gly, gly_dict, dsc_hgt, h_step, v_step, row, col, syntax):

    # Setting starting coordinates
    px = 0
    py = dsc_hgt    # We start from the descender, then we go all the way up

    # Iterating over glyph instructions (but backwards, so we start from the descenders)
    for line in gly_dict[::-1]:
        draw_bit_lin(gly, line, px, py, h_step, v_step, row, col, syntax)

        # Updating position once a row of characters (lin) is completed
        px = 0
        py += v_step



# draw_bit_fnt
# This function generates a full set of *alternative* (alt) glyphs from instructions.

# RFont, dictionary, string, float, float, float, dictionary -> RFont
def draw_bit_fnt(fnt, fnt_dict, alt, dsc_hgt, h_step, v_step, row, col, syntax):

    # Iterating over the dictionary (the instructions)
    for gly_name in fnt_dict:

        # Creating alternative glyph
        gly = fnt.newGlyph(gly_name + alt)
        gly.autoUnicodes()
        gly.clear()

        # Getting glyph instructions from dict
        gly_dict = fnt_dict[gly_name]

        # Setting glyph width
        gly.width = h_step * len(gly_dict[0])

        # Drawing the glyph
        draw_bit_gly(gly, gly_dict, dsc_hgt, h_step, v_step, row, col, syntax)

    return fnt