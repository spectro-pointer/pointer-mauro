# -*- coding: UTF-8 -*-
#



import http.server
#import hashlib
#import os
#import random
#import re
#import struct
#import sys
#import threading
#import xmlrpclib
#import zlib

#import config
#import pointer
import util


# prevent call to socket.getfqdn
def fast_address_string(self):
    return '%s' % self.client_address[0]
http.server.BaseHTTPRequestHandler.address_string = fast_address_string
del fast_address_string

def getServer(url):
    if not '://' in url:
        raise ValueError("URL must be of form [protocol]://" \
                         "[connection-string]")
    protocol, _ = url.split('://', 1)
    if protocol == 'http':
        return PointerServer(url)
    else:
        raise RuntimeError("The protocol '%s' is unsupported." % protocol)

class ServerError(IOError):
    pass

class PointerServer(util.AsyncXMLRPCServer):
    def __init__(self, pointer, iface='', port=17936):
        util.AsyncXMLRPCServer.__init__(self, iface, port)
        self.methods['move'] = self.move
        self.methods['home'] = self.home
        self.methods['point'] = self.point
        self.methods['get'] = self.get
        self.methods['set'] = self.set
        self.methods['getSpeed'] = self.getSpeed
        self.methods['setSpeed'] = self.setSpeed
        self.methods['getLatLon'] = self.getLatLon
        self.methods['setLatLon'] = self.setLatLon
        self.methods['ledOn'] = self.ledOn
        self.methods['ledOff'] = self.ledOff
        self.methods['abort'] = self.abort
        self.pointer = pointer
        self.start()

    def getSpeed(self):
        return self.pointer.getSpeed()

    def setSpeed(self, azimuth, elevation):
        self.pointer.setSpeed(azimuth, elevation)
        return True

    def abort(self):
        self.pointer.abort()
        return True

    def get(self, coords):
        return self.pointer.get(coords)
    
    def getLatLon(self):
        return self.pointer.getLatLon()

    def setLatLon(self, lat, lon):
        self.pointer.setLatLon(lat, lon)
        return True

    def ledOn(self):
        self.pointer.ledOn()
        return True

    def ledOff(self):
        self.pointer.ledOff()
        return True
    
    def set(self, coords, v1, v2):
        self.pointer.set(coords, v1, v2)
        return True
    
    def move(self, coords, v1, v2):
        self.pointer.move(coords, v1, v2)
        return True

    def home(self, coords, v1, v2):
        self.pointer.home(coords, v1, v2)
        return True
    
    def point(self, coords, v1, v2):
        self.pointer.point(coords, v1, v2)
        return True
