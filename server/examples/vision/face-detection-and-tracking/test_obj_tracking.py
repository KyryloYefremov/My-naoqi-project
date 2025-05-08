# -*- encoding: UTF-8 -*-
# This python script assumes that you have correctly set your PYTHONPATH
# environment variable to "your_naoqi_sdk_path"/lib/.
#
# When tracking is activated, faces looking sideways, or located further away
# should be tracked for a longer period.
# Launch Monitor, Cameraviewer, activate face detection, and see if it works better.
#
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
from naoqi import ALProxy


USAGE = "USAGE:\n" \
        "python vision_setfacetracking.py [NAO_IP] [0 or 1] \n" \
        "\nExamples: \n" \
        "Enable tracking: set_tracking.py 192.168.1.102 1\n" \
        "Disable tracking: set_tracking.py 192.168.1.102 0"


def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
    """Make a proxy to nao's ALFaceDetection and enable/disable tracking.

    """
    faceProxy = ALProxy("ALFaceDetection", nao_ip, nao_port)

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled # type: ignore

    # Enable or disable tracking.
    faceProxy.enableTracking(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled() # type: ignore


def main():
    # Specify your IP address here.

    tracking_enabled = False
    set_nao_face_detection_tracking(IP, PORT, tracking_enabled)


if __name__ == "__main__":
    main()