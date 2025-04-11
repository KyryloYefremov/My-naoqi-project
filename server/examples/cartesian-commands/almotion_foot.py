# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

'''Cartesian control: Torso and Foot trajectories'''
''' This example is only compatible with NAO '''

import motion
import almath
from naoqi import ALProxy
from config import *


def main():
    ''' Example of a cartesian foot trajectory
    Warning: Needs a PoseInit before executing
    '''

    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    frame      = motion.FRAME_WORLD
    axisMask   = motion.AXIS_MASK_ALL   # full control
    useSensorValues = False

    # Lower the Torso and move to the side
    effector = "Torso"
    initTf   = almath.Transform(
        motionProxy.getTransform(effector, frame, useSensorValues))
    deltaTf  = almath.Transform(0.0, -0.06, -0.03) # x, y, z
    targetTf = initTf*deltaTf
    path     = list(targetTf.toVector())
    times    = 2.0 # seconds
    motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

    # LLeg motion
    effector = "LLeg"
    initTf = almath.Transform()

    try:
        initTf = almath.Transform(motionProxy.getTransform(effector, frame, useSensorValues))
    except Exception, errorMsg:  # type: ignore
        print str(errorMsg)  # type: ignore
        print "This example is not allowed on this robot."  # type: ignore
        exit()

    # rotation Z
    deltaTf  = almath.Transform(0.0, 0.04, 0.0)*almath.Transform().fromRotZ(45.0*almath.TO_RAD)
    targetTf = initTf*deltaTf
    path     = list(targetTf.toVector())
    times    = 2.0 # seconds

    motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    main()