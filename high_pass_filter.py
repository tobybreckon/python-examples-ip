#####################################################################

# Example : perform high pass filterings in fourier space of image frame
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

# ignore divide by zero errors in np.log() operations

np.seterr(divide='ignore')

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

# create a simple high pass filter

def create_high_pass_filter(width, height, radius):
    hp_filter = np.ones((height, width, 2), np.float32)
    cv2.circle(hp_filter, (int(width / 2), int(height / 2)),
               radius, (0, 0, 0), thickness=-1)
    return hp_filter


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
window_name2 = "Fourier Magnitude Spectrum"  # window name
window_name3 = "Filtered Image"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)

    # add some track bar controllers for settings

    radius = 25
    cv2.createTrackbar("radius", window_name2, radius, 200, nothing)

    # if video file or camera successfully open then read frame from video

    if (cap.isOpened):
        ret, frame = cap.read()

        # rescale if specified

        if (args.rescale != 1.0):
            frame = cv2.resize(frame, (0, 0), fx=args.rescale, fy=args.rescale)

    # convert to grayscale

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # use this single frame to set up optimized DFT settings

    hieght, width = gray_frame.shape
    nheight = cv2.getOptimalDFTSize(hieght)
    nwidth = cv2.getOptimalDFTSize(width)

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

        # Performance of DFT calculation, via the FFT, is better for array
        # sizes of power of two. Arrays whose size is a product of
        # 2's, 3's, and 5's are also processed quite efficiently.
        # Hence we modify the size of the array to the optimal size (by padding
        # zeros) before finding DFT.

        pad_right = nwidth - width
        pad_bottom = nheight - hieght
        nframe = cv2.copyMakeBorder(
            gray_frame,
            0,
            pad_bottom,
            0,
            pad_right,
            cv2.BORDER_CONSTANT,
            value=0)

        # perform the DFT and get complex output

        dft = cv2.dft(np.float32(nframe), flags=cv2.DFT_COMPLEX_OUTPUT)

        # shift it so that we the zero-frequency, F(0,0), DC component to the
        # center of the spectrum.

        dft_shifted = np.fft.fftshift(dft)

        # perform high pass filtering

        radius = cv2.getTrackbarPos("radius", window_name2)
        hp_filter = create_high_pass_filter(nwidth, nheight, radius)

        dft_filtered = cv2.mulSpectrums(dft_shifted, hp_filter, flags=0)

        # shift it back to original quaderant ordering

        dft = np.fft.fftshift(dft_filtered)

        # recover the original image via the inverse DFT

        filtered_img = cv2.dft(dft, flags=cv2.DFT_INVERSE)

        # normalized the filtered image into 0 -> 255 (8-bit grayscale) so we
        # can see the output

        min_val, max_val, min_loc, max_loc = \
            cv2.minMaxLoc(filtered_img[:, :, 0])
        filtered_img_normalized = filtered_img[:, :, 0] * (
            1.0 / (max_val - min_val)) + ((-min_val) / (max_val - min_val))
        filtered_img_normalized = np.uint8(filtered_img_normalized * 255)

        # calculate the magnitude spectrum and log transform + scale it for
        # visualization

        magnitude_spectrum = np.log(cv2.magnitude(
            dft_filtered[:, :, 0], dft_filtered[:, :, 1]))

        # create a 8-bit image to put the magnitude spectrum into

        magnitude_spectrum_normalized = np.zeros(
            (nheight, nwidth, 1), np.uint8)

        # normalized the magnitude spectrum into 0 -> 255 (8-bit grayscale) so
        # we can see the output

        cv2.normalize(
            np.uint8(magnitude_spectrum),
            magnitude_spectrum_normalized,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX)

        # display images

        cv2.imshow(window_name, gray_frame)
        cv2.imshow(window_name2, magnitude_spectrum_normalized)
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
