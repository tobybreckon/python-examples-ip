#####################################################################

# Example : generic example for video processing from a video file
# specified as video.avi or from an
# attached web camera and saving to a video file

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
args = parser.parse_args()

video_width = 640
video_height = 480

#####################################################################

# define video capture object

cap = cv2.VideoCapture()

# define display window name

window_name = "Live Camera Input -> Video File"  # window name

# define video writer (video: 640 x 480 @ 25 fps)

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
output = cv2.VideoWriter('output.avi', fourcc, 25.0,
                         (video_width, video_height))

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if ((cap.open("input.avi")) or (cap.open(args.camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

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

        # *** do any processing here ****

        # write the frame to file (first resizing)

        frame2 = cv2.resize(
            frame,
            (video_width,
             video_height),
            interpolation=cv2.INTER_CUBIC)
        output.write(frame2)

        # display image

        cv2.imshow(window_name, frame)

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

        key = cv2.waitKey(1) & 0xFF  # wait 1ms only

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False

    # close all windows

    cv2.destroyAllWindows()

    # Release everything if job is finished
    cap.release()
    output.release()

else:
    print("No video file specified or camera connected.")

#####################################################################
