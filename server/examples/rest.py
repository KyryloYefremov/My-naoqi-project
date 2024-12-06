from naoqi import ALProxy

IP = '192.168.0.122'

motionProxy = ALProxy("ALMotion", IP, 9559)
motionProxy.rest()