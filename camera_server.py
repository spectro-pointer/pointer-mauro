# -*- coding: UTF-8 -*-
#



import BaseHTTPServer
#import hashlib
#import os
#import random
#import re
#import struct
#import sys
#import threading
import xmlrpclib
#import zlib

#import config
import util_27 as util


# prevent call to socket.getfqdn
def fast_address_string(self):
    return '%s' % self.client_address[0]
BaseHTTPServer.BaseHTTPRequestHandler.address_string = fast_address_string
del fast_address_string

def getServer(url):
    if not '://' in url:
        raise ValueError("URL must be of form [protocol]://" \
                         "[connection-string]")
    protocol, _ = url.split('://', 1)
    if protocol == 'http':
        return CameraServer(url)
    else:
        raise RuntimeError("The protocol '%s' is unsupported." % protocol)

class ServerError(IOError):
    pass

class CameraServer(util.AsyncXMLRPCServer):
    def __init__(self, camera, iface='', port=17937):
        util.AsyncXMLRPCServer.__init__(self, iface, port)
        
        self.methods['get'] = self.get
        self.methods['properties'] = self.properties
        self.methods['set'] = self.set
        self.methods['take'] = self.take
        
        self.camera = camera
        
        self.start()

    def properties(self):
        return self.camera.properties()
    
    def get(self, p):
        return self.camera.get(p)

    def set(self, p, v):
        self.camera.set(p, v)

    def take(self):
        return xmlrpclib.Binary(self.camera.takePicture())