# -*- encoding: UTF-8 -*-
""" 
Face Detection Test (Python 3 Version)
Demonstrates how to use the ALFaceDetection module.
Note: This module might not be available in all NAOqi distributions.
"""

import os
import sys
import time

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
from config import *
from naoqi3 import ALProxy  # Using Python 3 compatible proxy


def main():
    try:
        # Initialize face detection proxy
        face_proxy = ALProxy("ALFaceDetection", IP, PORT)
        print("Face detection proxy created successfully")
    except Exception as e:
        print(f"Error creating face detection proxy: {str(e)}")
        sys.exit(1)

    # Subscribe to face detection with 500ms period
    period = 500
    face_proxy.subscribe("Test_Face", period, 0.0)
    print("Subscribed to face detection service")

    # ALMemory variable for face detection results
    mem_value = "FaceDetected"

    try:
        # Initialize memory proxy
        memory_proxy = ALProxy("ALMemory", IP, PORT)
    except Exception as e:
        print(f"Error creating memory proxy: {str(e)}")
        face_proxy.unsubscribe("Test_Face")
        sys.exit(1)

    print("\nStarting face detection (20 iterations)...")
    for i in range(20):
        time.sleep(0.5)
        val = memory_proxy.getData(mem_value)

        print("\n*****")
        
        # Check for valid face data
        if val and isinstance(val, list) and len(val) >= 2:
            timestamp = val[0]
            face_info_array = val[1]

            try:
                # Process each detected face
                for face_info in face_info_array[:-1]:  # Skip last element if odd count
                    face_shape_info = face_info[0]
                    face_extra_info = face_info[1] if len(face_info) > 1 else None

                    # Print face position and size
                    print(f"  alpha {face_shape_info[1]:.3f} - beta {face_shape_info[2]:.3f}")
                    print(f"  width {face_shape_info[3]:.3f} - height {face_shape_info[4]:.3f}")

            except Exception as e:
                print(f"Error processing face data: {str(e)}")
                print(f"Raw data: {val}")
        else:
            print("No faces detected")

    # Cleanup
    face_proxy.unsubscribe("Test_Face")
    print("\nTest terminated successfully")

if __name__ == "__main__":
    main()