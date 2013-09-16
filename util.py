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



#import cStringIO
#import gzip
#import os
#import Queue
#import random
import socket
import xmlrpc.server
#import sys
#import struct
import time
import threading

#import config

VERSION = "0.5"
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


class AsyncXMLRPCServer(xmlrpc.server.SimpleXMLRPCServer, Thread):
    """A stoppable XMLRPCServer

       The main socket is made non-blocking so we can check on
       self.shallStop from time to time.

       Sub-classes should add (name:function)-entries to self.methods
    """

    def __init__(self, iface='', port=17934):
        xmlrpc.server.SimpleXMLRPCServer.__init__(self, (iface, port), \
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

import socketserver
import struct

class TelescopeRequestHandler(socketserver.BaseRequestHandler):
    """Telescope Server Request Handler class"""
    def __init__(self, request, client_addr, server):
        self.maxRequestLength= 1024
        self.clientRequestLength = 20
        self.defaultType = 0

        self.pointer = server.pointer # A little trick
        
        super(TelescopeRequestHandler, self).__init__(request, client_addr, server)

    "One instance per connection."
    def handle(self):
        # self.request is the client connection
        """ Request:
            client->server:
            MessageGoto (type = 0)
            LENGTH (2 bytes,integer): length of the message
            TYPE   (2 bytes,integer): 0
            TIME   (8 bytes,integer): current time on the client computer in microseconds
                              since 1970.01.01 UT. Currently unused.
            RA     (4 bytes,unsigned integer): right ascension of the telescope (J2000)
                       a value of 0x100000000 = 0x0 means 24h=0h,
                       a value of 0x80000000 means 12h
            DEC    (4 bytes,signed integer): declination of the telescope (J2000)
                       a value of -0x40000000 means -90degrees,
                       a value of 0x0 means 0degrees,
                       a value of 0x40000000 means 90degrees
        """
        try:
            length = struct.unpack("H", self.request.recv(2))[0]
        except struct.error:
            data = self.request.recv(self.maxRequestLength)
            if len(data) == 0:
                print('Client closed connection')
                self.request.close()
                return
            else:
                print('Data of unknown format received:', data)
                self.request.close()
                return
        if length != self.clientRequestLength:
            print('Wrong message length:', length)
            self.request.close()
            return
        type = struct.unpack("H", self.request.recv(2))[0]
        if type != self.defaultType:
            print('Unknown message type:', type)
            self.request.close()
            return
        # Go ahead
        data = self.request.recv(length-4)
        t, ra, dec = struct.unpack("qIi", data)
        ra  = float(ra) / 0x80000000 * 12.
        dec = float(dec) /  0x40000000 * 90.
        print('time  :', t)
        print('RA    :', ra)
        print('Dec   :', dec)
        # Now process
        self.pointer.point2(ra, dec)
        self.request.close()

class TelescopeServer(socketserver.ThreadingMixIn, socketserver.TCPServer, Thread):
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, requestHandlerArg):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.pointer = requestHandlerArg # our pointer instance
        
        self.clientReplyLength = 24
        self.defaultType = 0
        self.defaultReplyStatus = 0     
        self.defaultUnusedTime = 0 # FIXME: set time field
        
        # Start another thread, to periodically send our current position
        Thread.__init__(self)
        self.setDaemon(True)
        # Make the main socket non-blocking (for accept())
#        self.socket.settimeout(1)
        self.start()

    def run(self):
        while not self.shallStop:
            self.sendCurrentPosition()
            time.sleep(1)
        
    def sendCurrentPosition(self):
        """ Reply
            server->client:
            MessageCurrentPosition (type = 0):
            
            LENGTH (2 bytes,integer): length of the message
            TYPE   (2 bytes,integer): 0
            TIME   (8 bytes,integer): current time on the server computer in microseconds
                       since 1970.01.01 UT. Currently unused.
            RA     (4 bytes,unsigned integer): right ascension of the telescope (J2000)
                       a value of 0x100000000 = 0x0 means 24h=0h,
                       a value of 0x80000000 means 12h
            DEC    (4 bytes,signed integer): declination of the telescope (J2000)
                       a value of -0x40000000 means -90degrees,
                       a value of 0x0 means 0degrees,
                       a value of 0x40000000 means 90degrees
            STATUS (4 bytes,signed integer): status of the telescope, currently unused.
                       status=0 means ok, status<0 means some error
        """
        ra, dec = self.pointer.get2() # Get RA and dec values [degrees]

        # Convert RA to hours
        ra = ra / 360. * 24.
        
        print('Current RA [hs] :', ra)
        print('Current Dec[deg]:', dec)
        
        # Format
        ra = int(ra / 12. * 0x80000000)
        dec = int(dec / 90. * 0x40000000)
        
        # Build reply
        reply = struct.pack("<HHqIii", self.clientReplyLength, self.defaultType, self.defaultUnusedTime, ra, dec, self.defaultReplyStatus)
        if len(reply) != self.clientReplyLength:
            print("Reply wrong length(won't send):", len(reply))
            return
#        print('reply:', sep=' ')
#        for b in reply:
#            print(hex(b), sep=' ')
#        print()
        try:
            self.socket.send(reply)
        except socket.error:
            print('Client not connected?')
            pass