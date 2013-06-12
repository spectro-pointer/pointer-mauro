#!/usr/bin/env python
# Generic pointer driver
#
#(C) 2013 Mauro Lacy <mauro@lacy.com.ar>
# this is distributed under a free software license, see license.txt

import sys, time
sys.path.insert(0, '..')
import parallel

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
        """set data to the Pointer"""
        self.data = data
        self.p.setData(self.data)

class Pointer(EightBitIO):
    def __init__(self):
        self.p = parallel.Parallel()
        
        self.sleep_ON  = .0075
        self.sleep_OFF = .0075
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
        
        super(Pointer, self).__init__()
        
    def move(self, axis, steps=STEP_ONE, dir=DIR_CW):
        """Move 'axis' a 'steps' number of steps in direction 'dir'"""
        if (AXIS_X <= axis <= AXIS_A) and steps >0 and dir in (DIR_CW, DIR_CCW):
            pins=self.PINS[axis]
            port=self.PORT(axis)

            if port == self.PORT_DATA:
                bits=(self.DATA_BIT(pins[0]), self.DATA_BIT(pins[1]))
                data=(1<<bits[0]) | (dir<<(bits[1]))
                for i in range(steps):
                    print "step", i+1
                    self.out(data)
                    time.sleep(self.sleep_ON)
                    self.out(0)
                    time.sleep(self.sleep_OFF)
            elif port == self.PORT_CTRL:
                stepFunction = self.CTRL_FUN[pins[0]]
                dirFunction  = self.CTRL_FUN[pins[1]]
                # set dir
                dirFunction(dir)
                # set steps
                for i in range(steps):
                    print "step", i+1
                    stepFunction(1)
                    time.sleep(self.sleep_ON)
                    stepFunction(0)
                    time.sleep(self.sleep_OFF)
            else:
                print "ERROR: axis %d steps %d dir %d" %(axis, steps, dir)
        else:
            print "ERROR: axis %d steps %d dir %d" %(axis, steps, dir)

if __name__ == '__main__':
    pointer = Pointer()

    if len(sys.argv) != 4 or int(sys.argv[2]) <= 0 or sys.argv[3] not in ('CW', 'CCW'):
        print >>sys.stderr, "Usage: %s <axis> <steps> <dir>\naxis : {X|Y|Z|A}\nsteps: Number of steps\ndir  : {CW|CCW}" % sys.argv[0]
        sys.exit(1)
    axis = {'X': AXIS_X, 'Y': AXIS_Y, 'Z': AXIS_Z, 'A': AXIS_A}
    dirs = {'CW': DIR_CW, 'CCW': DIR_CCW}
    axis = axis[sys.argv[1]]
    steps=  int(sys.argv[2])
    dir  = dirs[sys.argv[3]]

    print "axis: %s, dir: %s, steps: %d" % (sys.argv[1], sys.argv[3], steps)
    pointer.move(axis, steps, dir)
