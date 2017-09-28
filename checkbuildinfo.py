#####################################################################

# Example : display the build options for OpenCV

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2017 Toby Breckon
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2

print("You are using OpenCV: " + cv2.__version__);
print();
print("OpenCV is built using the following options:")
print(cv2.getBuildInformation());

#####################################################################
