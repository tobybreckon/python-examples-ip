#####################################################################

# Example : perform low pass filterings in DCT space of image frame
# from a video file specified on the command line (e.g. python FILE.py
# video_file) or from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2019 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import argparse
import sys
import numpy as np
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

# create a simple low pass filter - DCT version (top left corner)

def create_low_pass_filter(width, height, radius):
    lp_filter = np.zeros((height, width), np.float32)
    cv2.circle(lp_filter, (0, 0), radius, (1, 1, 1), thickness=-1)
    return lp_filter

#####################################################################

# "Currently dct supports even-size arrays (2, 4, 6 ...). For data
# analysis and approximation, you can pad the array when necessary.
# Also, the function performance depends very much, and not
# monotonically, on the array size (see getOptimalDFTSize() ). In the
# current implementation DCT of a vector of size N is calculated
# via DFT of a vector of size N/2 . Thus, the optimal DCT
# size N1 >= N can be calculated as:" - OpenCV manual 3.0


def get_optimal_dct_size(n):
    return (2 * cv2.getOptimalDFTSize(math.floor((n + 1) / 2)))


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
window_name2 = "DCT Co-efficients Spectrum"  # window name
window_name3 = "Filtered Image"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)

    # if video file or camera successfully open then read frame from video

    if (cap.isOpened):
        ret, frame = cap.read()

        # rescale if specified

        if (args.rescale != 1.0):
            frame = cv2.resize(frame, (0, 0), fx=args.rescale, fy=args.rescale)

    # convert to grayscale

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # use this single frame to set up optimized DFT settings

    height, width = gray_frame.shape
    nheight = get_optimal_dct_size(height)
    nwidth = get_optimal_dct_size(width)

    # add some track bar controllers for settings

    radius = 25
    cv2.createTrackbar(
        "radius", window_name2, radius, max(
            nheight, nwidth) * 2, nothing)

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

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount()

        # convert to grayscale

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Performance of DCT calculation, via the DFT/FFT, is better for array
        # sizes of power of two. Arrays whose size is a product of 2's, 3's,
        # and 5's are also  processed quite efficiently.
        # Hence we modify the size of the array tothe optimal size (by padding
        # zeros) before finding DCT.

        pad_right = nwidth - width
        pad_bottom = nheight - height
        nframe = cv2.copyMakeBorder(
            gray_frame,
            0,
            pad_bottom,
            0,
            pad_right,
            cv2.BORDER_CONSTANT,
            value=0)

        # perform the DCT

        dct = cv2.dct(np.float32(nframe))

        # perform low pass filtering

        radius = cv2.getTrackbarPos("radius", window_name2)
        lp_filter = create_low_pass_filter(nwidth, nheight, radius)

        dct_filtered = cv2.multiply(dct, lp_filter)

        # recover the original image via the inverse DCT

        filtered_img = cv2.dct(dct_filtered, flags=cv2.DCT_INVERSE)

        # normalized the filtered image into 0 -> 255 (8-bit grayscale) so we
        # can see the output

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(filtered_img)
        filtered_img_normalized = filtered_img * \
            (1.0 / (max_val - min_val)) + ((-min_val) / (max_val - min_val))
        filtered_img_normalized = np.uint8(filtered_img_normalized * 255)

        # calculate the DCT spectrum for visualization

        # create a 8-bit image to put the magnitude spectrum into

        dct_spectrum_normalized = np.zeros((nheight, nwidth, 1), np.uint8)

        # normalized the magnitude spectrum into 0 -> 255 (8-bit grayscale) so
        # we can see the output

        cv2.normalize(
            np.uint8(dct_filtered),
            dct_spectrum_normalized,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX)

        # display images

        cv2.imshow(window_name, gray_frame)
        cv2.imshow(window_name2, dct_spectrum_normalized)
        cv2.imshow(window_name3, filtered_img_normalized)

        # stop timer and convert to ms. (to see how long processing and display
        # takes)

        stop_t = ((cv2.getTickCount() - start_t) /
                  cv2.getTickFrequency()) * 1000

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

        # here we use a wait time in ms. that takes account of processing time
        # already used in the loop

        # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)
        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF

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
