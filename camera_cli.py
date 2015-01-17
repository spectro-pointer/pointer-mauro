# -*- coding: UTF-8 -*-
#
#    Copyright 2013, Mauro Lacy, mauro@lacy.com.ar
#
#    This file is part of Pointer.
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


import getopt
#import glob
#import gzip
#import hashlib
#import itertools
#import os
#import random
import sys
#import time

#import config

import camera

import camera_client
import camera_server

import util_27 as util

class CameraRuntimeError(RuntimeError):
    pass

class Camera_CLI(object):

    def __init__(self):
        self.verbose = True

    def tell(self, text, sep=' ', end='\n', stream=sys.stdout, flush=False):
        if self.verbose or stream != sys.stdout:
            stream.write(text)
            if end is not None:
                stream.write(end)
            else:
                if sep is not None:
                    stream.write(sep)
            if flush or end is None:
                stream.flush()

    def initFromArgv(self):
        options = {}
        args, commands = getopt.getopt(sys.argv[1:], \
                                       's:h', \
                                       ['help'])
        args = dict(args)
        if len(commands) == 1 and commands[0] in self.commands:
            command = commands[0]
        else:
            command = 'help'
            args = {}
        if '-h' in args or '--help' in args:
            func = Camera_CLI.print_command_help
            args = {'-c': command}
        else:
            func = self.commands[command]

        req_params, opt_params = func.cli_options
        for param in req_params:
            if param not in ('-s',) and param not in args:
                raise CameraRuntimeError("The command '%s' requires the " \
                                        "option '%s'. See 'help'." % \
                                        (command, param))
        for arg, value in args.items():
            if arg in req_params or arg in opt_params:
                if arg == '-c':
                    options['command'] = value
            else:
                raise CameraRuntimeError("The command '%s' ignores the " \
                                        "option '%s'." % (command, arg))

        self.tell("Camera %s (C) 2015 Mauro Lacy " \
                  "http://maurol.com.ar/dav/git/pointer\n" \
                  "This code is distributed under the GNU General Public " \
                  "License v3+\n" % util.VERSION, stream=sys.stdout)
        if command == 'help':
            pass
        elif '-s' in args:
            server_host = args['-s']
            options['camera'] = self._getCamera(server_host)
        else: # local camera
            options['camera'] = camera.Camera()
        func(self, **options)

    def print_help(self):
        """Print general help

           You should have figured this one out by now.
        """
        self.tell('Usage: camera [options] command'
            '\n'
            '\nRecognized options:'
            '\n  -h|--help        : Print help for a certain command'
            '\n  -s               : IP/hostname of the server to use'
            '\n'
            '\nRecognized commands:')
        m = max([len(command) for command in self.commands])
        for command, func in sorted(self.commands.items()):
            self.tell('  %s%s : %s' % (command, \
                                        ' ' * (m - len(command)), \
                                        func.__doc__.split('\n')[0]))
    print_help.cli_options = ((), ())

    def print_command_help(self, command, camera=None):
        """Print help about a certain command"""
        doc = self.commands[command].__doc__
        self.tell('\n'.join(l.strip() for l in doc.split('\n')))
    print_command_help.cli_options = (('-c',), ())

    def _getCamera(self, host):
        url = 'http://' + host + ':17937' 
        self.tell("Connecting to xmlrpc-server camera '%s'... " % (url,), end=None)
        camera = camera_client.getCameraClient(url)
        self.tell("connected.")
        return camera

    def serve(self, camera):
        """Serve local camera to a Camera client or GUI

           Start a server that provides access to the local (pi)camera
           to a Camera client.
           TCP-port 5000 for the video stream must be accessible.
           TCP-port 17937 must be accessible for xmlrpc commands 

           For example, on the server (where the Camera is):
           ./camera serve

          ... and the client:
          camera -s 192.168.0.100 take
          pointer_gui.py -c 192.168.0.100
        """
        with camera_server.CameraServer(camera) as server:
            self.tell("Camera server started...")
            try:
                server.serve_forever()
            except (KeyboardInterrupt, SystemExit):
                pass
        self.tell("Camera server closed")
    serve.cli_options = ((), ())
    
    def take(self, camera):
        """Take a picture
            For example: camera -s raspberrypi take"""
        picture = camera.take()
        with open("picture.jpg", "wb") as pic:
            pic.write(picture)
    take.cli_options = (('-s',), ())
        
    commands = {'help': print_help,
                'serve': serve,
                'take': take
                }
