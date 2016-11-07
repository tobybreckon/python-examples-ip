#####################################################################

# Example : perform butterworth low pass filtering in fourier space of
# image frame from a video file specified on the command line
# (e.g. python FILE.py video_file) or from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

# version 0.1

#####################################################################

import cv2
import sys
import numpy as np
import math

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

recompute_filter = True;

#####################################################################

# create a butterworth low pass filter

def create_butterworth_low_pass_filter(width, height, D, n):
    lp_filter = np.zeros((height, width, 2), np.float32);
    centre = (width / 2, height / 2);

    # based on the forumla in lecture 8 (2015 version)
	# see also HIPR2 on-line

    for i in range(0, lp_filter.shape[1]): # image width
        for j in range(0, lp_filter.shape[0]): # image height
            radius = max(1, math.sqrt(math.pow((i - centre[0]), 2.0) + math.pow((j - centre[1]), 2.0)));
            lp_filter[j,i] = 1 / (1 + math.pow((radius / D), (2 * n)));

    return lp_filter


#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# to signal we need to reconstruct the filter

def reset_butterworth_filter(_):
    global recompute_filter;
    recompute_filter = True;
    return;

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowName2 = "Fourier Magnitude Spectrum"; # window name
windowName3 = "Filtered Image"; # window name
windowName4 = "Butterworth Filter"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName2, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName3, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName4, cv2.WINDOW_NORMAL);

    # add some track bar controllers for settings

    radius = 5;
    cv2.createTrackbar("radius", windowName4, radius, 100, reset_butterworth_filter);
    order = 1;
    cv2.createTrackbar("order", windowName4, order, 10, reset_butterworth_filter);

    # if video file successfully open then read frame from video

    if (cap.isOpened):
        ret, frame = cap.read();

    # convert to grayscale

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    # use this single frame to set up optimized DFT settings

    hieght,width = gray_frame.shape;
    nheight = cv2.getOptimalDFTSize(hieght);
    nwidth = cv2.getOptimalDFTSize(width);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount();

         # convert to grayscale

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

        # Performance of DFT calculation, via the FFT, is better for array sizes of power of two.
        # Arrays whose size is a product of 2's, 3's, and 5's are also processed quite efficiently.
        # Hence ee modify the size of the array tothe optimal size (by padding zeros) before finding DFT.

        pad_right = nwidth - width;
        pad_bottom = nheight - hieght;
        nframe = cv2.copyMakeBorder(gray_frame,0,pad_bottom,0,pad_right,cv2.BORDER_CONSTANT, value = 0);

        # perform the DFT and get complex output

        dft = cv2.dft(np.float32(nframe),flags = cv2.DFT_COMPLEX_OUTPUT);

        # shift it so that we the zero-frequency, F(0,0), DC component to the center of the spectrum.

        dft_shifted = np.fft.fftshift(dft);

        # perform low pass filtering

        radius = cv2.getTrackbarPos("radius",windowName4);
        order = cv2.getTrackbarPos("order",windowName4);

        # butterworth is slow to construct so only do it when needed (i.e. trackbar changes)

        if (recompute_filter):
            lp_filter = create_butterworth_low_pass_filter(nwidth, nheight, radius, order);
            recompute_filter = False;

        dft_filtered = cv2.mulSpectrums(dft_shifted, lp_filter, flags=0);

        # shift it back to original quaderant ordering

        dft = np.fft.fftshift(dft_filtered);

        # recover the original image via the inverse DFT

        filtered_img = cv2.dft(dft, flags = cv2.DFT_INVERSE);

        # normalized the filtered image into 0 -> 255 (8-bit grayscale) so we can see the output

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(filtered_img[:,:,0]);
        filtered_img_normalized = filtered_img[:,:,0] * (1.0/(maxVal-minVal)) + ((-minVal)/(maxVal-minVal));
        filtered_img_normalized = np.uint8(filtered_img_normalized * 255);

        # calculate the magnitude spectrum and log transform + scale it for visualization

        magnitude_spectrum = np.log(cv2.magnitude(dft_filtered[:,:,0],dft_filtered[:,:,1]));

        # create a 8-bit image to put the magnitude spectrum into

        magnitude_spectrum_normalized = np.zeros((nheight,nwidth,1), np.uint8);

        # normalized the magnitude spectrum into 0 -> 255 (8-bit grayscale) so we can see the output

        cv2.normalize(np.uint8(magnitude_spectrum), magnitude_spectrum_normalized, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX);

        # display images

        cv2.imshow(windowName,gray_frame);
        cv2.imshow(windowName2,magnitude_spectrum_normalized);
        cv2.imshow(windowName3,filtered_img_normalized);
        cv2.imshow(windowName4,lp_filter[:,:,0] * 255);

        # stop timer and convert to ms. (to see how long processing and display takes)

        stop_t = ((cv2.getTickCount() - start_t)/cv2.getTickFrequency()) * 1000;

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        # here we use a wait time in ms. that takes account of processing time already used in the loop

        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################


