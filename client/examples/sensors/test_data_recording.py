# -*- encoding: UTF-8 -*-
""" Record sensor values and write them to a file (Python 3 version) """

import os
import sys
# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
from config import *

import time
from naoqi3 import ALProxy

# List of ALMemory values to record
ALMEMORY_KEY_NAMES = [
    "Device/SubDeviceList/HeadYaw/Position/Sensor/Value",
    "Device/SubDeviceList/HeadYaw/Position/Actuator/Value"
]

def record_data():
    """Record data from ALMemory and return as a matrix of values"""
    print("Recording data...")
    memory = ALProxy("ALMemory", IP, PORT)
    data = []
    for _ in range(1, 100):
        line = []
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(0.05)
    return data

def main():
    """Main recording routine with head movement"""
    motion = ALProxy("ALMotion", IP, PORT)
    
    # Set head stiffness and move
    motion.setStiffnesses("Head", 1.0)
    motion.post.angleInterpolation(
        ["HeadYaw"],        # Joint name
        [1.0, 0.0],        # Target angles (radians)
        [1.0, 2.0],        # Time intervals (seconds)
        False               # Absolute movement
    )
    
    # Record sensor data during movement
    sensor_data = record_data()
    
    # Release head motors
    motion.setStiffnesses("Head", 0.0)

    # Save to CSV
    output = os.path.join(os.getcwd(), "examples/logging-data/data_recording.csv")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    with open(output, "w", encoding='utf-8') as f:
        for line in sensor_data:
            f.write("; ".join(str(x) for x in line) + "\n")

    print(f"Results written to {output}")

if __name__ == "__main__":
    main()