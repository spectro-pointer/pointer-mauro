# -*- coding: UTF-8 -*-
#
#    This file is part of Pointer.

"""   
   Camera is a Camera class for the pi camera control
    - Streaming server using gstreamer-1.0
    - Still pictures
    - Settings

"""

#from __future__ import with_statement

#import socket
#import SimpleXMLRPCServer
#import threading

#import config
        
import sys
import subprocess
import time

import util_27 as util

class Camera(util.Thread):
    # FIXME: socket server is pipelined to gstreamer command (use gst/opencv2 instead)   
    
    def __init__(self, server_address = ('0.0.0.0', 5000)):   
        import picamera

        self.server_address = server_address 
        util.Thread.__init__(self)
        self.setDaemon(True)
        self.shallStop = False

        self.frameSizeX = 1920
        self.frameSizeY = 1080
    
        self.fps = 25
    
        self.video = picamera.PiCamera()

#        self.video.res = (self.frameSizeX, self.frameSizeY)
        self.video.resolution = (self.frameSizeX, self.frameSizeY) 
        self.video.framerate = self.fps
        self.video.vflip=True
        self.video.hflip=True
        self.video.exposure_mode = 'night'
        self.video.iso = 800
        
        self.start()

    def run(self):
        """ gstreamer server command line """ # FIXME: Use python gst module
        serverline = 'gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=%s port=%d' % self.server_address
        serverline = serverline.split()
        server = subprocess.Popen(serverline, stdin=subprocess.PIPE)
        self.video.start_recording(server.stdin, format='h264', bitrate=4000000, profile='high', inline_headers=True, intra_period=128)
        while not self.shallStop:
            time.sleep(1)
        try:
            self.video.stop_recording()
            server.stdin.close()
            time.sleep(.25)
            server.terminate()
        except Exception as e:
            print >>sys.stderr, 'Exception:', e
            pass
            
    def shutdown(self):
        util.Thread.shutdown(self)
    
    def serve_forever(self):
        while not self.shallStop:
            time.sleep(1)
