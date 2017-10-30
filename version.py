#####################################################################

# Example : test if opencv environment is working

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2017 Toby Breckon
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import numpy as np
import sys
import math
import matplotlib

#####################################################################

# check if the OpenCV we are using has the extra modules available

def extraOpenCVModulesPresent():
    (is_built, not_built) = cv2.getBuildInformation().split("Disabled:")
    return ('xfeatures2d' in is_built);

#####################################################################

print("We are using OpenCV: " + cv2.__version__);
print(".. do we have the Open CV Contrib Modules: " + str(extraOpenCVModulesPresent()));
print("We are using numpy: " + np.__version__);
print("We are using matplotlib: " + matplotlib.__version__);
print(".. and this is in Python: " + sys.version)

#####################################################################
