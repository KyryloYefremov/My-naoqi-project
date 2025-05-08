# -*- encoding: UTF-8 -*-
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy
import time


def main():

    # Create proxy to ALMemory
    try:
        memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception, e: # type: ignore
        print "Could not create proxy to ALMemory" # type: ignore
        print "Error was: ", e # type: ignore

    # Create proxy to ALSonar
    try:
        sonarProxy = ALProxy("ALSonar", IP, PORT)
    except Exception, e:  # type: ignore
        print "Could not create proxy to ALSonar" # type: ignore
        print "Error was: ", e # type: ignore

    # Subscribe to sonars, this will launch sonars (at hardware level)
    # and start data acquisition.
    sonarProxy.subscribe("myApplication")

    # Now you can retrieve sonar data from ALMemory.
    # Get sonar left first echo (distance in meters to the first obstacle).
    left_value = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")

    # Same thing for right.
    right_value = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    print "Left sonar value: ", left_value # type: ignore
    print "Right sonar value: ", right_value # type: ignore

    # Unsubscribe from sonars, this will stop sonars (at hardware level)
    sonarProxy.unsubscribe("myApplication")

    # Please read Sonar ALMemory keys section
    # if you want to know the other values you can get.


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Execution time: {:.3f} seconds".format(end - start))