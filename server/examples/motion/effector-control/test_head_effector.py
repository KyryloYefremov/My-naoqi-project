# -*- encoding: UTF-8 -*-

''' Whole Body Motion: Head orientation control '''
''' This example is only compatible with NAO '''

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *

import time
import math
from naoqi import ALProxy

def main():
    ''' Example of a whole body head orientation control
        Warning: Needs a PoseInit before executing
                 Whole body balancer must be inactivated at the end of the script
    '''

    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    effectorName = "Head"

    # Active Head tracking
    isEnabled    = True
    motionProxy.wbEnableEffectorControl(effectorName, isEnabled)

    # Example showing how to set orientation target for Head tracking
    # The 3 coordinates are absolute head orientation in NAO_SPACE
    # Rotation in RAD in x, y and z axis

    # X Axis Head Orientation feasible movement = [-20.0, +20.0] degree
    # Y Axis Head Orientation feasible movement = [-75.0, +70.0] degree
    # Z Axis Head Orientation feasible movement = [-30.0, +30.0] degree

    targetCoordinateList = [
    [+20.0,  00.0,  00.0], # target 0
    [-20.0,  00.0,  00.0], # target 1
    [ 00.0, +70.0,  00.0], # target 2
    [ 00.0, +70.0, +30.0], # target 3
    [ 00.0, +70.0, -30.0], # target 4
    [ 00.0, -75.0,  00.0], # target 5
    [ 00.0, -75.0, +30.0], # target 6
    [ 00.0, -75.0, -30.0], # target 7
    [ 00.0,  00.0,  00.0], # target 8
    ]

    # wbSetEffectorControl is a non blocking function
    # time.sleep allow head go to his target
    # The recommended minimum period between two successives set commands is
    # 0.2 s.
    for targetCoordinate in targetCoordinateList:
        targetCoordinate = [target*math.pi/180.0 for target in targetCoordinate]
        motionProxy.wbSetEffectorControl(effectorName, targetCoordinate)
        time.sleep(3.0)

    # Deactivate Head tracking
    isEnabled = False
    motionProxy.wbEnableEffectorControl(effectorName, isEnabled)

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    main()