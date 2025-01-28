# python 2
import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)

from config import *
from naoqi import ALProxy


motionProxy  = ALProxy("ALMotion", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)

# Wake up robot
motionProxy.wakeUp()

# Send robot to Pose Init
postureProxy.goToPosture("StandInit", 0.5)

# Go to rest position
motionProxy.rest()

# print motion state
print(motionProxy.getSummary())