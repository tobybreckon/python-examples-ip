#####################################################################

# Example : mean and non-local means filter on an image from an attached
# web camera

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

# define video capture object


cap = cv2.VideoCapture()

# define display window name

window_name = "Live Camera Input"  # window name
window_name2 = "Mean Filtering"  # window name
window_name3 = "Non-Local Means Filtering"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create window by name

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name2, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name3, cv2.WINDOW_AUTOSIZE)

    # add some track bar controllers for settings

    neighbourhood = 7
    cv2.createTrackbar(
        "neighbourhood, N",
        window_name2,
        neighbourhood,
        25,
        nothing)
    searchW = 21
    cv2.createTrackbar("search area, W", window_name3, searchW, 50, nothing)
    filter_strength = 10
    cv2.createTrackbar(
        "strength, h",
        window_name3,
        filter_strength,
        25,
        nothing)

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

        # get parameters from track bars

        neighbourhood = cv2.getTrackbarPos("neighbourhood, N", window_name2)
        searchW = cv2.getTrackbarPos("search area, W", window_name3)
        filter_strength = cv2.getTrackbarPos("strength, h", window_name3)

        # check neighbourhood is greater than 3 and odd

        neighbourhood = max(3, neighbourhood)
        if not(neighbourhood % 2):
            neighbourhood = neighbourhood + 1

        # in opencv blur() performs filtering with a NxN kernel where each
        # element has a weight of 1 / (N^2) - this is mean filtering

        mean_img = cv2.blur(
            frame,
            (neighbourhood,
             neighbourhood),
            borderType=cv2.BORDER_DEFAULT)

        # perform NLM filtering on the same image

        nlm_img = cv2.fastNlMeansDenoisingColored(
            frame,
            h=filter_strength,
            hColor=10,
            templateWindowSize=neighbourhood,
            searchWindowSize=searchW)

        # display image

        cv2.imshow(window_name, frame)
        cv2.imshow(window_name2, mean_img)
        cv2.imshow(window_name3, nlm_img)

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

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
