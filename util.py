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
        self.clientReplyLength = 24
        self.defaultReplyStatus = 0
        self.defaultType = 0
        self.defaultUnusedTime = 0 # FIXME: set time field

        self.pointer = server.pointerInstance # A little trick
        
        """ Earth rotation compensation """
        self.cv = threading.Condition()
        self.rotationInterval = 10. # [seconds]
        self.ra = 0.
        self.dec = 0.

        super(TelescopeRequestHandler, self).__init__(request, client_addr, server)

    def earthRotation(self):
        """ 
            Earth's rotation compensation
            One turn in 24 hs.
        """
        print('earthRotation starts')
        while True:
            print('RA (earth):', self.ra)
            print('Dec(earth):', self.dec)
            with self.cv:
                if self.ra or self.dec:
                    self.pointer.point2(self.ra, self.dec)
            time.sleep(self.rotationInterval)

    "One instance per connection."
    def handle(self):
        # self.request is the client connection
        """Start a new thread to keep sending our position."""
        t1 = threading.Thread(target = self.sendCurrentPosition)
#        if self.daemon_threads:
#            t2.setDaemon (1)
        t1.start()
        
#        """Start a new thread to compensate Earth's rotation."""
        t2 = threading.Thread(target = self.earthRotation)
#        if self.daemon_threads:
##            t2.setDaemon(1)
        t2.start()

        # TODO: homing-in at (first?) connection time (blocking)
        # (or, at start up).
        
        """Use this thread to process incoming requests."""
        self.processGoToRequest()

    def processGoToRequest(self):
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
        while True:
            try:
                length = struct.unpack("H", self.request.recv(2))[0]
            except struct.error:
                data = self.request.recv(self.maxRequestLength)
                if len(data) == 0:
                    print('Client closed connection')
                    self.request.close()
                    return
                else:
                    print('Data of unknown format received(ignoring):', data)
#                    self.request.close()
#                    return
#                    time.sleep(1)
                    continue
            if length != self.clientRequestLength:
                print('Wrong message length(ignoring):', length)
#                self.request.close()
#                return
                continue
            type = struct.unpack("H", self.request.recv(2))[0]
            if type != self.defaultType:
                print('Unknown message type(ignoring):', type)
#                self.request.close()
#                return
                continue
            # Go ahead
            data = self.request.recv(length-4)
            t, ra, dec = struct.unpack("qIi", data)
            ra  = float(ra) / 0x80000000 * 12.
            dec = float(dec) /  0x40000000 * 90.
            # Now process
            with self.cv:
                print('Time(target)    :', t)
                print('RA (target)[deg]:', ra)
                print('Dec(target)[deg]:', dec)
                self.pointer.point2(ra, dec)
                # Wait for until it arrives...
                time.sleep(1)
                while self.pointer.is_moving():
                    ra2, dec2 = self.pointer.get2()
                    print('RA (waiting)[deg]:', ra2)
                    print('Dec(waiting)[deg] :', dec2)
                    time.sleep(1)
                # Update fixed position
                self.ra = ra
                self.dec = dec
                print('RA (updated)[deg]:', self.ra)
                print('Dec(updated)[deg]:', self.dec)
#            self.request.close()
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
        while True:            
            ra, dec = self.pointer.get2() # Get RA and dec values [degrees]
#            print('RA (current)[deg]:', ra)
#            print('Dec(current)[deg]:', dec)

            # Convert RA to hours
            ra = ra / 360. * 24.
                
            # Format
            ra = int(ra / 12. * 0x80000000)
            dec = int(dec / 90. * 0x40000000)
        
            # Build reply
            reply = struct.pack("<HHqIii", self.clientReplyLength, self.defaultType, self.defaultUnusedTime, ra, dec, self.defaultReplyStatus)
            if len(reply) != self.clientReplyLength:
                print("Reply has wrong length(won't send):", len(reply))
                continue
#        print('reply:', sep=' ')
#        for b in reply:
#            print(hex(b), sep=' ')
#        print()
            try:
                self.request.send(reply)
            except socket.error as msg:
                print('Socket error:', msg)
                self.request.close()
                return
            time.sleep(.5)

class TelescopeServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, requestHandlerArg):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.pointerInstance = requestHandlerArg # our pointer instance
