# python 3
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