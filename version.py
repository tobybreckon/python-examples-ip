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
import re
import struct
import math
import matplotlib

#####################################################################

# check if the OpenCV we are using has the extra modules available


def extraOpenCVModulesPresent():
    (is_built, not_built) = cv2.getBuildInformation().split("Disabled:")
    return ('xfeatures2d' in is_built)


def nonFreeAlgorithmsPresent():
    (before, after) = cv2.getBuildInformation().split("Non-free algorithms:")
    output_list = after.split("\n")
    return ('YES' in output_list[0])

#####################################################################

print()
print("We are using OpenCV: " + cv2.__version__)
print(".. do we have the OpenCV Contrib Modules: " +
      str(extraOpenCVModulesPresent()))
print(".. do we have the OpenCV Non-free algorithms: " +
      str(nonFreeAlgorithmsPresent()))
print("We are using numpy: " + np.__version__)
print("We are using matplotlib: " + matplotlib.__version__)
print(".. and this is in Python: " + sys.version +
      " (" + str(struct.calcsize("P") * 8) + " bit)")

#####################################################################

print()
print("Check Video I/O (OS identifier: " + sys.platform + ")")
print("Available camera backends: ", end='')
for backend in cv2.videoio_registry.getCameraBackends():
    print(" " + cv2.videoio_registry.getBackendName(backend), end='')
print()
print("Available stream backends: ", end='')
for backend in cv2.videoio_registry.getStreamBackends():
    print(" " + cv2.videoio_registry.getBackendName(backend), end='')
print()
print("Available video writer backends: ", end='')
for backend in cv2.videoio_registry.getWriterBackends():
    print(" " + cv2.videoio_registry.getBackendName(backend), end='')
print()
print()

#####################################################################

# credit to: https://tinyurl.com/y529vzc3

print("Available Cuda Information: ")
cuda_info = [re.sub('\s+', ' ', ci.strip()) for ci in \
            cv2.getBuildInformation().strip().split('\n') \
            if len(ci) > 0 and re.search(r'(nvidia*:?)|(cuda*:)|(cudnn*:)', \
            ci.lower()) is not None]
print(cuda_info)
print()

print("OpenCL available (within OpenCV) ? : " + str(cv2.ocl.haveOpenCL()))
print()
#####################################################################
