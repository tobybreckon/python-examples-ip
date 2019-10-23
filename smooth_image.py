#####################################################################

# Example : displaying an image from file (and smoothing it)

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import numpy as np
import cv2
import argparse

#####################################################################

# define display window name

windowName = "Smoothed Image"; # window name

# read an image from the specified file (in colour)

img = cv2.imread('example.jpg', cv2.IMREAD_COLOR);

# check it has loaded

if not img is None:

    # performing smoothing on the image using a 5x5 smoothing mark (see manual entry for GaussianBlur())

    blur = cv2.GaussianBlur(img,(5,5),0);

    # display this blurred image in a named window

    cv2.imshow(windowName, blur);

    # start the event loop - essential

    # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
    # It waits for specified milliseconds for any keyboard event.
    # If you press any key in that time, the program continues.
    # If 0 is passed, it waits indefinitely for a key stroke.

    key = cv2.waitKey(0) & 0xFF; # wait

    # It can also be set to detect specific key strokes by recording which key is pressed

    # e.g. if user presses "x" then exit and close all windows

    if (key == ord('x')):
        cv2.destroyAllWindows();
else:
    print("No image file successfully loaded.")

#####################################################################


