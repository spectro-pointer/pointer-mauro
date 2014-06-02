#!/usr/bin/env python

#include "opencv/cv.h"
#include "opencv/highgui.h"
import sys
import cv2 as cv

def capture():
    vcap = cv.VideoCapture()
#    image = cv.Mat;

    videoStreamAddress = "rtsp://pi:8554/"
     
    """
        it may be an address of an mjpeg stream, 
        e.g. "http://user:pass@cam_address:8081/cgi/mjpg/mjpg.cgi?.mjpg"
    """

    """"open the video stream and make sure it's opened """
    if not vcap.open(videoStreamAddress):
        print "Error opening video stream or file"
        sys.exit(-1);

    """
        Create output window for displaying frames. 
        It's important to create this window outside of the `for` loop
        Otherwise this window will be created automatically each time you call
        `imshow(...)`, which is very inefficient.
    """ 
    cv.namedWindow("Output Window")

    while True:
        ret, image = vcap.read()
        if not ret:
            print "No frame"
            cv.waitKey()
        cv.imshow("Output Window", image)
        if cv.waitKey(1) >= 0:
            break

if __name__ == "__main__":
   capture()
