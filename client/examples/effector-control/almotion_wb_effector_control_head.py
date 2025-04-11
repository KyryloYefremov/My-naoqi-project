# -*- encoding: UTF-8 -*-
''' Whole Body Motion: Head orientation control (Python 3) '''

import os
import sys
# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
from config import *

import time
import math
from naoqi3 import ALProxy


def main():
    '''Demonstrates whole body head orientation control'''
    
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot and stand
    motion_proxy.wakeUp()
    posture_proxy.goToPosture("StandInit", 0.5)

    effector_name = "Head"

    # Activate head tracking
    motion_proxy.wbEnableEffectorControl(effector_name, True)

    # Head orientation targets in degrees [X, Y, Z]
    # X: [-20.0, +20.0], Y: [-75.0, +70.0], Z: [-30.0, +30.0]
    target_coordinates = [
        [+20.0,  00.0,  00.0],  # target 0
        [-20.0,  00.0,  00.0],  # target 1
        [ 00.0, +70.0,  00.0],  # target 2
        [ 00.0, +70.0, +30.0],  # target 3
        [ 00.0, +70.0, -30.0],  # target 4
        [ 00.0, -75.0,  00.0],  # target 5
        [ 00.0, -75.0, +30.0],  # target 6
        [ 00.0, -75.0, -30.0],  # target 7
        [ 00.0,  00.0,  00.0],  # target 8 (center)
    ]

    # Convert to radians and execute each movement
    for target in target_coordinates:
        target_rad = [math.radians(angle) for angle in target]
        motion_proxy.wbSetEffectorControl(effector_name, target_rad)
        time.sleep(3.0)  # Allow time to reach target

    # Deactivate head tracking
    motion_proxy.wbEnableEffectorControl(effector_name, False)

    # Rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()