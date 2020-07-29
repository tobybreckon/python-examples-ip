#####################################################################

# Example : exponential transform on an image from an attached web camera

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

parser = argparse.ArgumentParser(
    description='Perform ' +
    sys.argv[0] +
    ' example operation on incoming camera/video image')
parser.add_argument(
    "-c",
    "--camera_to_use",
    type=int,
    help="specify camera to use",
    default=0)
parser.add_argument(
    "-r",
    "--rescale",
    type=float,
    help="rescale image by this factor",
    default=1.0)
parser.add_argument(
    'video_file',
    metavar='video_file',
    type=str,
    nargs='?',
    help='specify optional video file')
args = parser.parse_args()


#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# exponential transform
# I - greyscale image I
# C - scaling constant
# alpha - "gradient" co-efficient of exponential function


def exponential_transform(I, C, alpha):
    for i in range(0, I.shape[1]):  # image width
        for j in range(0, I.shape[0]):  # image height

            # compute exponential transform

            I[j, i] = int(C * (math.pow(1 + alpha, I[j, i]) - 1))
    return I

#####################################################################

# define video capture object


cap = cv2.VideoCapture()

# define display window name

windowName = "Live Camera Input"  # window name
windowName2 = "Exponential Transform"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.namedWindow(windowName2, cv2.WINDOW_NORMAL)

    # add some track bar controllers for settings

    constant = 10
    cv2.createTrackbar("constant, C", windowName2, constant, 100, nothing)

    alpha = 10
    cv2.createTrackbar("alpha (*0.001)", windowName2, alpha, 50, nothing)

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
                frame = cv2.resize(
                    frame, (0, 0), fx=args.rescale, fy=args.rescale)

        # convert to grayscale

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get parameters from track bars

        constant = cv2.getTrackbarPos("constant, C", windowName2)
        alpha = cv2.getTrackbarPos("alpha (*0.001)", windowName2) * 0.001

        # make a copy and exp tranform it

        exp_img = gray_img.copy()
        exp_img = exponential_transform(exp_img, constant, alpha)

        # display image

        cv2.imshow(windowName, gray_img)
        cv2.imshow(windowName2, exp_img)

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)
        key = cv2.waitKey(40) & 0xFF

        # It can also be set to detect specific key strokes by recording which
        # key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No usable camera connected.")


#####################################################################
