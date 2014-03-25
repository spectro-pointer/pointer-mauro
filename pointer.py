#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Parallel Port/GPIO Generic Pointer Driver
#
#(C) 2013 Mauro Lacy <mauro@lacy.com.ar>
# this is distributed under a free software license, see license.txt

import sys, time
from util import Thread
from threading import Condition

from collections import defaultdict
from functools import reduce

STEP_ONE	= 0x01
DIR_CW		= 0x00
DIR_CCW		= 0x01
AXIS_X	= 0
AXIS_Y	= 1
AXIS_Z	= 2
AXIS_A	= 3

class EightBitIO(object):
    def __init__(self):
        
        self.data = 0
        
        self.setRS(0)
        self.setRW(0)
        self.out(0)                 #reset pins
        time.sleep(0.050)           #wait more than 30ms

    def setRW(self, state):
        self.p.setAutoFeed(state)
    
    def setRS(self, state):
        self.p.setInitOut(state)
        
    def out(self, data):
        """set data to the Port"""
        self.data = data
        self.p.setData(self.data)

class ParallelPointer(EightBitIO):
    """ Parallel Port Pointer Driver"""
    
    def __init__(self):
        import parallel
        self.p = parallel.Parallel()
        
        self.PINS = ((17, 16), (14, 1), (2, 3), (4, 5)) # (STEP, DIR) pins for each axis      
        
        self.PORT_DATA=0
        self.PORT_CTRL=1
        self.PORT_STAT=2 # Not used
        
        # Port(DATA/CTRL) for each axis
        self.PORT     = lambda axis: int(not(axis/2))
        
        # Data bit for each Data pin
        self.DATA_BIT = lambda pin: pin-2
        
        # Control function for each Control pin
        self.CTRL_FUN = {1: self.p.setDataStrobe, 14: self.p.setAutoFeed, 16: self.p.setInitOut, 17: self.p.setSelect}
        
        super(ParallelPointer, self).__init__()
        
    def move2(self, axes):
        """Low-level Simultaneous Axis Move Function
           Simultaneously move each axis from 'axes', their given number of steps
           A negative step is CCW
        """
        steps = [0., 0., 0., 0.]
        datas = [0, 0, 0, 0]
        functions = {}
        dir = defaultdict(int)
        changeDir = [False, False, False, False]
        for axis, step in list(axes.items()):
            if (AXIS_X <= axis <= AXIS_A):
                dir[axis] = DIR_CW
                if step < 0: 
                    dir[axis] = DIR_CCW
                    step = -step
                
                steps[axis] = step

                if self.lastDir[axis] != dir[axis]: # change dir offsets
                    steps[axis] += self.dirChangeSteps[axis][dir[axis]]
                    changeDir[axis] = True
                    self.lastDir[axis] = dir[axis]                
                pins=self.PINS[axis]
                port=self.PORT(axis)
                if port == self.PORT_DATA:
                    bits=(self.DATA_BIT(pins[0]), self.DATA_BIT(pins[1]))
                    datas[axis] = (1<<bits[0]) | (dir[axis]<<(bits[1]))
                elif port == self.PORT_CTRL:
                    # Set dir just once
                    dirFunction = self.CTRL_FUN[pins[1]]
                    dirFunction(dir[axis])
                    # Save step function
                    functions[axis] = self.CTRL_FUN[pins[0]]
            else:
                print("ERROR: axis %d steps %d dir %d" %(axis, steps, dir[axis]))
        
        # Now process
        changeDirSteps = [0, 0, 0, 0]
        for i in range(int(round(max(steps)))):
#            print "step", i+1
            # Process each axis
            data = 0 # FIXME: Consider multiple independent requests
            # Data port axes
            sleep_ON = 0
            sleep_OFF= 0
            # Data port axis
            for axis in AXIS_Z, AXIS_A:
                if steps[axis] >0.:
                    data |= datas[axis]
                    sleep_ON  = max(sleep_ON, self.sleep_ON[axis])
                    sleep_OFF = max(sleep_OFF, self.sleep_OFF[axis])
            # Control port axes
            for axis in AXIS_X, AXIS_Y:
                if steps[axis] >0.:
                    # set dir
                    stepFunction = functions[axis]
                    stepFunction(1)
                    sleep_ON  = max(sleep_ON, self.sleep_ON[axis])
                    sleep_OFF = max(sleep_OFF, self.sleep_OFF[axis])
            self.out(data) 
            time.sleep(sleep_ON) # wait (max) on
            # Turn off Data axis (Z and A)
            self.out(0)
            # Turn off Control axis (X and Y)
            for stepFunction in list(functions.values()):
                stepFunction(0)
            # Absolute steps tracking
            print('pos/steps:', end=' ')
            for axis in AXIS_X, AXIS_Y, AXIS_Z, AXIS_A:
                print(dir[axis], self.pos[axis], '/', end=' ')
                if steps[axis] > 0.:
                    steps[axis] -= 1
                    if changeDir[axis]:
                        if changeDirSteps[axis] < self.dirChangeSteps[axis][dir[axis]]:
                            print('changeDir:', changeDirSteps[axis], end=' ')
                            changeDirSteps[axis] += 1
                        else:
                            self.pos[axis] -= (dir[axis] - 1 * (dir[axis] == 0))
                    else:
                        self.pos[axis] -= (dir[axis] - 1 * (dir[axis] == 0))
                print(steps[axis], ',', end=' ')
            print()
            time.sleep(sleep_OFF) # wait (max) off

class Axis(Thread):
    """ A threaded axis processor
    
        Independent processing for each axis
    """
    def __init__(self, step_dir, end):
        (step, dir) = step_dir

        Thread.__init__(self)
        
        self.PORTS = (step, dir)
        self.END   = end
        
        
        self.lastDir = DIR_CW # default
        self.dirChangeSteps = [0, 0]
        self.pos = 0.
        self.sleep = [0.050, 0.050] # default

        self.moving = False
        self.abortMove = False
        
        self.cv = Condition()

        # request queue        
        self.requests = []
        
        # Update initial state
#        print('Axis %s: limit switch port %d' % (self.name, self.END))
        self.get_state()
        
        self.setDaemon(True)
        self.start()
        
    def run(self):
        while self.shallStop is False:
            # read request from requests list and process
            with self.cv:
                while len(self.requests) == 0 and self.shallStop is False:
                        self.cv.wait(1)
                if self.shallStop:
                        break
            # sequential processing
            while self.moving: # not aborted
                time.sleep(.1)
            self.moving = True
            if len(self.requests):
                request = self.requests.pop(0)
                print("Request received in thread %s: req:" % (self.name), request)
                req = request[0]
                if req == 'move':
                    self.move(request[1])
                elif req == 'home':
                    self.home(request[1])
            self.moving = False

    def put_request(self, request):
        # write request to mqueue
        print('Request to thread %s:' % (self.name), request)
        with self.cv:
            self.requests.append(request)
            self.cv.notifyAll()

#    def serve_forever(self):
#        while not self.shallStop:
#            time.sleep(1)

    def shutdown(self):
        Thread.shutdown(self)
        
    def get_sleep(self):
        """ Get step delay
            Format is (ON, OFF)
            In seconds
        """
        return self.sleep
    
    def get_dirChangeSteps(self):
        return self.dirChangeSteps

    def get_pos(self):
        return self.pos
        
    def set_sleep(self, delay):
        """ Set step delay
            Format is (ON, OFF)
            In seconds
        """
        self.sleep = delay
       
    def set_dirChangeSteps(self, dirChangeSteps):
        """ Set step delay
            In seconds
        """
        self.dirChangeSteps = dirChangeSteps

    def set_pos(self, pos):
        self.pos = pos
        
    def abort(self):
        # abort all pending requests
        with self.cv:
            self.requests = []
        # abort current move
        self.abortMove = True
    
    def is_moving(self):
        return self.moving
    
    def move(self, steps):
        """Low-level Axis Move Function
           Move a given number of steps
           A negative step is CCW
        """
        self.moving = True
        dir = DIR_CW
        changeDir = False
        if steps < 0: 
            dir = DIR_CCW
            steps = -steps
        
        steps = float(steps)

        if self.lastDir != dir: # change dir offsets
            steps += self.dirChangeSteps[dir]
            changeDir = True
            self.lastDir = dir                
        port=self.PORTS
        # Set dir just once
        if gpioFound:
            GPIO.output(port[1], dir)
            self.get_state()
        
        sleepOn = self.sleep[0]
        sleepOff= self.sleep[1]
        # Now process
        changeDirSteps = 0
        step = 0
        self.abortMove = False
        while step < round(steps) and self.abortMove is not True:
            if gpioFound:      
                GPIO.output(port[0], True)
            time.sleep(sleepOn)
           
            if gpioFound:
                GPIO.output(port[0], False)
                self.get_state() # Update limit switches
            
            # Absolute steps tracking
#            print('pos/steps:', end=' ')
#            print(dir, self.pos, '/', end=' ')
            if changeDir:
                if changeDirSteps < self.dirChangeSteps[dir]:
#                    print('changeDir:', changeDirSteps, end=' ')
                    changeDirSteps += 1
                else:
                    self.pos -= (dir - 1 * (dir == 0))
            else:
                self.pos -= (dir - 1 * (dir == 0))
#            print(steps, ',', end=' ')
#            print()
            time.sleep(sleepOff) # wait off
            step += 1
        self.moving = False
            
    def home(self, steps):
        """
            Low-level Axis Homing Method
        """
        self.abortMove = False
        while steps and self.get_state() and not self.abortMove:
            self.move(steps)

    def get_state(self):
        """
            Returns limit switch state
            True  means open
            False means closed
        """
        if self.END > 0:
            self.state = GPIO.input(self.END)
        else:
            self.state = 0 # Always closed
        return self.state
              
try:
    import RPi.GPIO as GPIO
    gpioFound = True
except ImportError:
    gpioFound = False
    print("Warning: Raspberry Pi GPIO module not found.")
    pass
    
class GpioPointer(object):
    """ GPIO-Based (Raspberry Pi) Pointer Driver"""
    def __init__(self):
        # 1. First set up RPi.GPIO
        if gpioFound:
            GPIO.setmode(GPIO.BOARD)
        #             X(El)   Y(free)   Z(Az)     A(free)
        self.PORTS= ((18, 7), (11, 16), (22, 24), (13, 12)) # (STEP, DIR) GPIO ports for each axis      
        self.ENDS =  (23    , -1      , 21      , -1) # Limit switches GPIO ports
        
        for p in reduce(tuple.__add__, self.PORTS, ()):
            if p > 0:
                try:
                    if gpioFound:
                        print('port:', p)
                        GPIO.setup(p, GPIO.OUT)
                except ValueError:
                    print("Invalid port:", p)
                    sys.exit(1)
                
        for p in self.ENDS:
            if p > 0:
                try:
                    if gpioFound:
                        print('input port:', p)
                        GPIO.setup(p, GPIO.IN)
                except ValueError:
                    print("Invalid port:", p)
                    sys.exit(1)
                
#class Pointer(ParallelPointer):
class Pointer(GpioPointer):
    """Hardware Independent Pointer class"""
    def __init__(self):
        self.axes = {'X': AXIS_X, 'Y': AXIS_Y, 'Z': AXIS_Z, 'A': AXIS_A}

        # Faster means less torque for X(El), Y, Z(Az), A
        # FIXME: read all from config
        self.sleep_ON  = (.005, .0075, .020, .0025)
        self.sleep_OFF = (.005, .0075, .020, .0025)
        
        # Dir change adjustment (CW, CCW) for X(El), Y , Z(Az), A
        self.dirChangeSteps = [(20, 20), (0, 0), (5, 5), (0, 0)]
        self.lastDir = [DIR_CW, DIR_CW, DIR_CW, DIR_CW]
        
        super(Pointer, self).__init__()
        
        # Create and Initialize Threads for each axis
        self.Axes = []
        for i, name in enumerate(['X', 'Y', 'Z', 'A']): 
            self.Axes.append(Axis(self.PORTS[i], self.ENDS[i]))
            self.Axes[i].name=name
            self.Axes[i].set_sleep((self.sleep_ON[i], self.sleep_OFF[i]))
            self.Axes[i].set_dirChangeSteps(self.dirChangeSteps[i])

    def is_moving(self):
        moving = False
        for axis in self.Axes:
            moving |= axis.is_moving()
        return moving
    
    def abort(self):
        for axis in self.Axes:
            axis.abort()
     
    def setDirChangeSteps(self, axesNames):
        """ High level direction change extra steps for each axis
            Format is (CW, CCW)
            Units are steps
        """
        for axis, steps in list(axesNames.items()):
            ax = self.axes[axis]
            self.Axes[ax].set_dirChangeSteps(steps)
        
    def move(self, axes):
        """
            High-level Simultaneous Axis Move Function
            Simultaneously move each axis from 'axes', their given number of steps
            A negative step means CCW
        """
        for axis, step in list(axes.items()):
            self.Axes[axis].put_request(['move', step])

    def home(self, axes):
        """
            High-level Axis Homing Function
        """
        for axis, step in list(axes.items()):
            self.Axes[axis].put_request(['home', step])

#from accelerometer import AnglesSensor
class AnglesPointer(Pointer):
    """Angles Pointer class"""
    def __init__(self):
        # Angles to Steps conversions
        self.steps = [2980, 0, 1360, 0]
        self.stepAngle = [360./self.steps[0], 0., 360./self.steps[2], 0.]
        
#        self.angles = AnglesSensor()
        super(AnglesPointer, self).__init__()
        
    def get(self, axesNames):
        """Get the angles from each axis from 'axesNames'
           Angles are in degrees
           A negative angle means CCW
        """
        for axis in list(axesNames.keys()):
            ax = self.axes[axis]
            pos = self.Axes[ax].get_pos()
            angles = pos * self.stepAngle[ax]
            axesNames[axis] = angles
        return axesNames

    def set(self, axesNames):
        """Set each axis from 'axesNames' to the given angle
           Angles are in degrees
           A negative angle means CCW
        """
        for axis, angle in list(axesNames.items()):
            axis = self.axes[axis]
            steps = float(angle) / self.stepAngle[axis]
            self.Axes[axis].set_pos(steps)

    def move(self, axesNames):
        """
            Simultaneously move each axis from 'axesNames' the given angle
            Angles are in degrees
            A negative angle means CCW
        """
        ax = dict()
        for axis, angle in list(axesNames.items()):
            print(axis, angle)
            steps = angle / self.stepAngle[self.axes[axis]]
            ax[self.axes[axis]] = int(round(steps))
        Pointer.move(self, ax)

    def home(self, axesNames):
        """
            Home-in each axis from 'axesNames', with a given angle step
            Angles are in degrees
            A negative angle means CCW
        """
        ax = dict()
        for axis, angle in list(axesNames.items()):
            print(axis, angle)
            steps = angle / self.stepAngle[self.axes[axis]]
            ax[self.axes[axis]] = int(round(steps))
        Pointer.home(self, ax)
    
    def point(self, axesNames):
        """
            Simultaneously point each axis from 'axesNames' to the given angle
            Angles are in degrees
            A negative angle means CCW
        """
        ax = dict()
        for axis, angle in list(axesNames.items()):
            axis = self.axes[axis]
            steps = angle / self.stepAngle[axis]
            pos = self.Axes[axis].get_pos()
            print(axis, angle, pos, steps, end=' ')  
            ax[axis] = round(steps-pos)
            if ax[axis] > self.steps[axis]/2:
                ax[axis] -= self.steps[axis]
            if ax[axis] < -self.steps[axis]/2:
                ax[axis] += self.steps[axis]
            print('delta:', ax[axis])
        Pointer.move(self, ax)

    def getSpeed(self, axesNames):
        """
            Get the speed for each axis from 'axesNames'
            Speeds are in degrees/s
        """
        for axis in list(axesNames.keys()):
            ax = self.axes[axis]
            delay = self.Axes[ax].get_sleep()
            speed = 1./(delay[0]+delay[1]) * self.stepAngle[ax]
            axesNames[axis] = speed
        return axesNames

    def setSpeed(self, axesNames):
        """ 
            High level speed setting for each axis
            Speed Units are degrees/second
        """
        for axis, speed in list(axesNames.items()):
            ax = self.axes[axis]
            # convert to steps/s
            steps = float(speed) / self.stepAngle[ax]
            delay = 1./steps
            self.Axes[ax].set_sleep((delay/2., delay/2.))

class AzElPointer(AnglesPointer):
    """Azimuth/Elevation Pointer class
       0° Azimuth is North. Azimuth is positive eastward
       Angles are in degrees
    """
    def __init__(self):
        super(AzElPointer, self).__init__()

        self.axes['Az'] = AXIS_Z
        self.axes['El'] = AXIS_X

    def move(self, azimuth, elevation):
        """Simultaneously move in azimuth and elevation
           Angles are in degrees
           A negative angle means CCW
        """
        # Concurrent movements
        ax=dict()
        for axis, angles in zip(('Az', 'El'), (azimuth, elevation)): 
            ax[axis] = float(angles)
        AnglesPointer.move(self, ax)

    def home(self, azimuth, elevation):
        """
            Homes-in in azimuth and elevation
            Step angles are in degrees
            A negative angle means CCW
            Zero means no home-in for that axis
        """
        # Concurrent movements
        ax=dict()
        for axis, angles in zip(('Az', 'El'), (azimuth, elevation)): 
            ax[axis] = float(angles)
        AnglesPointer.home(self, ax)
        
    def point(self, azimuth, elevation):
        """Simultaneously point in azimuth and elevation
           Angles are in degrees
           A negative angle means CCW
        """
        # Concurrent movements
        ax=dict()
        for axis, angles in zip(('Az', 'El'), (azimuth, elevation)): 
            ax[axis] = float(angles)
        AnglesPointer.point(self, ax)
        
    def pointAz(self, azimuth):
        """Only point in Azimuth, leaving Elevation unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['Az'] = float(azimuth)
        AnglesPointer.point(self, ax)
        
    def pointEl(self, elevation):
        """Only point in Elevation, leaving Azimuth unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['El'] = float(elevation)
        AnglesPointer.point(self, ax)

    def get(self):
        """Get actual absolute Azimuth and Elevation angles
           Returned angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['Az'] = 0
        ax['El'] = 0
        ax = AnglesPointer.get(self, ax)
        return ax['Az'], ax['El']
    
    def getSpeed(self):
        """Get actual speed for Azimuth and Elevation axes
           Returned speeds are in degrees/s
        """
        ax=dict()
        ax['Az'] = 0
        ax['El'] = 0
        ax = AnglesPointer.getSpeed(self, ax)
        return ax['Az'], ax['El']
    
    def set(self, azimuth=0., elevation=0.):
        """Set absolute Azimuth and Elevation to actual azimuth/elevation angles
           Used for pointer reset
           Angles are in degrees
           A negative angle means CCW
        """
        self.setAz(azimuth)
        self.setEl(elevation)
        
    def setAz(self, azimuth=0.):
        """Self absolute Azimuth to actual azimuth axis position, leaving elevation axis unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['Az'] = azimuth
        AnglesPointer.set(self, ax)
        
    def setEl(self, elevation=0.):
        """Set absolute Elevation to actual elevation axis position, leaving azimuth axis unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['El'] = elevation
        AnglesPointer.set(self, ax)
        
    def setSpeed(self, azimuth=0., elevation=0.):
        """Set Azimuth and Elevation axes speed
           Speeds are in degrees/s
        """
        ax=dict()
        if azimuth != 0.:
            ax['Az'] = azimuth
        if elevation != 0.:
            ax['El'] = elevation
        AnglesPointer.setSpeed(self, ax)

import sidereal
import time
import datetime
from math import radians, degrees
from gps_cli import GpsPoller
 
class RAdecPointer(AzElPointer):
    """Right Ascension/Declination Pointer class"""
    def __init__(self):
        super(RAdecPointer, self).__init__()
        
        """ Observer's latitude and longitude, in degrees
            Longitude is positive eastward
        """
        # Default values
        self.lat = -41.14
        self.lon = -71.32
        self.height = 825.
        self.heading = 0.
        self.speed = 0.
        self.climb = 0.
        self.magneticDeclination = +7.0 # [degrees]
        self.time = time.time()
        self.gpsData = {}
#        self.gps = None # no gps
        self.gps = GpsPoller(server='pi') # FIXME: config parameter for server
        if (self.gps):
            self.gps.start()
            self._gpsUpdate() 

    def _gpsUpdate(self):
        """ Tries to update our latitude and longitude information from gps
        """
        # Update height, heading, speed, climb and time too 
        # FIXME: Implement proper GpsData class 
        try:
            if self.gps:
                self.gpsData = self.gps.get()
                self.lat = self.gpsData['lat']
                self.lon = self.gpsData['lon']
                self.height = self.gpsData['alt']
                self.heading = self.gpsData['heading']
                self.speed = self.gpsData['speed']
                self.climb = self.gpsData['climb']
                self.time = self.gpsData['time']
        except (TypeError, KeyError, AttributeError):
            pass

    def _parseRA(self, ra):
        """Parse a Right Ascension and return the equivalent hours
           Right Ascension format is "HHMMSS.sss"
        """
        hour   = float(ra[0:2])
        minute = float(ra[2:4])
        second = float(ra[4:])
        print('hour:', hour)
        print('minute:', minute)
        print('second:', second)
        return hour+minute/60.+second/3600.
    
    def _RAdec2AzEl(self, raHours, dec):
        # Convert hours to radians
        ra = sidereal.hoursToRadians(raHours)
        print('RA(radians):', ra)
        # Convert to azimuth and elevation
        RADec = sidereal.RADec(ra, radians(float(dec)))
        ut = datetime.datetime.utcnow()
        h = sidereal.raToHourAngle(ra, ut, radians(self.lon))
        self._gpsUpdate()
        AltAz = RADec.altAz(h, radians(self.lat))
        az = degrees(AltAz.az);
        el = degrees(AltAz.alt)
        print('Azimuth:', az, 'Elevation:', el)
        return az, el

    def getLatLon(self):
        self._gpsUpdate()
        return self.lat, self.lon

    def setLatLon(self, lat, lon):
        self.gps = None # Disable gps updating
        self.lat = lat
        self.lon = lon

    def get(self):
        """ Get actual RA and Dec values
            RA format is 'HHMMSS.sss'
            Dec in degrees
        """ 
        ra, dec = self.get2()
        # FIXME: implement RA conversion
        return ra, dec
        
    def get2(self):
        """ Get actual RA and Dec values, in degrees
        """
        Az, Alt = AzElPointer.get(self)
        
        # convert to RA/dec
        AltAz = sidereal.AltAz(radians(Alt), radians(Az))
        
        dt = datetime.datetime.utcnow()
        lst = sidereal.SiderealTime.fromDatetime(dt).lst(radians(self.lon))
        self._gpsUpdate()
        latLon = sidereal.LatLon(radians(self.lat), radians(self.lon))
        RAdec = AltAz.raDec(lst, latLon)
        return degrees(RAdec.ra), degrees(RAdec.dec)

    def set(self, ra, dec):
        """Set Right Ascension and declination
           Right Ascension format is "HHMMSS.sss"
           Declination Angle is in degrees
        """
        # Convert RA string to hours
        hours = self._parseRA(str(ra))
        self.set2(hours, dec)
    
    def set2(self, raHours, dec):
        """Set Right Ascension and declination
           Right Ascension in hours and fraction 
           Declination Angle in degrees
        """
        az, el = self._RAdec2AzEl(raHours, dec)
        AzElPointer.set(self, az, el)

    def point(self, ra, dec):
        """Simultaneously point in Right Ascension and declination
           Right Ascension format is "HHMMSS.sss"
           Declination Angle is in degrees
        """
        hours = self._parseRA(str(ra))
        self.point2(hours, dec)
        
    def point2(self, ra, dec):
        """Simultaneously point in Right Ascension and declination
           Right Ascension in degrees
           Declination Angle in degrees
        """
        az, el = self._RAdec2AzEl(ra, dec)
        AzElPointer.point(self, az, el)

class GenericPointer(RAdecPointer):
    """Generic/Wrapper Pointer class"""
    def __init__(self):
        super(GenericPointer, self).__init__()

    def get(self, coords):
        if coords == 'AzEl':
            return AzElPointer.get(self)
        elif coords == 'RAdec':
            return RAdecPointer.get(self)

    def set(self, coords, v1, v2):
        print('coords:', coords)
        if coords == 'AzEl':
            AzElPointer.set(self, v1, v2)
        elif coords == 'Az':
            AzElPointer.setAz(self, v1)
        elif coords == 'El':
            AzElPointer.setEl(self, v2)
        elif coords == 'RAdec':
            RAdecPointer.set(self, v1, v2)

    def move(self, coords, v1, v2):
        print('coords:', coords)
        if coords == 'AzEl':
            AzElPointer.move(self, v1, v2)
        elif coords == 'RAdec':
            RAdecPointer.move(self, v1, v2)
            
    def home(self, coords, v1, v2):
        print('coords:', coords)
        if coords == 'AzEl':
            AzElPointer.home(self, v1, v2)

    def point(self, coords, v1, v2):
        print('coords:', coords)
        if v1 is None:
            v1 = 0.
        if v2 is None:
            v2 = 0.
        if coords == 'AzEl':
            AzElPointer.point(self, v1, v2)
        elif coords == 'Az':
            AzElPointer.pointAz(self, v1)
        elif coords == 'El':
            AzElPointer.pointEl(self, v2)
        elif coords == 'RAdec':
            RAdecPointer.point(self, v1, v2)

#if __name__ == '__main__':
#    if len(sys.argv) < 3 or not len(sys.argv) & 1:
#        print >>sys.stderr, "Usage: %s <axis> <angle> ...\naxis : {X|Y|Z|A}\nangle: Angle in degrees(- = CCW)" % sys.argv[0]
#        sys.exit(1)
#    
#    pointer = AnglesPointer()
#
#    # Concurrent movements
#    ax=dict()
#    for axis, angles in zip(sys.argv[1::2], sys.argv[2::2]): 
#        ax[axis] = float(angles)
#    pointer.move(ax)
#    # FIXME: Wait for threads to finish/Ordered threads shutdown
#    time.sleep(3) # give time to the threads to process the requests
