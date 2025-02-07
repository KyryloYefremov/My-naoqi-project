# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)

''' Whole Body Motion: Head orientation control '''
''' This example is only compatible with NAO '''

# TODO: Fix problem with example test-head-motion.py

from config import *

import time
import math
from naoqi3 import ALProxy


''' Example of a whole body head orientation control
    Warning: Needs a PoseInit before executing
                Whole body balancer must be inactivated at the end of the script
'''

motionProxy  = ALProxy("ALMotion", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)

# Wake up robot
motionProxy.wakeUp()

# Send robot to Stand Init
result = postureProxy.goToPosture("StandInit", 0.5)
if result:

    # Active Head tracking
    motionProxy.wbEnable(True)

    effectorName = "Head"
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
    i = 1
    for targetCoordinate in targetCoordinateList:
        targetCoordinate = [target*math.pi/180.0 for target in targetCoordinate]
        res = motionProxy.wbSetEffectorControl(effectorName, targetCoordinate)
        print(f"RESULT: {res}")
        tts.say(str(i))
        time.sleep(8.0)
        i += 1

    # Deactivate Head tracking
    # isEnabled = False
    # motionProxy.wbEnableEffectorControl(effectorName, isEnabled)
    motionProxy.wbEnable(False)

    time.sleep(2.0)

    # Go to rest position
    motionProxy.rest()