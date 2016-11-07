#####################################################################

# Example : mean and non-local means filter on an image from an attached web camera

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
windowName2 = "Mean Filtering"; # window name
windowName3 = "Non-Local Means Filtering"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if cap.open(camera_to_use):

    # create window by name

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE);
    cv2.namedWindow(windowName2, cv2.WINDOW_AUTOSIZE);
    cv2.namedWindow(windowName3, cv2.WINDOW_AUTOSIZE);

    # add some track bar controllers for settings

    neighbourhood = 7;
    cv2.createTrackbar("neighbourhood, N", windowName2, neighbourhood, 25, nothing);
    searchW = 21;
    cv2.createTrackbar("search area, W", windowName3, searchW, 50, nothing);
    filter_strength = 10;
    cv2.createTrackbar("strength, h", windowName3, filter_strength, 25, nothing);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # get parameters from track bars

        neighbourhood = cv2.getTrackbarPos("neighbourhood, N", windowName2);
        searchW = cv2.getTrackbarPos("search area, W", windowName3);
        filter_strength = cv2.getTrackbarPos("strength, h", windowName3);

        # check neighbourhood is greater than 3 and odd

        neighbourhood = max(3, neighbourhood);
        if not(neighbourhood % 2):
            neighbourhood = neighbourhood + 1;

        # in opencv blur() performs filtering with a NxN kernel where each element has a weight of
        # 1 / (N^2) - this is mean filtering

        mean_img = cv2.blur(frame, (neighbourhood,neighbourhood), borderType=cv2.BORDER_DEFAULT);

        # perform NLM filtering on the same image

        nlm_img = cv2.fastNlMeansDenoisingColored(frame, h=filter_strength, hColor=10, templateWindowSize=neighbourhood, searchWindowSize=searchW);

        # display image

        cv2.imshow(windowName, frame);
        cv2.imshow(windowName2, mean_img);
        cv2.imshow(windowName3, nlm_img);

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


