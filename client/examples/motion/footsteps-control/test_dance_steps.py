# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
from config import *

''' setFootStep: Cha Cha Basic Steps using Python 3 '''
''' http://www.dancing4beginners.com/cha-cha-steps.htm '''
''' Compatible with NAO via naoqi3 interface '''

from naoqi3 import ALProxy

def main():
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()

    # Send robot to Stand Init
    posture_proxy.goToPosture("StandInit", 0.5)

    # Define dance steps [foot, [position]]
    foot_steps = [
        [["LLeg"], [[0.06, 0.1, 0.0]]],    # 1) Step forward left
        [["LLeg"], [[0.00, 0.16, 0.0]]],   # 2) Sidestep left
        [["RLeg"], [[0.00, -0.1, 0.0]]],   # 3) Right to left
        [["LLeg"], [[0.00, 0.16, 0.0]]],   # 4) Sidestep left
        [["RLeg"], [[-0.04, -0.1, 0.0]]],  # 5) Backward & left
        [["RLeg"], [[0.00, -0.16, 0.0]]],  # 6) Forward & right
        [["LLeg"], [[0.00, 0.1, 0.0]]],    # 7) Left to right
        [["RLeg"], [[0.00, -0.16, 0.0]]]   # 8) Sidestep right
    ]

    # Execute dance
    step_frequency = 0.8
    clear_existing = False
    dance_cycles = 2

    try:
        for _ in range(dance_cycles):
            for step in foot_steps:
                motion_proxy.setFootStepsWithSpeed(
                    step[0],       # Foot name
                    step[1],       # Position
                    [step_frequency],  # Speed
                    clear_existing
                )
    except Exception as error_msg:
        print(f"Error: {error_msg}")
        print("This example is not allowed on this robot.")
        sys.exit(1)

    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.rest()

if __name__ == "__main__":
    main()