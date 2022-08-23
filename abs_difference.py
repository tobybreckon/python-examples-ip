#####################################################################

# Example : simple image differencing and contrast via multiplication
# from a video file specified on the command line
# (e.g. python FILE.py video_file) or from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
# Copyright (c) 2019 Dept Computer Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import argparse
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
use_greyscale = False


#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass


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
window_name2 = "Difference Image"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)

    # add some track bar controllers for settings

    contrast = 1
    cv2.createTrackbar("contrast", window_name2, contrast, 30, nothing)

    fps = 25
    cv2.createTrackbar("fps", window_name2, fps, 25, nothing)

    threshold = 0
    cv2.createTrackbar("threshold", window_name2, threshold, 255, nothing)

    # if video file or camera successfully open then read frame from video

    if (cap.isOpened):
        ret, frame = cap.read()

        # rescale if specified

        if (args.rescale != 1.0):
            frame = cv2.resize(frame, (0, 0), fx=args.rescale, fy=args.rescale)

    # make a deep copy of this (as all camera frames otherwise reside
    # in the same portion of allocated memory)

    prev_frame = frame.copy()

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

        if (use_greyscale):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # if the previous frame we stored also has 3 channels (colour)
            if (len(prev_frame.shape) == 3):
                # convert it, otherwise absdiff() will break
                prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        # performing absolute differencing between consecutive frames

        diff_img = cv2.absdiff(prev_frame, frame)

        # retrieve the contrast setting from the track bar

        contrast = cv2.getTrackbarPos("contrast", window_name2)

        # multiple the result to increase the contrast (so we can see small
        # pixel changes)

        brightened_img = diff_img * contrast

        # display images

        cv2.imshow(window_name, frame)

        # threshold the image if its in grayscale and we have a valid threshold

        threshold = cv2.getTrackbarPos("threshold", window_name2)

        if (use_greyscale and (threshold > 0)):

            # display thresholded image if threshold > 0
            # thresholding : if pixel > (threshold value) set to 255 (white),
            # otherwise set to 0 (black)

            ret, thresholded_img = cv2.threshold(
                brightened_img, 127, 255, cv2.THRESH_BINARY)
            cv2.imshow(window_name2, thresholded_img)
        else:
            # otherwise just display the non-thresholded one

            cv2.imshow(window_name2, brightened_img)

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

        fps = cv2.getTrackbarPos("fps", window_name2)
        # wait T ms (i.e. 1000ms / 25 fps = 40 ms)
        key = cv2.waitKey(int(1000 / max(1, fps))) & 0xFF

        # It can also be set to detect specific key strokes by recording which
        # key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False

        elif (key == ord('g')):

            # toggle grayscale usage (when they press 'g')

            use_greyscale = not (use_greyscale)

            # if the previous frame we stored also has 3 channels (colour)
            if (len(prev_frame.shape) != 3):
                # convert it to just copying the gray information to all of the
                # three channels (this is a hack), otherwise absdiff() will
                # break
                prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_GRAY2BGR)
        else:

            # make a deep copy of the current frame (as all camera frames
            # otherwise reside in the same portion of allocated memory)
            prev_frame = frame.copy()

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################
