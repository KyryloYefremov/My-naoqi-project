# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

'''Cartesian control: Arm trajectory example'''
''' This example is only compatible with NAO '''

import motion
import almath
from naoqi import ALProxy
from config import *

''' Example showing a path of two positions
Warning: Needs a PoseInit before executing
'''

motionProxy  = ALProxy("ALMotion", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)

# Wake up robot
motionProxy.wakeUp()

# Send robot to Stand Init
postureProxy.goToPosture("StandInit", 0.5)

effector   = "LArm"
frame      = motion.FRAME_TORSO
axisMask   = almath.AXIS_MASK_VEL # just control position
print type(axisMask) # type: ignore
useSensorValues = False

path = []
currentTf = motionProxy.getTransform(effector, frame, useSensorValues)  # v cem jsou ty jednotky?
print type(currentTf) # type: ignore
targetTf  = almath.Transform(currentTf)
print "\n\n\n" #type: ignore
print type(targetTf) # type: ignore
targetTf.r1_c4 += 0.03 # x
targetTf.r2_c4 += 0.03 # y

path.append(list(targetTf.toVector()))
path.append(currentTf)

# Go to the target and back again
times      = [2.0, 4.0] # seconds

motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

# Go to rest position
motionProxy.rest()