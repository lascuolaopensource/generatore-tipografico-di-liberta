# -*- coding: utf-8 -*-

### MODULES
import os



### FUNCTIONS

# get_glyph_from_txt
# This function reads a txt file and returns a dictionary line
# The key is the name of the glyph, the value is the letter structure

# String -> Dictionary
def get_glyph_from_txt(txt_file):

    # Reading file
    with open(txt_file, "r") as txt_open:
        txt_read = txt_open.read().strip()

    # Splitting unique string
    txt_split = txt_read.split("\n")

    # Key: saving glyph name [and stripping "/r" because of windows]
    key = txt_split[0].strip("\r")

    # Value: saving letter structure (as list of lines)
    value = [i.strip() for i in txt_split[2:]]

    return {key: value}



# get_font_from_folder
# This function reads all the txts in a folder
# and returs a dictionary where each entry is a glyph name-structure pair

# String -> Dictionary
def get_font_from_folder(folder_path):

    # Creating an empty dictionary where all the keys will be appended
    font_dict = {}

    # Iterating over folders and subdirectories
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if ".txt" in file:

                # Adding to the dictionary the key value pair
                font_dict.update(get_glyph_from_txt(subdir + "/" + file))

    return font_dict
