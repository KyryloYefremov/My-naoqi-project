# -*- coding: utf-8 -*-
from naoqi import ALProxy

IP = '192.168.0.101'
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Ahoj, jsem Nao.")
