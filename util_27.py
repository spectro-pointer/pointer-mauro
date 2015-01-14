# -*- coding: UTF-8 -*-
#
#    This file is part of Pointer.
#    It's based on Lukas Lueg's Pyrit codebase.

"""Various utility- and backend-related classes and data for Pointer.

   Thread is a subclass of threading.Thread that adds a context-manager to
   make it 'stoppable'.

   AsyncXMLRPCServer is a stoppable (incl. 'serve_forever') subclass of
   SimpleXMLRPCServer.
   
   TelescopeServer is a TCP server for stellarium telescope control

"""

from __future__ import with_statement

#import cStringIO
#import gzip
#import os
#import Queue
#import random
import socket
import SimpleXMLRPCServer
#import sys
#import struct
import time
import threading

#import config

VERSION = "0.7"
__version__ = VERSION


class Thread(threading.Thread):
    """A stoppable subclass of threading.Thread"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.shallStop = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self.shallStop = True
        self.join()


class AsyncXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer, Thread):
    """A stoppable XMLRPCServer

       The main socket is made non-blocking so we can check on
       self.shallStop from time to time.

       Sub-classes should add (name:function)-entries to self.methods
    """

    def __init__(self, (iface, port)=('', 17934)):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, (iface, port), \
                                                        logRequests=False)
        Thread.__init__(self)
        self.setDaemon(True)
        # Make the main socket non-blocking (for accept())
        self.socket.settimeout(1)
        self.methods = {}
        self.register_instance(self)

    def run(self):
        while not self.shallStop:
            self.handle_request()

    def get_request(self):
        while not self.shallStop:
            try:
                sock, addr = self.socket.accept()
            except socket.timeout:
                pass
            else:
                # Accepted connections are made blocking again
                sock.settimeout(None)
                return sock, addr
        raise socket.timeout("Server has stopped.")

    def serve_forever(self):
        while not self.shallStop:
            time.sleep(1)

    def shutdown(self):
        Thread.shutdown(self)
        self.socket.close()

    def _dispatch(self, method, params):
        if method not in self.methods:
            raise AttributeError
        else:
            return self.methods[method](*params)

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