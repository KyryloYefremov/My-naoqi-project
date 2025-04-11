# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

'''Motion: Hula Hoop'''
''' This example is only compatible with NAO '''

import motion
import almath
from naoqi import ALProxy
from config import *


def main():
    '''
         Example showing a Hula Hoop Motion
         with the NAO cartesian control of torso
    '''

    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # end initialize proxy, begin go to Stand Init

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    # end go to Stand Init, begin define control point
    effector        = "Torso"
    frame           =  motion.FRAME_ROBOT
    axisMask        = motion.AXIS_MASK_ALL
    isAbsolute      = True
    useSensorValues = False

    currentTf = almath.Transform(motionProxy.getTransform(effector, frame, useSensorValues))

    # end define control point, begin define target

    # Define the changes relative to the current position
    dx         = 0.03                    # translation axis X (meter)
    dy         = 0.03                    # translation axis Y (meter)
    dwx        = 8.0*almath.TO_RAD       # rotation axis X (rad)
    dwy        = 8.0*almath.TO_RAD       # rotation axis Y (rad)

    # point 01 : forward  / bend backward
    target1Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target1Tf *= almath.Transform(dx, 0.0, 0.0)
    target1Tf *= almath.Transform().fromRotY(-dwy)

    # point 02 : right    / bend left
    target2Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target2Tf *= almath.Transform(0.0, -dy, 0.0)
    target2Tf *= almath.Transform().fromRotX(-dwx)

    # point 03 : backward / bend forward
    target3Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target3Tf *= almath.Transform(-dx, 0.0, 0.0)
    target3Tf *= almath.Transform().fromRotY(dwy)

    # point 04 : left     / bend right
    target4Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
    target4Tf *= almath.Transform(0.0, dy, 0.0)
    target4Tf *= almath.Transform().fromRotX(dwx)

    path = []
    path.append(list(target1Tf.toVector()))
    path.append(list(target2Tf.toVector()))
    path.append(list(target3Tf.toVector()))
    path.append(list(target4Tf.toVector()))

    path.append(list(target1Tf.toVector()))
    path.append(list(target2Tf.toVector()))
    path.append(list(target3Tf.toVector()))
    path.append(list(target4Tf.toVector()))

    path.append(list(target1Tf.toVector()))
    path.append(list(currentTf.toVector()))

    timeOneMove  = 0.5 #seconds
    times = []
    for i in range(len(path)):
        times.append((i+1)*timeOneMove)

    # end define target, begin call motion api

    # call the cartesian control API

    motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motionProxy.rest()

    # end script

if __name__ == "__main__":
    main()