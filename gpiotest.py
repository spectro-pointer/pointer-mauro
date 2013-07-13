#!/usr/bin/python


# 1. First set up RPi.GPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

for port in range(1, 26+1):
    print "%d:" % port,

    try:
        GPIO.setup(port, GPIO.OUT)
    except ValueError:
        print "Invalid port."
        continue

    # 2. To set an output high:
    GPIO.output(port, True)
    print "On", 
    time.sleep(1)

    # 3. To set an output low:
    GPIO.output(port, False)
    print "Off" 
    time.sleep(1)

#4. Clean up at the end of your program
GPIO.cleanup()
