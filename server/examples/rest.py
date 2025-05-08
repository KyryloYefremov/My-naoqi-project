import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from naoqi import ALProxy
from config import *


motionProxy = ALProxy("ALMotion", IP, PORT)
motionProxy.rest()