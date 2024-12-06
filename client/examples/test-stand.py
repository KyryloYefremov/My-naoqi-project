from config import *
from naoqi3 import ALProxy

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