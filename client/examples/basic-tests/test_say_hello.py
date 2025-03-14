# main.py (Python 3)
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi3 import ALProxy

tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.say("Ahoj, jsem Nao.")
tts.say("Ja jsem robot.")
tts.say("Ja pracuju, aby lidi mohli vic relaxovat.")

# motionProxy = ALProxy("ALMotion", IP, PORT)
# motionProxy.rest()
