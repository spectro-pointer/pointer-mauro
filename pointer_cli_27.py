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

import pointer_client_27 as client
#import pointer_server as server

import util_27 as util

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
                                       'a:e:r:d:s:h', \
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
        for arg, value in args.items():
            if arg in req_params or arg in opt_params:
                if arg == '-a':
                    options['v1'] = value
                    try:
                        if options['v2']:
                            options['coords'] = 'AzEl'
                    except KeyError:
                        options['coords'] = 'Az'
                elif arg == '-e':
                    options['v2'] = value
                    try:
                        if options['v1']:
                            options['coords'] = 'AzEl'
                    except KeyError: 
                        options['coords'] = 'El'
                elif arg == '-r':
                    options['v1'] = value
                    options['coords'] = 'RAdec'
                elif arg == '-d':
                    options['v2'] = value
                    options['coords'] = 'RAdec'
                elif arg == '--lat':
                    options['lat'] = value
                elif arg == '--lon':
                    options['lon'] = value
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
        else: # local pointer not supported in 2.7
            options['pointer'] = None
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
            "\n  -r               : Right Ascension in HHMMSS.sss format"
            "\n  -d               : Declination in degrees"
            "\n  --lat            : Latitude in degrees (negative is South latitude)"
            "\n  --lon            : Longitude in degrees (positive is East longitude)"
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
        """Serve local hardware to a Pointer client

           Start a server that provides access to the local pointing hardware
           to a Pointer client. TCP-port 17936 must be accessible.

           For example, on the server (where the Pointer is):
           pointer serve

          ... and the client:
          pointer -s 192.168.0.100 get
        """
        self.tell("Not supported in 2.7 version")
    serve.cli_options = ((), ())

    def telescope(self, pointer):
        """Serve local telescope hardware to a telescope client (i.e. stellarium)

           Start a server that provides access to the local telescope
           to a Slellarium client. The TCP-port 10001 must be accessible.

           For example, on the server (where the telescope is):
           pyrit telescope

           ... and in Stellarium, configure the server's IP in an 'External software
           or remote computer' telescope control
        """
        self.tell("Telescope server nos supported in 2.7 version.")
    telescope.cli_options = ((), ())

    def move(self, pointer, coords=None, v1=0., v2=0.):
        """Relative move the given Coords (Azimuth and Elevation [degrees], or Right Ascension [HHMMSS.sss] and Declination [degrees])
            For example:
            pointer -a 10 -e 5 move
            pointer -a 45 move
            pointer -e 15 move
            pointer -r 123456.789 -d 1.23 move
        """
        if coords in (None, 'Az', 'El'):
            coords = 'AzEl'
        pointer.move(coords, v1, v2)
    move.cli_options = (('-s'), ('-e', '-a', '-r', '-d'))
    
    def home(self, pointer, coords=None, v1=0., v2=0.):
        """Homes-in in Azimuth and Elevation, using the given step angles [degrees],
            For example:
            pointer -a 1 -e 1 home
            pointer -a 1 home
            pointer -a home (uses default homing step (1°) for azimuth, no homing for elevation)
        """
        if coords in (None, 'Az', 'El'):
            coords = 'AzEl'
        pointer.home(coords, v1, v2)
    home.cli_options = (('-s'), ('-e', '-a'))   

    def point(self, pointer, coords=None, v1=None, v2=None):
        """Absolute move to the given Coords (Azimuth and Elevation [degrees],
            or Right Ascension [HHMMSS.sss] and Declination [degrees])
            Defaults: Azimuth: 0°, Elevation: 0°
            For example:
            pointer -e 15 point
            pointer -r 120000.01 -d 45 point
        """
#        print('coords:', coords)
        if coords is not None:
            pointer.point(coords, v1, v2)
        else:
            pointer.point('AzEl', v1, v2)
#        if v1 is None and v2 is not None:
#            pointer.pointEl(v2)
#        elif v1 is not None and v2 is None:
#            pointer.pointAz(v1)
#        elif v1 is not  None and v2 is not None:
#            pointer.point(v1, v2)
#        else:
#            pointer.point(0., 0.)
    point.cli_options = (('-s'), ('-e', '-a', '-r', '-d'))

    def get(self, pointer):
        """Get actual pointer Azimuth and Elevation angles [degrees]
            and Right Ascension and Declination angles [degrees] 
            For example:
            pointer get
        """
        v1, v2 = pointer.get('AzEl')
        self.tell("\nAzimuth: %.2f°, " \
                  "Elevation: %.2f°" \
                  % (v1, v2))
        v1, v2 = pointer.get('RAdec')
        h = int(v1)
        m = int((v1 - h)*60.)
        s = (v1 - h - m / 60.)*3600.
        self.tell("RA: %02d:%02d:%05.2f, " \
                  "Dec: %.2f°" \
                  % (h, m, s, v2))
    get.cli_options = ((), ('-s'))
            
    def set(self, pointer, coords=None, v1=None, v2=None):
        """Set pointer position to the given Coords (Azimuth and Elevation [degrees],
            or Right Ascension [HHMMSS.sss] and Declination [degrees])
            Defaults: Azimuth 0., Elevation 0.
            For example:
            pointer -e 10 set
            pointer -r 120000 -d 90 set
        """
#        print('coords:', coords)
        if coords is not None:
            pointer.set(coords, v1, v2)
        else:
            pointer.set('AzEl', 0., 0.)
    set.cli_options = (('-s'), ('-e', '-a', '-r', '-d'))
    
    def getSpeed(self, pointer):
        """Get actual pointer Azimuth and Elevation axes speed [degrees/s]
            For example:
            pointer getSpeed
        """
        azimuth, elevation = pointer.getSpeed()
        self.tell("\nAzimuth Speed: %.2f°/s, " \
                  "Elevation Speed: %.2f°/s" \
                  % (azimuth, elevation))
    getSpeed.cli_options = (('-s'), ())

    def setSpeed(self, pointer, azimuth=1., elevation=1.):
        """Set pointer speed to the given Azimuth and Elevation speeds [degrees/s]
            Defaults: Azimuth: 1°/s, Elevation: 1°/s
            For example:
            pointer -e 2 setSpeed
        """
        pointer.setSpeed(azimuth, elevation)
    setSpeed.cli_options = (('-s'), ('-e', '-a'))

    def getLatLon(self, pointer):
        """Get actual pointer Latitude and Longitude settings [degrees]
            For example:
            pointer getLatLon
        """
        azimuth, elevation = pointer.getLatLon()
        self.tell("\nLatitude: %.4f°, " \
                  "Longitude: %.4f°" \
                  % (azimuth, elevation))
    getLatLon.cli_options = (('-s'), ())

    def setLatLon(self, pointer, lat=0., lon=0.):
        """Set pointer to the given Latitude and Longitude degrees]
            For example:
            pointer --lat -41 --lon -72 setLatLon
        """
        pointer.setLatLon(lat, lon)
    setLatLon.cli_options = (('-s', '--lat', '--lon'), ())

    def ledOn(self, pointer):
        """Turns the "live zero" led on
            For example:
            pointer -s pi ledOn
        """
        pointer.ledOn()
    ledOn.cli_options = (('-s'), ())

    def ledOff(self, pointer):
        """Turns the "live zero" led off
            For example:
            pointer -s pi ledOff
        """
        pointer.ledOff()
    ledOff.cli_options = (('-s'), ())

    def abort(self, pointer):
        """Abort currently executing command
            For example:
            pointer -s raspberrypi abort
        """
        pointer.abort()
    abort.cli_options = (('-s'), ())
        
    commands = {'home': home,
                'move': move,
                'point': point,
                'get' : get,
                'getSpeed' : getSpeed,
                'setSpeed' : setSpeed,
                'getLatLon' : getLatLon,
                'setLatLon' : setLatLon,
                'set' : set,
                'ledOn': ledOn,
                'ledOff': ledOff,
                'abort': abort,
                'help': print_help,
                'serve': serve,
                'telescope': telescope
                }
