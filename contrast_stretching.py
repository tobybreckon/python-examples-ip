#####################################################################

# Example : contrast stretching from a video file
# specified on the command line (e.g. python FILE.py video_file) or from an
# attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2019 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import argparse
import numpy as np
import sys

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

# basic grayscale histogram drawing in raw OpenCV using lines

# adapted from:
# https://raw.githubusercontent.com/Itseez/opencv/master/samples/python2/hist.py

def hist_lines(hist):
    h = np.ones((300, 256, 3)) * 255  # white background
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    hist = np.int32(np.around(hist))
    for x, y in enumerate(hist):
        y = y[0]
        cv2.line(h, (x, 0), (x, y), (0, 0, 0))  # black bars
    y = np.flipud(h)
    return y

#####################################################################

# define video capture object


cap = cv2.VideoCapture()

# define display window name

window_name1 = "Live Camera Input"  # window name
window_name2 = "Input Histogram"  # window name
window_name3 = "Processed Output"  # window name
window_name4 = "Output Histogram"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(window_name1, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name4, cv2.WINDOW_NORMAL)

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

        # create an empty image of the same size for the output

        output = np.empty(gray_img.shape, dtype=np.uint8)

        # perform basic contrast stretching

        # cv2.normalize() with these parameters does
        # basic constrast stretching

        cv2.normalize(
            gray_img,
            output,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX)

        # display image

        cv2.imshow(window_name1, gray_img)
        cv2.imshow(
            window_name2, hist_lines(
                cv2.calcHist(
                    [gray_img], [0], None, [256], [
                        0, 256])))
        cv2.imshow(window_name3, output)
        cv2.imshow(
            window_name4, hist_lines(
                cv2.calcHist(
                    [output], [0], None, [256], [
                        0, 256])))

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
    print("No video file specified or camera connected.")

#####################################################################
