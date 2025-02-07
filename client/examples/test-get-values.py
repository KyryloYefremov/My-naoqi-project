# python 3
import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)

from config import *
from naoqi3 import ALProxy
import time

motionProxy = ALProxy("ALMotion", IP, PORT)

motionProxy.wakeUp()

# print motion state
print(f"Motion state: {motionProxy.getSummary()}")
time.sleep(4.0)

# Go to rest position
motionProxy.rest()