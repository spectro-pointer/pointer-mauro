#!/usr/bin/python


# 1. First set up RPi.GPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ports = (11,)
for port in ports:
    try:
        GPIO.setup(port, GPIO.OUT)
    except ValueError:
        print "Invalid port:", port
        continue

state=True
while True:
    for port in ports:
        print "%d:" % port,
        if state:
            print 'On'
        else:
            print 'Off'
        GPIO.output(port, state)
    state = not state
    time.sleep(1)
GPIO.cleanup()
