#!/usr/bin/python3

import time
import sys

from util import Thread
from gps import *

class GpsPoller(Thread):
    def __init__(self, server='localhost'):
        Thread.__init__(self)
        self.setDaemon(True)
        self.session = gps(host=server, mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.current_value = None

    def get(self):
        return self.current_value

    def run(self):
        try:
            while not self.shallStop:
                self.current_value = next(self.session)
        except StopIteration:
            pass

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Usage: %s <host>" % sys.argv[0])
        sys.exit(1)
    
    g = GpsPoller(server=sys.argv[1])
    g.start()
    while True:
        try:
            time.sleep(1)
            gpsData = g.get()
#            print(gpsData)
            for k in gpsData.keys():
                print("%s: %s" % (k, gpsData[k]))
            print()
            print(gpsData['lat'], gpsData['lon'])
        except (KeyError, AttributeError):
            pass
        except (KeyboardInterrupt, SystemExit):
            g.shutdown()
            break
    print()