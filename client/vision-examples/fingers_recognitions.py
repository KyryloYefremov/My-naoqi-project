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
# import mediapipe as mp
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
    """
    Detekuje ruku a spočítá zvednuté prsty pomocí konvexních defektů.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (35, 35), 0)
    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0

    max_contour = max(contours, key=cv2.contourArea)
    hull = cv2.convexHull(max_contour, returnPoints=False)

    if len(hull) < 4:
        return 0

    defects = cv2.convexityDefects(max_contour, hull)
    if defects is None:
        return 0

    finger_count = 0
    for i in range(defects.shape[0]):
        _, _, far_idx, depth = defects[i, 0]
        if depth > 10000:  # Filtruje jen významné defekty (velikost ruky)
            finger_count += 1

    return min(finger_count, 5)  # Omezíme max počet prstů na 5

# def count_fingers(image):
#     result = mp_hands.Hands().process(image)
#     return result


if __name__ == "__main__":
    image_folder = "vision-examples\images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # mp_hands = mp.solutions.hands
    # mp_drawing = mp.solutions.drawing_utlis

    cam_proxy = ALProxy("ALVideoDevice", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)

    i = 1
    while True:
        frame = get_image(cam_proxy)
        if frame is None:
            print("Nepodařilo se získat snímek.")
            continue
    
        fingers = count_fingers(frame)

        # save img 
        image_path = os.path.join(image_folder, str(i).zfill(3) + "image_" + str(fingers) + "fingers" + ".png")
        cv2.imwrite(image_path, frame)
        print("Saved: ", image_path)

        # TODO: try to implement this
        # results = count_fingers(frame)
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         mp_drawing.draw_landmarks(frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)

        # Řekne rozpoznaný počet prstů
        tts.say("Vidim {} prstu.".format(fingers))

        time.sleep(2)  # Počkej, než se další snímek zpracuje
        i+=1
