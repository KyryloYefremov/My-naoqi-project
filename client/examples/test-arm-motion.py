# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)

''' Whole Body Motion: ARM orientation control '''
''' This example is only compatible with NAO '''


from config import *

import time
from naoqi3 import ALProxy


motionProxy  = ALProxy("ALMotion", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)

# Wake up robot
motionProxy.wakeUp()

# Send robot to Pose Init
postureProxy.goToPosture("StandInit", 0.5)

motionProxy.wbEnable(True)

# Example showing how to set orientation target for LArm tracking.
effectorName = "LArm"

motionProxy.wbEnableEffectorControl(effectorName, True)
time.sleep(2.0)
targetCoordinate = [0.20, 0.12, 0.30]
motionProxy.wbSetEffectorControl(effectorName, targetCoordinate)

time.sleep(4.0)
motionProxy.wbEnable(False)

# Go to rest position
motionProxy.rest()