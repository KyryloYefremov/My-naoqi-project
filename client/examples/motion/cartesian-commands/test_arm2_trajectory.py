# -*- encoding: UTF-8 -*-
'''Cartesian control: Arm trajectory example (Python 3)'''

import os
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from naoqi3 import ALProxy
import motion
from config import *


def create_transform_matrix(position_offset, rotation=None):
    """Create a 4x4 transformation matrix from position offset and optional rotation"""
    tf = np.eye(4)
    tf[:3, 3] = position_offset  # Set translation components
    if rotation is not None:
        tf[:3, :3] = R.from_euler('xyz', rotation).as_matrix()
    return tf


def main():
    ''' Example showing a hand ellipsoid path '''
    
    # Initialize proxies using Python 3 interface
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()

    # Send robot to Stand Init
    posture_proxy.goToPosture("StandInit", 0.5)

    effector = "LArm"
    frame      = motion.FRAME_TORSO
    axisMask   = motion.AXIS_MASK_VEL
    use_sensor_values = False

    path = []
    current_tf = motion_proxy.getTransform(effector, frame, use_sensor_values)
    current_tf_np = np.array(current_tf).reshape((4, 4))

    # Define trajectory points using numpy transformations
    offsets = [
        [0.0, -0.05, 0.0],   # point 1: y -0.05
        [0.0, 0.0, 0.04],     # point 2: z +0.04
        [0.0, 0.04, 0.0],     # point 3: y +0.04
        [0.0, 0.0, -0.02],    # point 4: z -0.02
        [0.0, -0.05, 0.0],    # point 5: y -0.05
        [0.0, 0.0, 0.0]       # point 6: return to original
    ]

    for offset in offsets:
        new_tf = current_tf_np.copy()
        new_tf[:3, 3] += offset  # Apply position offset
        path.append(new_tf.flatten().tolist())

    times = [0.5, 1.0, 2.0, 3.0, 4.0, 4.5]  # seconds

    # Execute trajectory
    motion_proxy.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()