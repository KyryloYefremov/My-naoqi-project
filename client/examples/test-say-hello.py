# main.py (Python 3)
from config import *
from naoqi3 import ALProxy

IP = '192.168.0.122'
tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.say("Ahoj, jsem Nao.")

# motionProxy = ALProxy("ALMotion", IP, PORT)
# motionProxy.rest()
