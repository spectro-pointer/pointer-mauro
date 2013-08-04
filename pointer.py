#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Generic Parallel Port Pointer Driver
#
#(C) 2013 Mauro Lacy <mauro@lacy.com.ar>
# this is distributed under a free software license, see license.txt

import sys, time
from util import Thread
from threading import Condition

from collections import defaultdict

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
        for axis, step in axes.items():
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
                print "ERROR: axis %d steps %d dir %d" %(axis, steps, dir[axis])
        
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
            for stepFunction in functions.values():
                stepFunction(0)
            # Absolute steps tracking
            print 'pos/steps:',
            for axis in AXIS_X, AXIS_Y, AXIS_Z, AXIS_A:
                print dir[axis], self.pos[axis], '/',
                if steps[axis] > 0.:
                    steps[axis] -= 1
                    if changeDir[axis]:
                        if changeDirSteps[axis] < self.dirChangeSteps[axis][dir[axis]]:
                            print 'changeDir:', changeDirSteps[axis],
                            changeDirSteps[axis] += 1
                        else:
                            self.pos[axis] -= (dir[axis] - 1 * (dir[axis] == 0))
                    else:
                        self.pos[axis] -= (dir[axis] - 1 * (dir[axis] == 0))
                print steps[axis], ',',
            print
            time.sleep(sleep_OFF) # wait (max) off

class Axis(Thread):
    """ A threaded axis processor
    
        Independent processing for each axis
    """
    def __init__(self, (step, dir)):
        Thread.__init__(self)
        
        self.PORTS = (step, dir)
        
        self.lastDir = DIR_CW # default
        self.dirChangeSteps = [0, 0]
        self.pos = 0.
        self.sleep = [0.050, 0.050] # default
        
        self.cv = Condition()

        # request queue        
        self.requests = []
        
        self.setDaemon(True)
        self.start()
        
    def run(self):
        while self.shallStop is False:
            # read request from requests list and process
            with self.cv:
                while len(self.requests) == 0 and self.shallStop is False:
                        self.cv.wait(1)
                if self.shallStop is not False:
                        break
                request = self.requests.pop(0)
            # process
            print "Request received in thread %s: req: %d" % (self.name, request)
            self.move(request)      

    def put_request(self, request):
        # write request to mqueue
        print 'Request to thread %s: steps: %d' % (self.name, request)
        with self.cv:
            self.requests.append(request)
            self.cv.notifyAll()

#    def serve_forever(self):
#        while not self.shallStop:
#            time.sleep(1)

    def shutdown(self):
        Thread.shutdown(self)
        
    def get_sleep(self):
        return self.sleep
    
    def get_dirChangeSteps(self):
        return self.dirChangeSteps

    def get_pos(self):
        return self.pos
        
    def set_sleep(self, delay):
        """ Set step delay
            Format is (CW, CCW)
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

    def move(self, steps):
        """Low-level Axis Move Function
           Move a given number of steps
           A negative step is CCW
        """
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
        
        sleepOn = self.sleep[0]
        sleepOff= self.sleep[1]
        # Now process
        changeDirSteps = 0
        for _ in range(int(round(steps))):
            if gpioFound:      
                GPIO.output(port[0], True)
            time.sleep(sleepOn)
           
            if gpioFound:
                GPIO.output(port[0], False)
            
            # Absolute steps tracking
            print 'pos/steps:',
            print dir, self.pos, '/',
            if changeDir:
                if changeDirSteps < self.dirChangeSteps[dir]:
                    print 'changeDir:', changeDirSteps,
                    changeDirSteps += 1
                else:
                    self.pos -= (dir - 1 * (dir == 0))
            else:
                self.pos -= (dir - 1 * (dir == 0))
            print steps, ',',
            print
            time.sleep(sleepOff) # wait off

try:
    import RPi.GPIO as GPIO
    gpioFound = True
except ImportError:
    gpioFound = False
    print "Warning: Raspberry Pi GPIO module not found."
    pass
    
class GpioPointer(object):
    """ GPIO-Based (Raspberry Pi) Pointer Driver"""
    def __init__(self):
        # 1. First set up RPi.GPIO
        if gpioFound:
            GPIO.setmode(GPIO.BOARD)
        
        self.PORTS= ((18, 7), (11, 21), (22, 24), (13, 5)) # (STEP, DIR) GPIO ports for each axis
        
        for p in reduce(tuple.__add__, self.PORTS, ()):
            try:
                if gpioFound:
                    GPIO.setup(p, GPIO.OUT)
            except ValueError:
                print "Invalid port:", p
                sys.exit(1)
                
class Pointer(GpioPointer):
#class Pointer(ParallelPointer):
    """Hardware Independent Pointer class"""
    def __init__(self):
        self.axes = {'Az': AXIS_Z, 'El': AXIS_X, 'X': AXIS_X, 'Y': AXIS_Y, 'Z': AXIS_Z, 'A': AXIS_A}

        # Angles to Steps conversions
        self.stepAngle = [360./2980, 0., 90./340, 0.]
        
        # Faster means less torque for X(El), Y, Z(Az), A
        # FIXME: read all from config
        self.sleep_ON  = (.005, .0075, .020, .0025)
        self.sleep_OFF = (.005, .0075, .020, .0025)
        # Dir change adjustment (CW, CCW) for X(El), Y , Z(Az), A
        self.dirChangeSteps = [(40, 40), (0, 0), (18, 18), (0, 0)]
        self.lastDir = [DIR_CW, DIR_CW, DIR_CW, DIR_CW]
        
        super(Pointer, self).__init__()
        
        # Threads for each axis
        self.Axes = []
        for i, name in enumerate(['X', 'Y', 'Z', 'A']): 
            self.Axes.append(Axis(self.PORTS[i]))
            self.Axes[i].name=name
            self.Axes[i].set_sleep((self.sleep_ON[i], self.sleep_OFF[i]))
            self.Axes[i].set_dirChangeSteps(self.dirChangeSteps[i])

    def setSpeed(self, axesNames):
        """ High level speed setting for each axis
            Speed Units are degrees/second
        """
        for axis, speed in axesNames.items():
            ax = self.axes[axis]
            # convert to steps/s
            steps = float(speed) * self.stepAngle[ax]
            delay = 1./steps
            self.Axes[ax].set_sleep((delay/2., delay/2.))

    def setDirChangeSteps(self, axesNames):
        """ High level direction change extra steps for each axis
            Format is (CW, CCW)
            Units are steps
        """
        for axis, steps in axesNames.items():
            ax = self.axes[axis]
            self.Axes[ax].set_dirChangeSteps(steps)
        
    def move(self, axes):
        """High-level Simultaneous Axis Move Function
           Threaded Version 
           Simultaneously move each axis from 'axes', their given number of steps
           A negative step is CCW
        """
        for axis, step in axes.items():
            self.Axes[axis].put_request(step)

    def moveAngles(self, axesNames):
        """Simultaneously move each axis from 'axesNames' the given angle
           Angles are in degrees
           A negative angle means CCW
        """
        ax = dict()
        for axis, angle in axesNames.items():
            print axis, angle
            steps = angle / self.stepAngle[self.axes[axis]]
            ax[self.axes[axis]] = int(round(steps))
        self.move(ax)
    
    def moveAzEl(self, azimuth, elevation):
        """Simultaneously move in azimuth and elevation
           Angles are in degrees
           A negative angle means CCW
        """
        # Concurrent movements
        ax=dict()
        for axis, angles in zip(('Az', 'El'), (azimuth, elevation)): 
            ax[axis] = float(angles)
        self.moveAngles(ax)

    def pointAngles(self, axesNames):
        """Simultaneously point each axis from 'axesNames' to the given angle
           Angles are in degrees
           A negative angle means CCW
        """
        ax = dict()
        for axis, angle in axesNames.items():
            axis = self.axes[axis]
            steps = angle / self.stepAngle[axis]
            pos = self.Axes[axis].get_pos()
            print axis, angle, pos, steps,  
            ax[axis] = round(steps-pos)
            print 'delta:', ax[axis]
        self.move(ax)
        
    def pointAzEl(self, azimuth, elevation):
        """Simultaneously point in azimuth and elevation
           Angles are in degrees
           A negative angle means CCW
        """
        # Concurrent movements
        ax=dict()
        for axis, angles in zip(('Az', 'El'), (azimuth, elevation)): 
            ax[axis] = float(angles)
        self.pointAngles(ax)
        
    def pointAz(self, azimuth):
        """Only point in Azimuth, leaving Elevation unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['Az'] = float(azimuth)
        self.pointAngles(ax)
        
    def pointEl(self, elevation):
        """Only point in Elevation, leaving Azimuth unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['El'] = float(elevation)
        self.pointAngles(ax)

    def getAngles(self, axesNames):
        """Get each axis from 'axesNames' to the given angle(step)
           Angles are in degrees
           A negative angle means CCW
        """
        for axis in axesNames.keys():
            ax = self.axes[axis]
            pos = self.Axes[ax].get_pos()
            angles = pos * self.stepAngle[ax]
            axesNames[axis] = angles
        return axesNames

    def getAzEl(self):
        """Get actual absolute Azimuth and Elevation angles
           Returned angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['Az'] = 0
        ax['El'] = 0
        ax = self.getAngles(ax)
        return ax['Az'], ax['El']
    
    def setAngles(self, axesNames):
        """Set each axis from 'axesNames' to the given angle(step)
           Angles are in degrees
           A negative angle means CCW
        """
        for axis, angle in axesNames.items():
            axis = self.axes[axis]
            steps = float(angle) / self.stepAngle[axis]
            self.Axes[axis].set_pos(steps)

    def setAzEl(self, azimuth=0., elevation=0.):
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
        self.setAngles(ax)
        
    def setEl(self, elevation=0.):
        """Set absolute Elevation to actual elevation axis position, leaving azimuth axis unchanged
           Angles are in degrees
           A negative angle means CCW
        """
        ax=dict()
        ax['El'] = elevation
        self.setAngles(ax)
                 
if __name__ == '__main__':
    if len(sys.argv) < 3 or not len(sys.argv) & 1:
        print >>sys.stderr, "Usage: %s <axis> <angle> ...\naxis : {Az|El|X|Y|Z|A}\nangle: Angle in degrees(- = CCW)" % sys.argv[0]
        sys.exit(1)
    
    pointer = Pointer()

    # Concurrent movements
    ax=dict()
    for axis, angles in zip(sys.argv[1::2], sys.argv[2::2]): 
        ax[axis] = float(angles)
    pointer.moveAngles(ax)
    time.sleep(3) # give time to the threads to process the requests
