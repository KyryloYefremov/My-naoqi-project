# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

'''Cartesian control: Torso and Foot trajectories (Python 3)'''

import numpy as np
from scipy.spatial.transform import Rotation as R
from naoqi3 import ALProxy
import motion
from config import *

def create_transform(translation, rotation=None):
    """Create 4x4 transform matrix from translation and rotation"""
    tf = np.eye(4)
    tf[:3, 3] = translation
    if rotation is not None:
        tf[:3, :3] = R.from_euler('z', rotation, degrees=True).as_matrix()
    return tf

def main():
    ''' Example of a cartesian foot trajectory '''
    
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()

    # Send to Stand Init
    posture_proxy.goToPosture("StandInit", 0.5)

    # Preserve original motion constants
    frame = motion.FRAME_WORLD (1)
    axis_mask = motion.AXIS_MASK_ALL (63)
    use_sensor = False

    # Torso movement
    effector = "Torso"
    init_tf = np.array(motion_proxy.getTransform(effector, frame, use_sensor)).reshape(4,4)
    
    # Create translation transform (-0.06y, -0.03z)
    delta_tf = create_transform([0.0, -0.06, -0.03])
    target_tf = init_tf @ delta_tf  # Matrix multiplication
    motion_proxy.transformInterpolations(
        effector, frame, [target_tf.flatten().tolist()], axis_mask, [2.0])

    # Leg movement
    effector = "LLeg"
    try:
        init_tf = np.array(motion_proxy.getTransform(effector, frame, use_sensor)).reshape(4,4)
    except Exception as error_msg:
        print(error_msg)
        print("This example is not allowed on this robot.")
        exit()

    # Create transform (0.04y translation + 45° Z rotation)
    translation_tf = create_transform([0.0, 0.04, 0.0])
    rotation_tf = create_transform([0,0,0], 45)
    delta_tf = translation_tf @ rotation_tf
    target_tf = init_tf @ delta_tf
    
    motion_proxy.transformInterpolations(
        effector, frame, [target_tf.flatten().tolist()], axis_mask, [2.0])

    # Rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()