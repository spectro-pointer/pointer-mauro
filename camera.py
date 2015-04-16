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

        self.video = picamera.PiCamera()
        
        self.video.resolution = (1920, 1080) 
        self.video.framerate = 25

        
        self.video.vflip=True
        self.video.hflip=True
        
        self.video.led = False

        self.video.exposure_mode = 'auto'
#        self.video.exposure_mode = 'night'
        
        self.video.iso = 0
#        self.video.iso = 800

        self.getters = {}
        self.setters = {}
        for m in dir(self.video):
            prefix = m[:5]
            suffix = m[5:]
            if prefix == '_get_':
                self.getters[suffix] = eval('self.video.%s' % m)
            elif prefix == '_set_':
                self.setters[suffix] = eval('self.video.%s' % m)

        self.defaults = {}            
        for k in self.getters.keys():
            try:
                self.defaults[k] = str(self.getters[k]())
            except TypeError:
                self.defaults[k] = 'N/A'
                pass
            except picamera.PiCameraRuntimeError:
                self.defaults[k] = 'N/A'
                pass
            except NotImplementedError:
                self.defaults[k] = 'N/A'
                pass
            print '%s:' % k, self.defaults[k]
            
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

    def properties(self):
        return [(p, p in self.getters.keys(), p in self.setters.keys(), self.defaults[p] if p in self.getters.keys() else '-') for p  in set(self.getters.keys() + self.setters.keys())]
        
    def get(self, prop):
        try:
            print 'get property %s:' % prop,
            v = self.getters[prop]()
            print v
#            if isinstance(v, picamera.camera.PiCameraFraction):
#                return float.__div__(*map(float, picamera.camera.to_rational(v)))
#            return v
            return str(v)
        except KeyError:
            print
            raise Exception("Invalid property '%s'." % prop)

    def set(self, prop, value):
        r = False
        try:
            print 'set property %s:' % prop, value
            self.setters[prop](eval(value)) # tuples support
        except NameError:
            self.setters[prop](value)
        except picamera.PiCameraRuntimeError as e:
            print e, ': stopping recording and retrying.'
            r = self.recording
            self.stopRecording()
            self.setters[prop](eval(value))
            if r:
                self.startRecording()
        except KeyError:
            raise Exception("Invalid property '%s'." % prop)
    
    def takePicture(self):
        r = False
        try:
            self.video._check_recording_stopped()
        except picamera.PiCameraRuntimeError as e:
            print e, 'stopping recording.'
            r = self.recording
            self.stopRecording()
#        self.video.resolution = (2592, 1944) # Full still port resolution
        picture = io.BytesIO()
        self.video.capture(picture, format='jpeg', use_video_port=False, resize=None, quality=85)
#        self.video.resolution = (1920, 1080)
        if r:
            self.startRecording()
        return picture.getvalue()
