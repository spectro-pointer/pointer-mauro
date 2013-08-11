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

from time import sleep

if __name__ == '__main__':
    accel = Accelerometer()

    while True:
        print(accel.getAxes())
        sleep(1)
