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

from __future__ import with_statement

import BaseHTTPServer
#import hashlib
#import os
#import random
import re
#import struct
#import sys
#import threading
import xmlrpclib
#import zlib

#import config
#import util


# prevent call to socket.getfqdn
def fast_address_string(self):
    return '%s' % self.client_address[0]
BaseHTTPServer.BaseHTTPRequestHandler.address_string = fast_address_string
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
            except xmlrpclib.Fault, e:
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
                    if cls == 'cpyrit.storage.DigestError':
                        raise DigestError(fault)
                    elif cls == 'cpyrit.storage.StorageError':
                        raise PointerError(fault)
                    else:
                        raise
            return ret
        protected_f.func_name = f.func_name
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
        self.cli = xmlrpclib.ServerProxy(url)

    @handle_xmlfault()
    def getStats(self):
        return self.cli.getStats()

    @handle_xmlfault()
    def moveAzEl(self, azimuth, elevation):
        """Moves."""
        return self.cli.moveAzEl(azimuth, elevation)