#####################################################################

# Example : JPEG compression as processing on frames from a video file
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
window_name2 = "JPEG compression noise"  # window name
window_name_jpeg = "JPEG compressed version"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create window by name (note flags for resizable or not)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name_jpeg, cv2.WINDOW_NORMAL)

    jpeg_quality = 90
    cv2.createTrackbar("JPEG quality",
                       window_name2, jpeg_quality, 100, nothing)

    amplification = 0
    cv2.createTrackbar(
        "amplification",
        window_name2,
        amplification,
        255,
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

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount()

        # write/compress and then read back from as JPEG

        jpeg_quality = cv2.getTrackbarPos("JPEG quality", window_name2)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]

        # either via file output / input

        # cv2.imwrite("camera.jpg", frame, encode_param)
        # jpeg_img = cv2.imread("camera.jpg")

        # or via encoding / decoding in a memory buffer

        retval, buffer = cv2.imencode(".JPG", frame, encode_param)
        jpeg_img = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)

        # compute absolute difference between original and compressed version

        diff_img = cv2.absdiff(jpeg_img, frame)

        # retrieve the amplification setting from the track bar

        amplification = cv2.getTrackbarPos("amplification", window_name2)

        # multiple the result to increase the amplification (so we can see
        # small pixel changes)

        amplified_diff_img = diff_img * amplification

        # display images

        cv2.imshow(window_name, frame)
        cv2.imshow(window_name2, amplified_diff_img)
        cv2.imshow(window_name_jpeg, jpeg_img)

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

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################
