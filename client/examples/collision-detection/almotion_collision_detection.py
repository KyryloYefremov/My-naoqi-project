# -*- encoding: UTF-8 -*-
''' Collision detection: Arm collision detection test (Python 3) '''

import os
import sys
# Locate config file
sys.path.insert(0, os.getcwd())
from config import *


import time
import math
from naoqi3 import ALProxy


def move_arm(motion_proxy, target, robot_name, chain_name):
    '''Makes NAO bump on his Torso or Head with specified arm'''
    
    # Set movement speed
    max_speed_fraction = 0.5

    # Define target positions
    if target == "Torso":
        shoulder_pitch = 50
    elif target == "Head":
        shoulder_pitch = -50
    else:
        print("ERROR: Target must be 'Torso' or 'Head'")
        sys.exit(1)

    shoulder_roll = 6
    elbow_yaw = 0
    elbow_roll = -150

    # Set angles based on arm
    if chain_name == "LArm":
        target_angles = [shoulder_pitch, shoulder_roll, elbow_yaw, elbow_roll]
    elif chain_name == "RArm":
        target_angles = [shoulder_pitch, -shoulder_roll, -elbow_yaw, -elbow_roll]
    else:
        print("ERROR: chain_name must be 'LArm' or 'RArm'")
        sys.exit(1)

    # Adjust for robot model
    if robot_name in ["naoH25", "naoAcademics", "naoT14"]:
        target_angles.extend([0.0, 0.0])
    elif robot_name == "naoH21":
        pass
    elif robot_name == "naoT2":
        target_angles = []
    else:
        print("ERROR: Unsupported robot model")
        sys.exit(1)

    # Convert to radians
    target_angles = [math.radians(x) for x in target_angles]

    # Execute movement
    motion_proxy.angleInterpolationWithSpeed(
        chain_name, target_angles, max_speed_fraction)

def main():
    '''Demonstrates collision detection by bumping torso and head'''
    
    chain_name = "LArm"  # Can be changed to "RArm"

    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()
    posture_proxy.goToPosture("StandInit", 0.5)

    # Get robot configuration
    robot_config = motion_proxy.getRobotConfig()
    robot_name = ""
    for i, name in enumerate(robot_config[0]):
        if name == "Model Type":
            robot_name = robot_config[1][i]
            break

    def test_collision(target, enable_protection):
        '''Helper function to test collision scenarios'''
        print(f"\nTesting {target} with protection {'ON' if enable_protection else 'OFF'}")
        
        success = motion_proxy.setCollisionProtectionEnabled(chain_name, enable_protection)
        if not success:
            print(f"Failed to {'enable' if enable_protection else 'disable'} collision protection")
        
        time.sleep(1.0)
        move_arm(motion_proxy, target, robot_name, chain_name)
        time.sleep(1.0)
        posture_proxy.goToPosture("StandInit", 1.0)

    # Test torso collisions
    test_collision("Torso", False)  # Protection OFF
    test_collision("Torso", True)   # Protection ON

    # Test head collisions
    test_collision("Head", False)   # Protection OFF
    test_collision("Head", True)    # Protection ON

    # Rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()