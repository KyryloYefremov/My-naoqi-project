# -*- encoding: UTF-8 -*-
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi3 import ALProxy


def main():

    # Create proxy to ALMemory
    try:
        memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception as e:
        print("Could not create proxy to ALMemory")
        print("Error was: ", e)

    # Create proxy to ALSonar
    try:
        sonarProxy = ALProxy("ALSonar", IP, PORT)
    except Exception as e:  
        print("Could not create proxy to ALSonar")
        print("Error was: ", e)

    # Subscribe to sonars, this will launch sonars (at hardware level)
    # and start data acquisition.
    sonarProxy.subscribe("myApplication")

    # Now you can retrieve)sonar data from ALMemory.
    # Get sonar left first echo (distance in meters to the first obstacl)
    left_value = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")

    # Same thing for right.
    right_value = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    print("Left sonar value: ", left_value)
    print("Right sonar value: ", right_value)

    # Unsubscribe from sonars, this will stop sonars (at hardware level)
    sonarProxy.unsubscribe("myApplication")

    # Please read Sonar ALMemory keys section
    # if you want to know the other values you can get.


if __name__ == "__main__":
    main()