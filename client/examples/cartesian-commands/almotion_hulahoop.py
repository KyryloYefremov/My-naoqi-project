# -*- encoding: UTF-8 -*-
'''Motion: Hula Hoop (Python 3 Version)'''

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

import os
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R
from naoqi3 import ALProxy
import motion
from config import *

def create_transform(translation=None, rotation=None):
    """Create 4x4 transform matrix from translation and/or rotation"""
    tf = np.eye(4)
    if translation is not None:
        tf[:3, 3] = translation
    if rotation is not None:
        tf[:3, :3] = R.from_euler('xyz', rotation, degrees=False).as_matrix()
    return tf

def main():
    '''Hula Hoop Motion using Cartesian control'''
    
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot and stand
    motion_proxy.wakeUp()
    posture_proxy.goToPosture("StandInit", 0.5)

    # Motion parameters
    effector = "Torso"
    frame = motion.FRAME_ROBOT
    axis_mask = motion.AXIS_MASK_ALL
    use_sensor = False

    # Get current transform
    current_tf = np.array(motion_proxy.getTransform(effector, frame, use_sensor)).reshape(4,4)
    current_pos = current_tf[:3, 3]

    # Movement parameters
    dx = 0.03  # X translation (meters)
    dy = 0.03  # Y translation (meters)
    dw = 8.0 * np.pi/180  # Rotation (8° in radians)

    # Define the four key poses
    # Point 1: forward / bend backward
    tf1 = create_transform([dx, 0, 0]) @ create_transform(rotation=[0, -dw, 0])
    
    # Point 2: right / bend left
    tf2 = create_transform([0, -dy, 0]) @ create_transform(rotation=[-dw, 0, 0])
    
    # Point 3: backward / bend forward
    tf3 = create_transform([-dx, 0, 0]) @ create_transform(rotation=[0, dw, 0])
    
    # Point 4: left / bend right
    tf4 = create_transform([0, dy, 0]) @ create_transform(rotation=[dw, 0, 0])

    # Build path (2 full circles + return)
    path = []
    for tf in [tf1, tf2, tf3, tf4] * 2 + [tf1, np.eye(4)]:
        final_tf = current_tf @ tf
        path.append(final_tf.flatten().tolist())

    # Timing (0.5s per movement)
    times = [0.5 * (i+1) for i in range(len(path))]

    # Execute motion
    motion_proxy.transformInterpolations(effector, frame, path, axis_mask, times)

    # Rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()