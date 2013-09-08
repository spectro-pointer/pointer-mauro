#!/usr/bin/python3

class Accelerometer(object):
    """ Accelerometer Driver
        ADXL345 Accelerometer Class driver
    """
    def __init__(self):
        from i2clibraries import i2c_adxl345
        self.adxl345 = i2c_adxl345.i2c_adxl345(1)
        self.scale = 2 # 2, 4, 8, 16
        self.adxl345.setScale(self.scale)
 
    def getAxes(self):
        """ Get X,Y,Z accelerations
        """
        self.adxl345.wakeUp()
#        return self.adxl345.getRawAxes()
        return self.adxl345.getAxes()

import numpy
import math
class AnglesSensor(Accelerometer):
    """ Angles converter
        Uses Accelerometer to Report (Approximate) Inclination Angles
    """
    def __init__(self):
        """Orientation of Accelerometer wrt Pointer Body axes 
        """
        self.accelOrientation = numpy.array([1., -1., -1.])
        """ Angles Conversion""" 
        self.Angles = numpy.array([90./1., 90./1., 90/1.])
        
        super(AnglesSensor, self).__init__()
        
    def get(self):
        """ Use the accelerometer to (try to) measure angles
            Angles must be read when the device is not moving
        """
        
        axes = numpy.array(self.getAxes())
        axes /= numpy.linalg.norm(axes)
        print ('axes:', axes)
        axes[0] = math.degrees(math.acos(axes[0]))
#        if axes[2] > 0.:
        if axes[2]-axes[1] > 0.:
            axes[0] = 360. -axes[0]
        axes[1] = math.degrees(math.acos(axes[1]))
        axes[2] = math.degrees(math.acos(axes[2]))
        return list(axes)
    
from time import sleep
if __name__ == '__main__':
#    accel = Accelerometer()
    angles = AnglesSensor()

    while True:
#        print(accel.getAxes())
        print(angles.get())
        sleep(1)
