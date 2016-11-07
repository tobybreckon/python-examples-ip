#####################################################################

# Example : median filter on an image from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

# version 0.1

#####################################################################

import cv2
import math

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowName2 = "Median Filtering"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if cap.open(camera_to_use):

    # create window by name

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE);
    cv2.namedWindow(windowName2, cv2.WINDOW_AUTOSIZE);

    # add some track bar controllers for settings

    neighbourhood = 3;
    cv2.createTrackbar("neighbourhood, N", windowName2, neighbourhood, 40, nothing);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # get parameter from track bars

        neighbourhood = cv2.getTrackbarPos("neighbourhood, N", windowName2);

        # check it is greater than 3 and odd

        neighbourhood = max(3, neighbourhood);
        if not(neighbourhood % 2):
            neighbourhood = neighbourhood + 1;


        # perform median filtering using NxN neighbourhood

        median_img = cv2.medianBlur(frame, neighbourhood);

        # display image

        cv2.imshow(windowName, frame);
        cv2.imshow(windowName2, median_img);

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


