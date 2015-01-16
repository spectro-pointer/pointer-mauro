""" A video abstraction module """

import sys
import io
try:
    import picamera
except:
    print >>sys.stderr, "Warning: picamera module not found"
    pass
import cv2
import numpy as np
      
class Video():
    """
        Video class
            - Webcam/Picamera/Video stream abstraction
            - QtGui output format support
    """
    def __init__(self, stream, res=None):
        self.piCamera=False
        if stream == 'picamera':
            self.capture = picamera.PiCamera()
            if res:
                self.capture.resolution = res
            self.capture.hflip = True
            self.capture.vflip = True
            self.piCamera = True
        else:
            self.capture = cv2.VideoCapture()
            if not self.capture.open(stream):
                print >>sys.stderr, "Error: video stream or device open failed"
                sys.exit(-1);
        self.currentFrame=np.array([])

    def captureNextFrame(self):
        """ 
            Capture frame, reverse RBG BGR, and return opencv image                                                                         
        """
        ret = False
        readFrame = None
        if self.piCamera:
            ret, readFrame=self.readPicamera()
        else:
            ret, readFrame=self.capture.read()
        if(ret):
            self.currentFrame=cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
        else:
            print >>sys.stderr, 'Warning: no frame'
            return None
        return readFrame
    
    def readPicamera(self):
        """ 
            Read a single frame from the camera and return the data as an OpenCV
            image (which is a numpy array).
        """
        # This code is based on the picamera example at:
        # http://picamera.readthedocs.org/en/release-1.0/recipes1.html#capturing-to-an-opencv-object
        # Capture a frame from the camera.
        data = io.BytesIO()
        try:
            self.capture.capture(data, format='jpeg', use_video_port=True)
        except Exception as e:
            print >>sys.stderr, 'Exception: readPiCamera():', e
            return False, None
        data = np.fromstring(data.getvalue(), dtype = np.uint8)
        # Decode the image data and return an OpenCV image.
        readFrame = cv2.imdecode(data, 1)
        return True, readFrame