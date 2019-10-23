#####################################################################

# Example : save an image from file (and invert it)

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import numpy as np
import cv2
import argparse

#####################################################################

# read an image from the specified file (in colour)

img = cv2.imread('example.jpg', cv2.IMREAD_COLOR)

# check it has loaded

if not img is None:

    # performing logical inversion (see manual entry for bitwise_not()

    inverted = cv2.bitwise_not(img)

    # write inverted image to file

    cv2.imwrite("inverted.jpg", inverted)

else:
    print("No image file successfully loaded.")

#####################################################################


