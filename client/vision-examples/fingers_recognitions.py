import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)
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
    Pošle požadavek na získání snímku z kamery NAO a vrátí jej jako OpenCV obrázek.
    """
    resolution = vision_definitions.kQVGA  # 320x240
    color_space = vision_definitions.kBGRColorSpace  # OpenCV používá BGR

    nameId = cam_proxy.subscribe("python_GVM", resolution, color_space, 30)
    image = cam_proxy.getImageRemote(nameId)
    cam_proxy.unsubscribe(nameId)

    if image is None:
        return None

    width = image[0]
    height = image[1]
    array = np.frombuffer(bytes(image[6], encoding='latin1'), dtype=np.uint8).reshape((height, width, 3))
    return array

def count_fingers(image):
    processed_img = hand_detector.find_hands(image)
    land_mark_list = hand_detector.find_position(processed_img, draw=False)
    fingers_up = hand_detector.fingers_up()

    if fingers_up is not None:
        fingers_up_count = sum(fingers_up)
    else:
        fingers_up_count = 0

    return fingers_up_count, processed_img


if __name__ == "__main__":
    image_folder = "vision-examples\images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # init
    cam_proxy = ALProxy("ALVideoDevice", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    hand_detector = HandDetector()

    # get images from robot camera and count fingers
    i = 1
    while True:
        frame = get_image(cam_proxy)
        if frame is None:
            print("Nepodařilo se získat snímek.")
            continue
    
        fingers, landmark_img = count_fingers(frame)

        # save img 
        image_path = os.path.join(image_folder, str(i).zfill(3) + "image_" + str(fingers) + "fingers" + ".png")
        cv2.imwrite(image_path, landmark_img)
        print("Saved: ", image_path)

        # say fingers number
        tts.say("Vidim {} prstu.".format(fingers))

        time.sleep(2)  # sleep for a while
        i+=1
