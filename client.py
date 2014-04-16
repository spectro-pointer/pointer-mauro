# -*- coding: UTF-8 -*-
#
#    Copyright 2013, Mauro Lacy, mauro@lacy.com.ar
#
#    This file is part of Pointer. Based on Pyrit's implementation
#
#    Pointer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pointer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pointer.  If not, see <http://www.gnu.org/licenses/>.



import http.server
#import hashlib
#import os
#import random
import re
#import struct
#import sys
#import threading
import xmlrpc.client
#import zlib

#import config
#import util


# prevent call to socket.getfqdn
def fast_address_string(self):
    return '%s' % self.client_address[0]
http.server.BaseHTTPRequestHandler.address_string = fast_address_string
del fast_address_string


URL_GROUPER = re.compile("(?P<protocol>\w+)://(((?P<user>\w+):?(?P<passwd>\w+)?@)?(?P<tail>.+))?")
XMLFAULT = re.compile("\<class '(?P<class>[\w\.]+)'\>:(?P<fault>.+)")


def handle_xmlfault(*params):
    """Decorate a function to check for and rebuild storage exceptions from
       xmlrpclib.Fault
    """

    def check_xmlfault(f):

        def protected_f(*args, **kwds):
            try:
                ret = f(*args, **kwds)
            except xmlrpc.client.Fault as e:
                # rpc does not know Exceptions so they always come as pure
                # strings. One way would be to hack into the de-marshalling.
                # These seems easier and less intrusive.
                match = XMLFAULT.match(e.faultString)
                if match is None:
                    raise
                else:
                    groups = match.groupdict()
                    cls = groups['class']
                    fault = groups['fault']
                    if cls == 'pointer.DigestError':
                        raise DigestError(fault)
                    elif cls == 'pointer.PointerError':
                        raise PointerError(fault)
                    else:
                        raise
            return ret
        protected_f.__name__ = f.__name__
        protected_f.__doc__ = f.__doc__
        return protected_f
    return check_xmlfault

def getPointerClient(url):
    if not '://' in url:
        raise ValueError("URL must be of form [protocol]://" \
                         "[connection-string]")
    protocol, _ = url.split('://', 1)
    if protocol == 'http':
        return RPCPointer(url)
    else:
        raise RuntimeError("The protocol '%s' is unsupported." % protocol)

class PointerError(IOError):
    pass


class DigestError(PointerError):
    pass


class RPCPointer(object):

    def __init__(self, url):
        self.cli = xmlrpc.client.ServerProxy(url, allow_none=True)

    @handle_xmlfault()
    def move(self, coords, v1, v2):
        """Moves."""
        return self.cli.move(coords, v1, v2)

    @handle_xmlfault()
    def home(self, coords, v1, v2):
        """Homes."""
        return self.cli.home(coords, v1, v2)
        
    @handle_xmlfault()
    def point(self, coords, v1, v2):
        """Points."""
        return self.cli.point(coords, v1, v2)
       
#    @handle_xmlfault()
    def get(self, coords):
        """Gets actual Azimuth and Elevation angles."""
        c1, c2 = self.cli.get(coords)
        return c1, c2
        
    @handle_xmlfault()
    def set(self, coords, v1, v2):
        """Sets Azimuth and Elevation."""
        return self.cli.set(coords, v1, v2)
    
    @handle_xmlfault()
    def getSpeed(self):
        """Gets actual Azimuth and Elevation speeds."""
        azimuth, elevation = self.cli.getSpeed()
        return azimuth, elevation

    @handle_xmlfault()
    def setSpeed(self, azimuth, elevation):
        """Sets Speeds."""
        return self.cli.setSpeed(azimuth, elevation)

    @handle_xmlfault()
    def getLatLon(self):
        """Gets actual Latitude and Longitude."""
        lat, lon = self.cli.getLatLon()
        return lat, lon

    @handle_xmlfault()
    def setLatLon(self, lat, lon):
        """Sets Latitude and Longitude."""
        return self.cli.setLatLon(lat, lon)

    @handle_xmlfault()
    def ledOn(self):
        """Turns the "live zero" led on."""
        return self.cli.ledOn()

    @handle_xmlfault()
    def ledOff(self):
        """Turns the "live zero" led off."""
        return self.cli.ledOff()

    @handle_xmlfault()
    def abort(self):
        """Abort in-process commands."""
        return self.cli.abort()