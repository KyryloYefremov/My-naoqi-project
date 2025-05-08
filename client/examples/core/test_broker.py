# -*- encoding: UTF-8 -*-
""" 
Say 'hello, you' each time a human face is detected
"""

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

import time

from naoqi3 import ALProxy
from naoqi3 import ALBroker

from config import *




def main():
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       IP,         # parent broker IP
       PORT)       # parent broker port

    try:
        tts = ALProxy("ALTextToSpeech")
        while True:
            time.sleep(5)
            tts.say("5 sekund uplinulo")

    except KeyboardInterrupt:
        print()
        print("Interrupted by user")
    except Exception as e:
        print(e)
    finally:
        print("shutting down")
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()



