# Verification Testing for OpenCV Installation

As OpenCV is a complex beast, to ensure the full installation of OpenCV is working correctly we perform the following tests.

All tested with [OpenCV](http://www.opencv.org) 3.x and Python 3.x.

_Assumes that git and wget tools are available on the command line or that similar tools are available to access git / download files._

For testing on MS Windows, download example files from source URL as specified.

---

## Test #1 - check versions:

```
git clone https://github.com/tobybreckon/python-examples-ip.git
cd python-examples-ip
python3 ./version.py
```
### Result #1:

- Text output to console such that:

```
We are using OpenCV: CCC
We are using numpy: <???>
We are using matplotlib: <???>
.. and this is in Python: PPP
```
- such that CCC >= 3.3.x (or higher); PPP > 3.x; ??? = (doesn't matter)

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
| OpenCV modules: | contains: core flann ... imgproc ... ml ... imgcodecs ... videoio .. xfeatures2d ... ximgproc ... optflow ... stitching | <-- same as Linux|
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

---

## Test #2 - check image read + window display functions:

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
python3 ./save_video.py
```

## Result #3:
- a window appears with live video from camera, pressing 'x' closes window and ends program (saving a video file).
-  video file saved as _output.avi_ file can be played in [vlc](http://www.vlc.org) or similar.
- Ignore _"cannot open video messages"_ from ffpmeg/xine or similar (this is it failing to open video file as alt. to camera, not write from camera).

---

## Test #4 - test video read function:

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
