# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *

# -*- encoding: UTF-8 -*-

''' Walk: Small example to make Nao walk '''
'''       with gait customization        '''
'''       NAO is Keyser Soze             '''
''' This example is only compatible with NAO '''

import time
import almath
from naoqi import ALProxy

def main():

    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0

    # Defined a limp walk
    try:
        motionProxy.moveToward(X, Y, Theta,[["Frequency", Frequency],
                                            # LEFT FOOT
                                            ["LeftStepHeight", 0.02],
                                            ["LeftTorsoWy", 5.0*almath.TO_RAD],
                                            # RIGHT FOOT
                                            ["RightStepHeight", 0.005],
                                            ["RightMaxStepX", 0.001],
                                            ["RightMaxStepFrequency", 0.0],
                                            ["RightTorsoWx", -7.0*almath.TO_RAD],
                                            ["RightTorsoWy", 5.0*almath.TO_RAD]] )
    except Exception, errorMsg:  # type: ignore
        print str(errorMsg)  # type: ignore
        print "This example is not allowed on this robot."  # type: ignore
        exit()

    time.sleep(4.0)

    try:
        motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:  # type: ignore
        print str(errorMsg)  # type: ignore
        print "This example is not allowed on this robot."  # type: ignore
        exit()  

    time.sleep(4.0)

    # stop walk in the next double support
    motionProxy.stopMove()

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    main()