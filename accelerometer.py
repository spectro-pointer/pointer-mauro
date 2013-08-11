#!/usr/bin/python3

 
class Accelerometer(object):
    """ Accelerometer Driver
        ADXL345 Accelerometer Class driver
    """
    
    def __init__(self):
        from i2clibraries import i2c_adxl345
        self.adxl345 = i2c_adxl345.i2c_adxl345(1)
        self.adxl345.setScale(16) # 2, 4, 8, 16
 
    def getCoords(self):
        self.adxl345.wakeUp()
#        return self.adxl345.getRawAxes()
        return self.adxl345.getAxes()