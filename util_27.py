# -*- coding: UTF-8 -*-
#
#    This file is part of Pointer.
#    Based on Lukas Lueg's Pyrit codebase.

"""Various utility- and backend-related classes and data for Pointer.
   Python 2.7 version.

   Thread is a subclass of threading.Thread that adds a context-manager to
   make it 'stoppable'.

   AsyncXMLRPCServer is a stoppable (incl. 'serve_forever') subclass of
   SimpleXMLRPCServer.  
   
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