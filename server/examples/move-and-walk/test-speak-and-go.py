import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy


motion = ALProxy("ALMotion", IP, PORT)
tts    = ALProxy("ALTextToSpeech", IP, PORT)

motion.wakeUp()
motion.moveInit()
motion.post.moveTo(0.5, 0, 0)
tts.say("Ja jdu nekam, hodne, hodne daleko. A nikdo me nenajde.")

motion.rest()