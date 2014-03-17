#!/usr/bin/python


# 1. First set up RPi.GPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ports = (21, 23)
for port in ports:
    try:
        GPIO.setup(port, GPIO.IN)
    except ValueError:
        print "Invalid port:", port
        continue

while True:
    for port in ports:
        print "%d:" % port,

        if GPIO.input(port):
            print "On"
        else:
            print "Off"
    time.sleep(1)
GPIO.cleanup()
