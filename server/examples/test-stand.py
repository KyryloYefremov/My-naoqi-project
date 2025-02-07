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

motionProxy.wakeUp()

# Send robot to Pose Init
try:
    result = postureProxy.goToPosture("StandInit", 0.5)
    print("RESULT GO TO: ", result)
except Exception as e:
    print("Chyba pri vykonavani prikazu:", e)


# Go to rest position
motionProxy.rest()