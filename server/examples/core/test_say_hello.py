# -*- coding: utf-8 -*-
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy
import time

start = time.time()

tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.setLanguage("Czech")
tts.say("Ahoj kamaráde, jsem Nao. Umím všechna česká písmena.")
tts.setLanguage("English")
tts.say("Hello, I am Nao. I can speak English as well.")
tts.setLanguage("Czech")

end = time.time()
print("Execution time: {:.3f} sec".format(end - start))
