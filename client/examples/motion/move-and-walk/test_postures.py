# python 3
### test:
### Execution time: 154.3668 seconds

import os
import sys
import time

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi3 import ALProxy

# measure the execution time
start_time = time.time()


sleep_time = 3  # sec
speed = 0.5

try:
    motionProxy  = ALProxy("ALMotion", IP, PORT)
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
    
    motionProxy.wakeUp()

    print(postureProxy.getPostureList())

    postures = [
        "StandInit",
        "SitRelax",
        "StandZero",
        "LyingBelly",
        "LyingBack",
        "Crouch",
    ]

    for posture in postures:
        postureProxy.goToPosture(posture, speed)
        time.sleep(sleep_time)

    
except Exception as e:
    print("Could not create proxy to ALRobotPosture")
    print("Error was: ", e)
finally:
    # Go to rest position
    motionProxy.rest()

    # count end time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")






