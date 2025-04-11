# -*- encoding: UTF-8 -*-

import os
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

'''Cartesian control: Arm trajectory example'''
''' This example is only compatible with NAO '''

import motion
from naoqi3 import ALProxy
from config import *


def transform_to_vector(translation, rotation):
    """Convert translation and rotation to transform vector"""
    rot_matrix = R.from_euler('xyz', rotation).as_matrix()
    return [
        rot_matrix[0,0], rot_matrix[0,1], rot_matrix[0,2], translation[0],
        rot_matrix[1,0], rot_matrix[1,1], rot_matrix[1,2], translation[1],
        rot_matrix[2,0], rot_matrix[2,1], rot_matrix[2,2], translation[2],
        0.0, 0.0, 0.0, 1.0
    ]

def main():
    ''' Example showing a path of two positions
    Warning: Needs a PoseInit before executing
    '''

    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    effector   = "LArm"
    frame      = motion.FRAME_TORSO
    axisMask   = motion.AXIS_MASK_VEL # just control position
    useSensorValues = False

    path = []
    currentTf = motionProxy.getTransform(effector, frame, useSensorValues)
    
    # Convert current transform to numpy array
    currentTf_np = np.array(currentTf).reshape((4,4))
    
    # Create target transform by offsetting current position
    targetTf_np = currentTf_np.copy()
    targetTf_np[:3, 3] += np.array([0.03, 0.03, 0.0])  # x,y,z offsets
    
    # Convert back to vector format expected by NAOqi
    path.append(targetTf_np.flatten().tolist())
    path.append(currentTf)

    # Go to the target and back again
    times = [2.0, 4.0] # seconds

    motionProxy.transformInterpolations(effector, frame, path, axisMask, times)

    # Go to rest position
    motionProxy.rest()

if __name__ == "__main__":
    main()