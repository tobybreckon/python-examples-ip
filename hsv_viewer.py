#####################################################################

# Example : display individual HSV channels from an video file
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


colour_map_hue = False  # use colour mapping to display Hue

#####################################################################

# define video capture object

try:
    # to use a non-buffered camera stream (via a separate thread)

    if not (args.video_file):
        import camera_stream
        cap = camera_stream.CameraVideoStream(use_tapi=False)
    else:
        cap = cv2.VideoCapture()  # not needed for video files

except BaseException:
    # if not then just use OpenCV default

    print("INFO: camera_stream class not found - camera input may be buffered")
    cap = cv2.VideoCapture()

# define display window name

window_name = "Live Camera Input"  # window name
window_name_hue = "Hue Channel"  # window name
window_name_sat = "Saturation Channel"  # window name
window_name_val = "Value Channel"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create window by name (note flags for resizable or not)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # usage

    print("USAGE: press 'c' to toggle Hue channel colour mapping")

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

        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # display images

        cv2.imshow(window_name, frame)

        # colour channels are HSV ordering in OpenCV

        cv2.imshow(window_name_sat, img_hsv[:, :, 1])  # saturation
        cv2.imshow(window_name_val, img_hsv[:, :, 2])  # value

        if (colour_map_hue):
            # re map S and V to top outer rim of HSV colour space

            img_hsv[:, :, 1] = np.ones(img_hsv[:, :, 1].shape) * 255
            img_hsv[:, :, 2] = np.ones(img_hsv[:, :, 1].shape) * 255

            # convert the result back to BGR to produce a false colour
            # version of hue for display

            colour_mapped_hue = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
            cv2.imshow(window_name_hue, colour_mapped_hue)  # colour mapped hue
        else:
            cv2.imshow(window_name_hue, img_hsv[:, :, 0])  # hue

        # stop the timer and convert to ms. (to see how long processing and
        # display takes)

        stop_t = ((cv2.getTickCount() - start_t) /
                  cv2.getTickFrequency()) * 1000

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

        # wait 40ms or less depending on processing time taken (i.e. 1000ms /
        # 25 fps = 40 ms)

        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF

        # It can also be set to detect specific key strokes by recording which
        # key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False
        elif (key == ord('c')):
            colour_map_hue = not (colour_map_hue)

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################
