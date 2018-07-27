# -*- coding: utf-8 -*-

### FUNCTIONS

# draw_bit_chr
# This function reads a character at a given position
# and invokes a drawing function specified in the syntax dictionary - paired with that character.
# The function draws (with a RPen) in the glyph in a box of width h_step and height v_step.

# RGlyph, string, (float, float), (float, float), (int, int), dictionary
def draw_bit_chr(gly, char, box_position, box_size, box_layout, syntax):

    # Try to execute the matching...
    try:

        # Cell size
        cell_wdt = box_size[0]/box_layout[0]
        cell_hgt = box_size[1]/box_layout[1]

        # Starting point
        sx = box_position[0] + cell_w/2
        sy = box_position[1] + cell_h/2

        # Iteraring over the cells
        for i in range(box_layout[0]):
            for j in range(box_layout[1]):

                # Center of new cell
                cell_x = sx + j*cell_wdt
                cell_y = sy + i*cell_hgt

                syntax[char][0](gly, (cell_x, cell_y), (cell_wdt, cell_hgt), syntax[char][1])

    # ...unless there's no matching function
    except KeyError:
        print "Invalid character used: " + char



# draw_bit_lin
# This function iterates draw_bit_chr over a string (line) of characters.

# RGlyph, string, (float, float), (float, float), (int, int), dictionary
def draw_bit_lin(gly, char_line, box_position, box_size, box_layout, syntax):

    for char in char_line:
        draw_bit_chr(gly, char, box_position, box_size, box_layout, syntax)

        # Translating the x position by the width of the box
        box_position[0] += box_size[0]



# draw_bit_gly
# This function iterates draw_bit_lin over the full glyph ascii description.
# (So it draws the full glyph)

# RGlyph, list of lists, float, (float, float), (int, int), dictionary -> RGlyph
def draw_bit_gly(gly, gly_desc, dsc_hgt, box_size, box_layout, syntax):

    # Setting starting coordinates
    box_x = 0
    box_y = dsc_hgt    # We start from the descender, then we go all the way up

    # Iterating over glyph instructions (but backwards, so that we start from the descenders)
    for char_line in gly_dict[::-1]:
        draw_bit_lin(gly, char_line, (box_x, box_y), box_size, box_layout, syntax)

        # Updating position once a row of characters (lin) is completed
        box_x = 0
        box_y += box_size[1]

    return gly



# draw_bit_fnt
# This function generates a full set of *alternative* (alt) glyphs from instructions.

# RFont, dictionary, string, float, (float, float), (int, int), dictionary -> RFont
def draw_bit_fnt(fnt, fnt_dict, suffix, dsc_hgt, box_size, box_layout, syntax):

    # Iterating over the dictionary (the instructions)
    for gly_name in fnt_dict:

        # Creating new glyph
        gly = fnt.newGlyph(gly_name + "." + suffix)
        gly.autoUnicodes()
        gly.clear()

        # Getting glyph description from dict
        gly_desc = fnt_dict[gly_name]

        # Setting glyph width
        gly.width = box_size[0] * len(gly_desc[0])

        # Drawing the glyph
        draw_bit_gly(gly, gly_desc, dsc_hgt, box_size, box_layout, syntax)

    return fnt