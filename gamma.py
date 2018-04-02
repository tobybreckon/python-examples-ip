#####################################################################

# Example : gamma correction /power-law transform on an image
# from an attached web camera (or video file specified on command line)

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2018 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import math
import sys
import numpy as np

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# power law transform
# I - colour image I
# gamma - "gradient" co-efficient of gamma function

def powerlaw_transform(I, gamma):

    # compute power-law transform
    # remembering not defined for pixel = 0 (!)

    # handle any overflow in a quick and dirty way using 0-255 clipping

    I = np.clip(np.power(I, gamma), 0, 255).astype('uint8')

    return I;

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowName2 = "Gamma Corrected (Power-Law Transform)"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE);
    cv2.namedWindow(windowName2, cv2.WINDOW_AUTOSIZE);

    # add some track bar controllers for settings

    gamma = 100; # default gamma - no change

    cv2.createTrackbar("gamma, (* 0.01)", windowName2, gamma, 500, nothing);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # get parameters from track bars

        gamma = cv2.getTrackbarPos("gamma, (* 0.01)", windowName2) * 0.01;

        # make a copy

        gamma_img = frame.copy();

        # use power-law function to perform gamma correction

        gamma_img = powerlaw_transform(gamma_img, gamma);

        # display image

        cv2.imshow(windowName, frame);
        cv2.imshow(windowName2, gamma_img);

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        key = cv2.waitKey(40) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No usable camera connected.")


#####################################################################
