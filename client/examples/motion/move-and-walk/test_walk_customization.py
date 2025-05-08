# -*- encoding: UTF-8 -*-
''' Walk: Small example to make Nao walk with gait customization '''

import os
import sys
# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
from config import *

import time
import numpy as np
from naoqi3 import ALProxy


def make_gait_param(name, value):
    """Ensure parameters are sent as regular strings, not unicode"""
    return [str(name), float(value)]

def main():
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()

    # Send robot to Stand Init
    posture_proxy.goToPosture("StandInit", 0.5)

    # TARGET VELOCITY
    X = 1.0
    Y = 0.0
    Theta = 0.0
    Frequency = 1.0

    # Define limp walk parameters with proper string encoding
    try:
        motion_proxy.moveToward(X, Y, Theta, [
            make_gait_param("Frequency", Frequency),
            # LEFT FOOT
            make_gait_param("LeftStepHeight", 0.02),
            make_gait_param("LeftTorsoWy", 5.0 * np.pi/180),
            # RIGHT FOOT
            make_gait_param("RightStepHeight", 0.005),
            make_gait_param("RightMaxStepX", 0.001),
            make_gait_param("RightMaxStepFrequency", 0.0),
            make_gait_param("RightTorsoWx", -7.0 * np.pi/180),
            make_gait_param("RightTorsoWy", 5.0 * np.pi/180)
        ])
    except Exception as error_msg:
        print(error_msg)
        print("This example is not allowed on this robot.")
        sys.exit(1)

    time.sleep(4.0)

    # Normal walk
    try:
        motion_proxy.moveToward(X, Y, Theta, [
            make_gait_param("Frequency", Frequency)
        ])
    except Exception as error_msg:
        print(error_msg)
        print("This example is not allowed on this robot.")
        sys.exit(1)

    time.sleep(4.0)

    motion_proxy.stopMove()
    motion_proxy.rest()

if __name__ == "__main__":
    main()