# -*- encoding: UTF-8 -*-
""" 
Periodically checks for faces and greets when detected.
This example shows that ALModule is no needed and can be replaced by ALProxy and subscribing to events.
"""

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

import time
from naoqi import ALProxy
from config import *


def main():
    # create proxies with hardcoded values
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    memory = ALProxy("ALMemory", IP, PORT)
    face_detection = ALProxy("ALFaceDetection", IP, PORT)
    
    # enable face detection
    face_detection.subscribe("FaceGreeter", 500, 0.1)  # Name, period, precision

    try:
        last_detection_time = 0
        while True:
            # check for faces via memory
            faces = memory.getData("FaceDetected")
            
            if faces and isinstance(faces, list) and len(faces) >= 2:
                # only greet once per new detection
                if time.time() - last_detection_time > 5:  # 5-second cooldown
                    tts.say("Ahoj")
                    last_detection_time = time.time()
            
            time.sleep(0.5)  # polling interval

    except KeyboardInterrupt:
        print("\nShutting down...")
        face_detection.unsubscribe("FaceGreeter")

if __name__ == "__main__":
    main()