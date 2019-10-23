#####################################################################

# Example : capture an image from an attached camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2019 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import numpy as np
import cv2
import argparse
import sys

#####################################################################

# parse command line arguments for camera ID or video file

parser = argparse.ArgumentParser(description='Perform ' + sys.argv[0] + ' example operation on incoming camera/video image')
parser.add_argument("-c", "--camera_to_use", type=int, help="specify camera to use", default=0)
parser.add_argument("-r", "--rescale", type=float, help="rescale image by this factor", default=1.0)
args = parser.parse_args()

#####################################################################

# define video capture object

cap = cv2.VideoCapture()

# define display window name

windowName = "Live Camera Input" # window name

# open camera device (and check it worked)

if not(cap.open(args.camera_to_use)):
    print("Cannot open camera - check connection and operation as suggested.")
    sys.exit

# read an image from the camera

ret, frame = cap.read()

# to avoid the black/blank first frame from many cameras
# with some (not all) cameras you need to read the first frame twice (first frame only)

ret, frame = cap.read()

# check it has loaded

if not frame is None:

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

    # display image

    cv2.imshow(windowName,frame)

    # start the event loop - essential
    # wait indefinitely for any key press

    cv2.waitKey(0)

else:
    print("No image successfully loaded from camera.")

# close all windows

cv2.destroyAllWindows()

#####################################################################
