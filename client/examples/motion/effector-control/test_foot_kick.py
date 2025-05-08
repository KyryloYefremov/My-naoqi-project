# -*- encoding: UTF-8 -*-
''' Whole Body Motion: kick (Python 3 version) '''

import os
import sys
# Locate config file
sys.path.insert(0, os.getcwd())
from config import *

import time
import math
import numpy as np
from scipy.spatial.transform import Rotation as R
from naoqi3 import ALProxy
import motion


def compute_path(proxy, effector, frame):
    """Calculate kick trajectory path"""
    dx = 0.05                 # translation X (meters)
    dz = 0.05                 # translation Z (meters)
    dwy = math.radians(5.0)   # rotation Y (5 degrees in radians)

    try:
        current_tf = np.array(proxy.getTransform(effector, frame, False)).reshape(4,4)
    except Exception as error_msg:
        print(error_msg)
        print("This example is not allowed on this robot.")
        sys.exit(1)

    path = []
    
    # Position 1: Back and up with rotation
    tf1 = current_tf @ create_transform([-dx, 0.0, dz]) @ create_transform(rotation=[0, dwy, 0])
    path.append(tf1.flatten().tolist())
    
    # Position 2: Forward and up
    tf2 = current_tf @ create_transform([dx, 0.0, dz])
    path.append(tf2.flatten().tolist())
    
    # Position 3: Return to original
    path.append(current_tf.flatten().tolist())
    
    return path

def create_transform(translation=None, rotation=None):
    """Create 4x4 transform matrix"""
    tf = np.eye(4)
    if translation is not None:
        tf[:3, 3] = translation
    if rotation is not None:
        tf[:3, :3] = R.from_euler('xyz', rotation).as_matrix()
    return tf

def main():
    """Execute whole body kick motion"""
    
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up and stand
    motion_proxy.wakeUp()
    posture_proxy.goToPosture("StandInit", 0.5)

    # Activate whole body control
    motion_proxy.wbEnable(True)

    # Set up balance constraints
    motion_proxy.wbFootState("Fixed", "Legs")
    motion_proxy.wbEnableBalanceConstraint(True, "Legs")

    # Shift weight to left leg
    motion_proxy.wbGoToBalance("LLeg", 2.0)

    # Prepare right leg for kicking
    motion_proxy.wbFootState("Free", "RLeg")
    effector = "RLeg"
    axis_mask = 63  # All axes
    frame = motion.FRAME_WORLD

    # Execute right leg kick
    kick_times = [2.0, 2.7, 4.5]
    path = compute_path(motion_proxy, effector, frame)
    motion_proxy.transformInterpolations(effector, frame, path, axis_mask, kick_times)

    # Shift weight to right leg
    motion_proxy.wbGoToBalance("RLeg", 2.0)

    # Prepare left leg for kicking
    motion_proxy.wbFootState("Free", "LLeg")
    effector = "LLeg"
    path = compute_path(motion_proxy, effector, frame)
    motion_proxy.transformInterpolations(effector, frame, path, axis_mask, kick_times)

    time.sleep(1.0)

    # Deactivate whole body control
    motion_proxy.wbEnable(False)
    posture_proxy.goToPosture("StandInit", 0.3)
    motion_proxy.rest()

if __name__ == "__main__":
    main()