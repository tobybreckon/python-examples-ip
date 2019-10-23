#####################################################################

# Example : gaussian and bi-lateral filtering on an image from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2019 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys
import argparse
import math

#####################################################################

keep_processing = True

# parse command line arguments for camera ID or video file

parser = argparse.ArgumentParser(description='Perform ' + sys.argv[0] + ' example operation on incoming camera/video image')
parser.add_argument("-c", "--camera_to_use", type=int, help="specify camera to use", default=0)
parser.add_argument("-r", "--rescale", type=float, help="rescale image by this factor", default=1.0)
parser.add_argument('video_file', metavar='video_file', type=str, nargs='?', help='specify optional video file')
args = parser.parse_args()


#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# define video capture object

cap = cv2.VideoCapture()

# define display window name

windowName = "Live Camera Input" # window name
windowName2 = "Gaussian Smoothing" # window name
windowName3 = "Bilaterial Filtering" # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if cap.open(args.camera_to_use):

    # create window by name

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(windowName2, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(windowName3, cv2.WINDOW_AUTOSIZE)

    # add some track bar controllers for settings Gaussian smoothing

    neighbourhood = 3
    cv2.createTrackbar("neighbourhood, N", windowName2, neighbourhood, 40, nothing)
    sigma = 1
    cv2.createTrackbar("sigma", windowName2, sigma, 10, nothing)

    # add some track bar controllers for settings bilateral smoothing

    sigmaS = 10
    cv2.createTrackbar("sigmaS", windowName3, sigmaS, 25, nothing)
    sigmaR = 10
    cv2.createTrackbar("sigmaR", windowName3, sigmaR, 25, nothing)

    while (keep_processing):

        # if video file or camera successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read()

            # when we reach the end of the video (file) exit cleanly

            if (ret == 0):
                keep_processing = False
                continue

            # rescale if specified

            if (args.rescale != 1.0):
                frame = cv2.resize(frame, (0, 0), fx=args.rescale, fy=args.rescale)

        # get parameter from track bars - Gaussian

        neighbourhood = cv2.getTrackbarPos("neighbourhood, N", windowName2)
        sigma = cv2.getTrackbarPos("sigma", windowName2)

        # get parameter from track bars - bilateral

        sigmaS = cv2.getTrackbarPos("sigmaS", windowName3)
        sigmaR = cv2.getTrackbarPos("sigmaR", windowName3)

        # check neighbourhood is greater than 3 and odd

        neighbourhood = max(3, neighbourhood)
        if not(neighbourhood % 2):
            neighbourhood = neighbourhood + 1

        # perform Gaussian smoothing using NxN neighbourhood

        smoothed_img = cv2.GaussianBlur(frame, (neighbourhood, neighbourhood), sigma, sigma, borderType=cv2.BORDER_REPLICATE)

        # perform bilateral filtering using a neighbourhood calculated automatically from sigmaS

        filtered_img = cv2.bilateralFilter(frame, -1, sigmaR, sigmaS, borderType=cv2.BORDER_REPLICATE)

        # display image

        cv2.imshow(windowName, frame)
        cv2.imshow(windowName2, smoothed_img)
        cv2.imshow(windowName3, filtered_img)

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        key = cv2.waitKey(40) & 0xFF # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No usable camera connected.")


#####################################################################
