# python 2
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy
import time

start = time.time()

motionProxy = ALProxy("ALMotion", IP, PORT)

motionProxy.wakeUp()

# print motion state
print("Motion state: " + str(motionProxy.getSummary()))
time.sleep(4.0)

# Go to rest position
motionProxy.rest()

end = time.time()
print("Execution time: {:.3f} sec".format(end - start))