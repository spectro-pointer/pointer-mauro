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

PINS=((17, 16), (14, 1), (2, 3), (4, 5)) # (STEP, DIR) pins for earch axis

PORT_DATA=0
PORT_CTRL=1
PORT_STAT=2 # Not used
PORT=(-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 2, 1, 1) # port(data/ctrl/status) for each pin
# Data bit for earch pin (DATA, CTRL, STAT)
BIT =((-1, -1, 0, 1, 2, 3, 4, 5, 6, 7), (-1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 2, 3), (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 5, 4, -1, 3))

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
        
#    def toggleE(self):
#        """toggle enable pin"""
#        self.p.setDataStrobe(1)     #toggle LCD_E, the enable pin
#        #~ time.sleep(0.001)
#        self.p.setDataStrobe(0)     #back to inactive position
#        #~ time.sleep(0.001)

    def out(self, data):
        """set data to the Pointer"""
        self.data = data
        self.p.setData(self.data)

#    def putc(self, c):
#        """send a data byte to the LCD"""
#        self.setRS(1)
#        self.setRW(0)
#        self.out(ord(c))
#        self.toggleE()              #toggle LCD_E, the enable pin
#        time.sleep(0.001)           #wait until instr is finished


class Pointer(EightBitIO):
    def __init__(self):
        self.p = parallel.Parallel()
        super(Pointer, self).__init__()
        
    def move(self, axis, steps=STEP_ONE, dir=DIR_CW):
        """Move 'axis' a 'steps' number of steps in direction 'dir'"""
        if (AXIS_X <= axis <= AXIS_A) and steps >0 and dir in (DIR_CW, DIR_CCW):
            pins=PINS[axis]
            port=PORT[pins[0]] # It's the same por for both pins
            bits=(BIT[port][pins[0]], BIT[port][pins[1]])
            data=(1<<bits[0]) | (dir<<(bits[1]))

            i=1
            print "Axis: %d, Steps: %d, Dir: %d" % (axis, steps, dir)
            while steps > 0:
                print "step %d: port %d, axis bit  %d, dir bit  %d, data 0x%02x" % (i, port, bits[0], bits[1], data)
                if port == PORT_DATA:
                    self.out(data)
                steps -= 1
                i += 1
            print
        else:
            print "ERROR: axis %d steps %d dir %d" %(axis, steps, dir)

if __name__ == '__main__':
    pointer = Pointer()
    pointer.move(AXIS_X, STEP_ONE, DIR_CW)
    pointer.move(AXIS_X, STEP_ONE, DIR_CCW)
    pointer.move(AXIS_Y, STEP_ONE, DIR_CW)
    pointer.move(AXIS_Y, STEP_ONE, DIR_CCW)
    pointer.move(AXIS_Z, STEP_ONE, DIR_CW)
    pointer.move(AXIS_Z, STEP_ONE, DIR_CCW)
    pointer.move(AXIS_A, STEP_ONE, DIR_CW)
    pointer.move(AXIS_A, STEP_ONE, DIR_CCW)
