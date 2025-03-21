import os
import sys
# Locate the config file dynamically
sys.path.insert(0, os.getcwd())


import numpy as np  # type: ignore
from scipy.spatial.transform import Rotation as R  # type: ignore
from naoqi3 import ALProxy
from config import *

def create_transform_matrix(translation, rotation):
    """
    Create a 4x4 transformation matrix from translation and rotation.
    :param translation: [x, y, z] translation vector.
    :param rotation: Rotation matrix (3x3) or quaternion.
    :return: 4x4 transformation matrix.
    """
    transform = np.eye(4)  # Create a 4x4 identity matrix
    transform[:3, :3] = rotation  # Set the rotation part
    transform[:3, 3] = translation  # Set the translation part
    return transform

def main():
    # Initialize proxies
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Wake up robot
    motion_proxy.wakeUp()

    # Send robot to Stand Init
    posture_proxy.goToPosture("StandInit", 0.5)

    # Define effector and frame
    effector = "LArm"
    frame = motion_proxy.FRAME_TORSO
    axis_mask = 7  # AXIS_MASK_VEL (control position only)
    use_sensor_values = False

    # Get the current transform of the effector
    current_tf = motion_proxy.getTransform(effector, frame, use_sensor_values)
    print("Current Transform (as list):", current_tf)

    # Convert the current transform to a 4x4 matrix
    current_matrix = np.array(current_tf).reshape(4, 4)

    # Create a target transform by modifying the current transform
    target_matrix = np.copy(current_matrix)
    target_matrix[0, 3] += 0.03  # Translate in X
    target_matrix[1, 3] += 0.03  # Translate in Y

    # Prepare the path (list of transforms)
    path = [
        list(target_matrix.flatten()),  # Target transform
        list(current_matrix.flatten())  # Current transform
    ]

    # Define the time for each transform in the path
    times = [2.0, 4.0]  # Seconds

    # Execute the trajectory
    motion_proxy.transformInterpolations(effector, frame, path, axis_mask, times)

    # Go to rest position
    motion_proxy.rest()

if __name__ == "__main__":
    main()