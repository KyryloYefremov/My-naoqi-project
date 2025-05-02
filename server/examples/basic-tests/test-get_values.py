# python 2
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy
import time

motionProxy = ALProxy("ALMotion", IP, PORT)

motionProxy.wakeUp()

# print motion state
print(f"Motion state: {motionProxy.getSummary()}")
time.sleep(4.0)

# Go to rest position
motionProxy.rest()