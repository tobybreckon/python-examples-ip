# Verification Testing for OpenCV Installation

As OpenCV is a complex beast, to ensure the full installation of OpenCV is working correctly we perform the following tests.

All tested with [OpenCV](http://www.opencv.org) 3.x / 4.x and Python 3.x.

_Assumes that git and wget tools are available on the command line or that similar tools are available to access git / download files._

(_On-site at Durham University_: For testing on MS Windows, download and unzip example files from source URL as specified - [here](https://github.com/tobybreckon/python-examples-ip.git) - onto the user space J:/ drive. On Linux run the associated ``opencv ... .init`` shell script before testing.).

---

## Test #1 - check versions:

(for testing on MS Windows at Durham (DUDE system), open all ```.py``` scripts from J:/ in IDLE and run module from there)

```
git clone https://github.com/tobybreckon/python-examples-ip.git
cd python-examples-ip
python3 ./version.py
```
### Result #1:

- Text output to console such that:

```
We are using OpenCV: CCC
.. do we have the OpenCV Contrib Modules: True
.. do we have the OpenCV Non-free algorithms: True
.. do we have the Intel Performance Primitives (IPP): 
.. version: <???> (in use: True)
We are using numpy: <???>
We are using matplotlib: <???>
.. and this is in Python: PPP ??? (64 bit)

Check Video I/O (OS identifier: MMM)
... available camera backends:  LLL
... available stream backends:  LLL
... available video writer backends: LLL

Available Cuda Information:
... ['NVIDIA CUDA: YES (ver NNN, RRR)', 'NVIDIA GPU arch: ???', 'NVIDIA PTX archs: ZZZ']

GGG

DNN module CUDA backend/target availability : 
... DNN_TARGET_CUDA:            True
... DNN_TARGET_CUDA_FP16:       True
... DNN_TARGET_CPU:             True
... DNN_TARGET_OPENCL:          True
... DNN_TARGET_OPENCL_FP16:     True

OpenCL available (within OpenCV) ? : True

Available CPU Optimizations (*: build enabled; ?: not CPU supported):
... ???

```
- such that CCC >= 4.3.x (or higher), PPP > 3.x, MMM is sensible for the OS in use, each of the LLL list are sensible (may not all be identical) and ideally include FFMPEG + GSTREAMER in addition to V4L/V4L (for MMM = linux*), QT (for MMM = darwin) or DSHOW / MSMF (for MMM = win*), NNN > 10.x, ZZZ includes ``cuDNN: Yes``, GGG is sensible if a CUDA compatible GPU is present + configured and ??? = (doesn't matter). In addition, for maximum performance RRR ideally includes ``CUFFT CUBLAS FAST_MATH``.

[ N.B. to build with Non-free algorithms set OPENCV_ENABLE_NONFREE=TRUE in CMake ]

---

## Test #1a - check we have all the correct functionality:

Only to be used if building OpenCV from source (any platform) or using a pre-built version from a 3rd party repository (on Linux / Mac OS).

```
.. (as per test 1 for steps 1 + 2)
python3 ./checkbuildinfo.py
```
### Results #1a

- The resulting build element information should ideally contain the following as a subset of the configuration (where _present_ indicates a reference to a system file or a version number that tells us it is present on the system / in the build):

| build element                       | Linux | MS Windows |
|------------------------------------ | ----- | --------|
| Platform: ... Configuration:        |Release|Release|
| Built as dynamic libs:             | YES | YES |
| OpenCV modules: | contains: core flann ... imgproc ... ml ... imgcodecs ... videoio .. xfeatures2d ... dnn ... dnn_objdetect ... ximgproc ... optflow ... stitching ... **cuda** | <-- same as Linux|
|    Non-free algorithms:  | YES | YES |
| QT:                          | NO | NO |
|    GTK+ 2.x:                 |   YES | NO |
|    ZLib:                     |   present |   present |
|    JPEG:                     |   present |   present |
|    WEBP:                     |   present |   present |
|    PNG:                     |   present |   present |
|    JPEG 2000:                     |   present |   present |
|    OpenEXR:                     |   present |   present |
|    PNG:                     |   present |   present |
|   FFMPEG:                   |   YES (all sub-elements)| NO |
|   GStreamer:                   |   YES (all sub-elements)| NO |
|  V4L/V4L2:                  |   present | NO |
|    XINE:                   |    YES | NO |
|    gPhoto2:                 |   YES | NO |
| Parallel framework:         |   pthreads | ??? |
| Use IPP:                    | present | NO |
| **NVIDIA CUDA:**              |   YES ( >= 10.x) | NO |
| **OpenCL:**                   |   YES |  YES |

- elements **in bold** required for OpenCV 4.3.x and later on Linux (to enable GPU use for CNN/DNN inference via DNN module).

---

## Test #2 - check image read + window display functions:

(for MS Windows download image from [here](https://upload.wikimedia.org/wikipedia/commons/b/b4/JPEG_example_JPG_RIP_100.jpg) and save as example.jpg in directory python-examples-ip-master)

```
.. (as per test 1 for steps 1 + 2)
wget https://upload.wikimedia.org/wikipedia/commons/b/b4/JPEG_example_JPG_RIP_100.jpg
mv JPEG_example_JPG_RIP_100.jpg example.jpg
python3 ./smooth_image.py
```

### Result #2:
- image is displayed in window (a blurred version of example.jpg),
pressing 'x' closes window.

---

## Test #3 - test camera access and video write function:

```
.. (as per test 1 for steps 1 + 2)
<<< connect a usb web-cam (any web-cam)
python3 ./save_video.py -c 0
```

## Result #3:
- possible error message such as "???... ???? Unable to open source 'input.avi'" - _ignore this_.
- possible error message relating to inability to read from camera or video device (try with ``-c 1`` or greater to address different video devices)
- a window appears with live video from camera, pressing 'x' closes window and ends program (saving a video file).
-  video file saved as _output.avi_ file can be played in [vlc](http://www.vlc.org) or similar.
- Ignore _"cannot open video messages"_ from ffpmeg/xine or similar (this is it failing to open video file as alt. to camera, not write from camera).

---

## Test #4 - test video read function:

(for MS Windows download video from [here](http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4) and save as video.avi in directory python-examples-ip-master)

```
.. (as per test 1 for steps 1 + 2)
wget http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4
mv big_buck_bunny.mp4 video.avi
python3 ./capture_video.py
```

### Result #4:

- The video available at
http://camendesign.co.uk/code/video_for_everybody/test.html is played
back in a window, but with no audio.

---
