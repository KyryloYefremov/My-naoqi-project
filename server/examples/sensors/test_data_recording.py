# -*- encoding: UTF-8 -*-
""" Record some sensors values and write them into a file.

"""

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *

# MEMORY_VALUE_NAMES is the list of ALMemory values names you want to save.
ALMEMORY_KEY_NAMES = [
"Device/SubDeviceList/HeadYaw/Position/Sensor/Value",
"Device/SubDeviceList/HeadYaw/Position/Actuator/Value",
]


import os
import sys
import time

from naoqi import ALProxy

def recordData():
    """ Record the data from ALMemory.
    Returns a matrix of values

    """
    print "Recording data ..."  # type: ignore
    memory = ALProxy("ALMemory", IP, PORT)
    data = list()
    for i in range (1, 100):
        line = list()
        for key in ALMEMORY_KEY_NAMES:
            value = memory.getData(key)
            line.append(value)
        data.append(line)
        time.sleep(0.05)
    return data


def main():
    """ Parse command line arguments,
    run recordData and write the results
    into a csv file

    """

    motion = ALProxy("ALMotion", IP, PORT)
    # Set stiffness on for Head motors
    motion.setStiffnesses("Head", 1.0)
    # Will go to 1.0 then 0 radian
    # in two seconds
    motion.post.angleInterpolation(
        ["HeadYaw"],
        [1.0, 0.0],
        [1  , 2],
        False
    )
    data = recordData()
    # Gently set stiff off for Head motors
    motion.setStiffnesses("Head", 0.0)

    output = os.getcwd() + "/examples/logging-data/data_recording.csv"

    with open(output, "w") as fp:
        for line in data:
            fp.write("; ".join(str(x) for x in line))
            fp.write("\n")

    print "Results written to", output  # type: ignore


if __name__ == "__main__":
    main()