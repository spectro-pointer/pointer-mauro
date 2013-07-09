# -*- coding: UTF-8 -*-
#

from __future__ import with_statement

import BaseHTTPServer
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
BaseHTTPServer.BaseHTTPRequestHandler.address_string = fast_address_string
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
        util.AsyncXMLRPCServer.__init__(self, (iface, port))
        self.methods['moveAzEl'] = self.moveAzEl
        self.methods['pointAz'] = self.pointAz
        self.methods['pointEl'] = self.pointEl
        self.methods['pointAzEl'] = self.pointAzEl
        self.methods['getAzEl'] = self.getAzEl
        self.methods['setAz'] = self.setAz
        self.methods['setEl'] = self.setEl
        self.methods['setAzEl'] = self.setAzEl
        self.pointer = pointer
        self.start()
    def moveAzEl(self, azimuth, elevation):
        self.pointer.moveAzEl(azimuth, elevation)
        return True
    
    def pointAz(self, azimuth):
        self.pointer.pointAz(azimuth)
        return True
    def pointEl(self, elevation):
        self.pointer.pointEl(elevation)
        return True
    def pointAzEl(self, azimuth, elevation):
        self.pointer.pointAzEl(azimuth, elevation)
        return True
    
    def getAzEl(self):
        return self.pointer.getAzEl()
    
    def setAz(self, azimuth):
        self.pointer.setAz(azimuth)
        return True
    def setEl(self, elevation):
        self.pointer.setEl(elevation)
        return True
    def setAzEl(self, azimuth, elevation):
        self.pointer.setAzEl(azimuth, elevation)
        return True