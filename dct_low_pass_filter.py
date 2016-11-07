#####################################################################

# Example : perform low pass filterings in DCT space of image frame
# from a video file specified on the command line (e.g. python FILE.py
# video_file) or from an attached web camera

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

#####################################################################

# create a simple low pass filter - DCT version (top left corner)

def create_low_pass_filter(width, height, radius):
    lp_filter = np.zeros((height, width), np.float32);
    cv2.circle(lp_filter, (0, 0), radius, (1,1,1), thickness=-1)
    return lp_filter

#####################################################################

# "Currently dct supports even-size arrays (2, 4, 6 ...). For data
# analysis and approximation, you can pad the array when necessary.
# Also, the function performance depends very much, and not
# monotonically, on the array size (see getOptimalDFTSize() ). In the
# current implementation DCT of a vector of size N is calculated
# via DFT of a vector of size N/2 . Thus, the optimal DCT
# size N1 >= N can be calculated as:" - OpenCV manual 3.0


def getOptimalDCTSize(N):
    return (2* cv2.getOptimalDFTSize((N+1)/2))


#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowName2 = "DCT Co-efficients Spectrum"; # window name
windowName3 = "Filtered Image"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName2, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName3, cv2.WINDOW_NORMAL);

    # if video file successfully open then read frame from video

    if (cap.isOpened):
        ret, frame = cap.read();

    # convert to grayscale

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

    # use this single frame to set up optimized DFT settings

    hieght,width = gray_frame.shape;
    nheight = getOptimalDCTSize(hieght);
    nwidth = getOptimalDCTSize(width);

    # add some track bar controllers for settings

    radius = 25;
    cv2.createTrackbar("radius", windowName2, radius, max(nheight,nwidth) * 2, nothing);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount();

         # convert to grayscale

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

        # Performance of DCT calculation, via the DFT/FFT, is better for array sizes of power of two.
        # Arrays whose size is a product of 2's, 3's, and 5's are also processed quite efficiently.
        # Hence ee modify the size of the array tothe optimal size (by padding zeros) before finding DCT.

        pad_right = nwidth - width;
        pad_bottom = nheight - hieght;
        nframe = cv2.copyMakeBorder(gray_frame,0,pad_bottom,0,pad_right,cv2.BORDER_CONSTANT, value = 0);

        # perform the DCT

        dct = cv2.dct(np.float32(nframe));

        # perform low pass filtering

        radius = cv2.getTrackbarPos("radius",windowName2);
        lp_filter = create_low_pass_filter(nwidth, nheight, radius);

        dct_filtered = cv2.multiply(dct, lp_filter);

        # recover the original image via the inverse DCT

        filtered_img = cv2.dct(dct_filtered, flags = cv2.DCT_INVERSE);

        # normalized the filtered image into 0 -> 255 (8-bit grayscale) so we can see the output

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(filtered_img);
        filtered_img_normalized = filtered_img * (1.0/(maxVal-minVal)) + ((-minVal)/(maxVal-minVal));
        filtered_img_normalized = np.uint8(filtered_img_normalized * 255);

        # calculate the DCT spectrum for visualization

        # create a 8-bit image to put the magnitude spectrum into

        dct_spectrum_normalized = np.zeros((nheight,nwidth,1), np.uint8);

        # normalized the magnitude spectrum into 0 -> 255 (8-bit grayscale) so we can see the output

        cv2.normalize(np.uint8(dct_filtered), dct_spectrum_normalized, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX);

        # display images

        cv2.imshow(windowName,gray_frame);
        cv2.imshow(windowName2,dct_spectrum_normalized);
        cv2.imshow(windowName3,filtered_img_normalized);

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


