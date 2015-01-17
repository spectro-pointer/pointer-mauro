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
import io

import util_27 as util

try:
    import picamera
except:
    print >>sys.stderr, "Warning: picamera module not found.\n"

class Camera(util.Thread):
    # FIXME: socket server is pipelined to gstreamer command (use gst/opencv2 instead)   
    def __init__(self, server_address = ('0.0.0.0', 5000)):   
        self.server_address = server_address 
        util.Thread.__init__(self)
        self.setDaemon(True)
        self.shallStop = False

        self.frameSizeX = 1920
        self.frameSizeY = 1080
    
        self.fps = 25
    
        self.video = picamera.PiCamera()

        self.video.led = False
        
        self.video.resolution = (self.frameSizeX, self.frameSizeY) 
        self.video.framerate = self.fps
        
        self.video.vflip=True
        self.video.hflip=True
        
        self.video.exposure_mode = 'night'
#        self.video.exposure_mode = 'auto'
#        self.video.iso = 0
#        self.video.iso = 800
        self.video.iso = 1600

        self.getters = [m[5:] for m in dir(self.video) if m.find('_get_') == 0]
        self.setters = [m[5:] for m in dir(self.video) if m.find('_set_') == 0]

        self.recording = False
        self.start()

    def run(self):
        """ gstreamer server command line """ # FIXME: Use python gst module
        serverline = 'gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=%s port=%d' % self.server_address
        serverline = serverline.split()
        self.server = subprocess.Popen(serverline, stdin=subprocess.PIPE)
        self.startRecording()
        while not self.shallStop:
            time.sleep(1)
        try:
            self.stopRecording()
            self.server.stdin.close()
            time.sleep(.25)
            self.server.terminate()
            self.video.close()
        except Exception as e:
            print >>sys.stderr, 'Exception:', e
            pass
            
    def shutdown(self):
        util.Thread.shutdown(self)
    
    def serve_forever(self):
        while not self.shallStop:
            time.sleep(1)
            
    def startRecording(self):
        self.video.start_recording(self.server.stdin, format='h264', bitrate=4000000, profile='high', inline_headers=True, intra_period=128)
        self.recording = True
            
    def stopRecording(self):
        self.video.stop_recording()
        self.recording = False
        
    def get(self, prop):
        if prop in self.getters:
            print 'get property %s:' % prop,
            v = eval('self.video._get_%s()' % prop)
            print v
            return v
        else:
            print
            raise Exception("Invalid property '%s'." % prop)

    def set(self, prop, value):
        if prop in self.setters:
            print 'set property %s:' % prop, value
            r = False
            try:
                eval('self.video._set_%s(%s)' % (prop, value))
            except picamera.PiCameraRuntimeError as e:
                print e, ': stopping recording and retrying.'
                r = self.recording
                self.stopRecording()
                eval('self.video._set_%s(%s)' % (prop, value))
            if r:
                self.startRecording()
        else:
            raise Exception("Invalid property '%s'." % prop)
    
    def takePicture(self):
        r = False
        try:
            self.video._check_recording_stopped()
        except picamera.PiCameraRuntimeError as e:
            print e, 'stopping recording.'
            r = self.recording
            self.stopRecording()
        self.video.resolution = (2592, 1944) # Full still port resolution
        picture = io.BytesIO()
        self.video.capture(picture, format='jpeg', use_video_port=False, resize=None, quality=85)
        self.video.resolution = (self.frameSizeX, self.frameSizeY)
        if (r):
            self.startRecording()
        return picture.getvalue()