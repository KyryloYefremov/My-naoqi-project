from naoqi import ALProxy

IP = '192.168.0.122'
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Ahoj, jsem Nao.")

# motionProxy = ALProxy("ALMotion", IP, 9559)
# motionProxy.rest()