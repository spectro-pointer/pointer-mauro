# -*- coding: UTF-8 -*-
#
#    Copyright 2013, Mauro Lacy, mauro@lacy.com.ar
#
#    This file is part of CNC/Pointer.
#
#    CNC/Pointer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CNC/Pointer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CNC/Pointer.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement

import getopt
#import glob
#import gzip
#import hashlib
#import itertools
#import os
#import random
import sys
#import time

import pointer
#import config
import util
import client
import server

class PointerRuntimeError(RuntimeError):
    pass


class Pointer_CLI(object):

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
                                       'a:e:s:h', \
                                       ['help'])
        args = dict(args)

        if len(commands) == 1 and commands[0] in self.commands:
            command = commands[0]
        else:
            command = 'help'
            args = {}
        if '-h' in args or '--help' in args:
            func = Pointer_CLI.print_command_help
            args = {'-c': command}
        else:
            func = self.commands[command]

        req_params, opt_params = func.cli_options
        for param in req_params:
            if param not in ('-s',) and param not in args:
                raise PointerRuntimeError("The command '%s' requires the " \
                                        "option '%s'. See 'help'." % \
                                        (command, param))
        for arg, value in args.iteritems():
            if arg in req_params or arg in opt_params:
                if arg == '-a':
                    options['azimuth'] = value
                elif arg == '-e':
                    options['elevation'] = value
                elif arg == '-c':
                    options['command'] = value
            else:
                raise PointerRuntimeError("The command '%s' ignores the " \
                                        "option '%s'." % (command, arg))

        self.tell("Pointer %s (C) 2013 Mauro Lacy " \
                  "http://maurol.com.ar/dav/git/pointer\n" \
                  "This code is distributed under the GNU General Public " \
                  "License v3+\n" % util.VERSION, stream=sys.stdout)
        if command == 'help':
            pass
        elif '-s' in args:
            server_host = args['-s']
            options['pointer'] = self._getPointer(server_host)
        else: # local pointer
            options['pointer'] = pointer.RAdecPointer()
        
        func(self, **options)

    def print_help(self):
        """Print general help

           You should have figured this one out by now.
        """
        self.tell('Usage: pointer [options] command'
            '\n'
            '\nRecognized options:'
            '\n  -h|--help        : Print help for a certain command'
            "\n  -a               : Azimuth in degrees"
            "\n  -e               : Elevation in degrees"
            '\n  -s               : IP/hostname of the server to use'
            '\n'
            '\nRecognized commands:')
        m = max([len(command) for command in self.commands])
        for command, func in sorted(self.commands.items()):
            self.tell('  %s%s : %s' % (command, \
                                        ' ' * (m - len(command)), \
                                        func.__doc__.split('\n')[0]))
    print_help.cli_options = ((), ())

    def print_command_help(self, pointer, command):
        """Print help about a certain command"""
        doc = self.commands[command].__doc__
        self.tell('\n'.join(l.strip() for l in doc.split('\n')))
    print_command_help.cli_options = (('-c',), ())

    def _getPointer(self, host):
        url = 'http://' + host + ':17936' 
        self.tell("Connecting to xmlrpc-server pointer '%s'... " % (url,), end=None)
        pointer = client.getPointerClient(url)
        self.tell("connected.")
        return pointer

    def serve(self, pointer):
        """Serve local hardware to other Pointer client

           Start a server that provides access to the local pointing hardware
           to a Pointer client. TCP-port 17936 must be accessible.

           For example, on the server (where the Pointer is):
           pointer serve

          ... and the client:
          pointer -s http://192.168.0.100:17936 -a 1 -e 2 point
        """
        with server.PointerServer(pointer) as rpcd:
            self.tell("Server started...")
            try:
                rpcd.serve_forever()
            except (KeyboardInterrupt, SystemExit):
                pass
        self.tell("Server closed")
    serve.cli_options = ((), ())

    def move(self, pointer, azimuth=0, elevation=0):
        """Relative move the given Azimuth and Elevation [degrees]
            For example:
            pointer -a 10 -e 5 move
            pointer -a 45 move
            pointer -e 15 move
        """
        pointer.move(azimuth, elevation)
    move.cli_options = ((), ('-e', '-a', '-s'))

    def point(self, pointer, azimuth=None, elevation=None):
        """Absolute move to the given Azimuth and Elevation [degrees]
            For example:
            pointer -e 15 point
        """
        if azimuth is None and elevation is not None:
            pointer.pointEl(elevation)
        elif azimuth is not None and elevation is None:
            pointer.pointAz(azimuth)
        elif azimuth is not  None and elevation is not None:
            pointer.point(azimuth, elevation)
        else:
            pointer.point(0., 0.)
    point.cli_options = ((), ('-e', '-a', '-s'))

    def get(self, pointer):
        """Get actual pointer Azimuth and Elevation angles [degrees]
            For example:
            pointer get
        """
        azimuth, elevation = pointer.get()
        self.tell("\nAzimuth: %.2f, " \
                  "Elevation: %.2f" \
                  % (azimuth, elevation))
    get.cli_options = ((), ('-s'))
            
    def set(self, pointer, azimuth=None, elevation=None):
        """Set pointer position to the given Azimuth and Elevation [degrees]
            Defaults: 0., 0.
            For example:
            pointer -e 0 set
        """
        if azimuth is None and elevation is not None:
            pointer.setEl(elevation)
        elif azimuth is not None and elevation is None:
            pointer.setAz(azimuth)
        elif azimuth is not  None and elevation is not None:
            pointer.set(azimuth, elevation)
        else:
            pointer.set(0., 0.)
    set.cli_options = ((), ('-e', '-a', '-s'))
    
    def getSpeed(self, pointer):
        """Get actual pointer Azimuth and Elevation axes speed [degrees/s]
            For example:
            pointer getSpeed
        """
        azimuth, elevation = pointer.getSpeed()
        self.tell("\nAzimuth Speed: %.2f º/s, " \
                  "Elevation Speed: %.2f º/s" \
                  % (azimuth, elevation))
    getSpeed.cli_options = ((), ('-s'))

    def setSpeed(self, pointer, azimuth=0., elevation=0.):
        """Set pointer speed to the given Azimuth and Elevation speeds [degrees/s]
            For example:
            pointer -e 1 setSpeed
        """
        pointer.setSpeed(azimuth, elevation)
    setSpeed.cli_options = ((), ('-e', '-a', '-s'))

    def abort(self, pointer):
        """Abort currently executing command
            For example:
            pointer -s raspberrypi abort
        """
        pointer.abort()
    abort.cli_options = ((), ('-s'))
        
    commands = {'move': move,
                'point': point,
                'get' : get,
                'getSpeed' : getSpeed,
                'set' : set,
                'setSpeed' : setSpeed,
#                'setChangeDirSteps:' setChangeDirSteps,
                'abort': abort,
                'help': print_help,
                'serve': serve}