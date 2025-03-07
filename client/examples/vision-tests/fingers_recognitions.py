import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())
os.system('cls')

import sys
import time
import numpy as np
import cv2

from computer_vision import HandDetector
from naoqi3 import ALProxy

import vision_definitions
from config import *


def get_image(cam_proxy):
    """
    sends a request to get an image from the NAO camera
    """
    image = cam_proxy.getImageRemote(name_id)

    if image is None:
        return None

    width = image[0]
    height = image[1]
    channels = image[2]
    array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, channels))
    return array.copy()


def count_fingers(image):
    image = hand_detector.find_hands(image)
    land_mark_list = hand_detector.find_position(image, draw=False)
    fingers_up = hand_detector.fingers_up()

    if fingers_up is not None:
        fingers_up_count = sum(fingers_up)
    else:
        fingers_up_count = None

    return fingers_up_count


if __name__ == "__main__":
    image_folder = "vision-examples\images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # init
    cam_proxy = ALProxy("ALVideoDevice", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    hand_detector = HandDetector()
    # define params for nao camera
    resolution = vision_definitions.kQVGA  # 320x240
    color_space = vision_definitions.kBGRColorSpace  # OpenCV používá BGR
    # get string handle under which the module is known from ALVideoDevice
    name_id: str = cam_proxy.subscribe("python_GVM", resolution, color_space, 30)

    try:
        # get images from robot camera and count fingers
        while True:
            frame = get_image(cam_proxy)
            if frame is None:
                print("Nepodařilo se získat snímek.")
                continue
        
            fingers = count_fingers(frame)
            cv2.putText(frame, f"Fingers up: {str(fingers)}", (50, 50),  cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 2)
            cv2.imshow('image', frame)
            # wait for 'q' to quit
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    except Exception as e:
        print(e)
    finally:
        # unsubscribe from module
        cam_proxy.unsubscribe(name_id)