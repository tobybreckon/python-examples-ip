#####################################################################

# Example : display individual HSV channels from an video file
# specified on the command line (e.g. python FILE.py video_file) or from an
# attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 Toby Breckon
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys
import numpy as np
import math

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

colour_map_hue = False; # use colour mapping to display Hue

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowNameH = "Hue Channel"; # window name
windowNameS = "Saturation Channel"; # window name
windowNameV = "Value Channel"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create window by name (note flags for resizable or not)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    # usage

    print("USAGE: press 'c' for Hue channel colour mapping")

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount();

        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

        # display images

        cv2.imshow(windowName,frame);

        # colour channels are HSV ordering in OpenCV

        cv2.imshow(windowNameS,img_hsv[:,:,1]); # saturation
        cv2.imshow(windowNameV,img_hsv[:,:,2]); # value

        if (colour_map_hue):
            # re map S and V to top outer rim of HSV colour space

            img_hsv[:,:,1] = np.ones(img_hsv[:,:,1].shape) * 255;
            img_hsv[:,:,2] = np.ones(img_hsv[:,:,1].shape) * 255;

            # convert the result back to BGR to produce a false colour version of hue
            # for display

            colour_mapped_hue = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR);
            cv2.imshow(windowNameH,colour_mapped_hue); # colour mapped hue
        else:
            cv2.imshow(windowNameH,img_hsv[:,:,0]); # hue

        # stop the timer and convert to ms. (to see how long processing and display takes)

        stop_t = ((cv2.getTickCount() - start_t)/cv2.getTickFrequency()) * 1000;

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)
        # here we use a wait time in ms. that takes account of processing time already used in the loop

        # wait 40ms or less depending on processing time taken (i.e. 1000ms / 25 fps = 40 ms)

        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF;

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;
        elif (key == ord('c')):
            colour_map_hue = True;

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################


