#####################################################################

# Example : generic example for video processing from a video file
# specified as video.avi or from an
# attached web camera and saving to a video file

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys

#####################################################################

keep_processing = True;
camera_to_use = 0; # 0 if you have one camera, 1 or > 1 otherwise

video_width = 640;
video_height = 480;

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input -> Video File"; # window name

# define video writer (video: 640 x 480 @ 25 fps)

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G');
output = cv2.VideoWriter('output.avi',fourcc, 25.0, (video_width,video_height));

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if ((cap.open("input.avi")) or (cap.open(camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # *** do any processing here ****

        # write the frame to file (first resizing)

        frame2 = cv2.resize(frame,(video_width, video_height), interpolation = cv2.INTER_CUBIC)
        output.write(frame2);

        # display image

        cv2.imshow(windowName,frame);

        # start the event loop - essential

        # set cv2.waitKey() to minimum value of 1 so that the framerate is preserved
        # for writing to video file (if we set it differently we get strange
        # speeding up effects in the output, as we are specifying 25 fps playback
        # but writing the frames at a slower rate - capture etc. takes some time).

        key = cv2.waitKey(1) & 0xFF; # wait 1ms only

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

    # close all windows

    cv2.destroyAllWindows()

    # Release everything if job is finished
    cap.release()
    output.release()

else:
    print("No video file specified or camera connected.")

#####################################################################
