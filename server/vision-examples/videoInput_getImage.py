# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, config_dir)

# This is just an example script that shows how images can be accessed
# through ALVideoDevice in python.
# Nothing interesting is done with the images in this example.

import numpy as np
import cv2
from config import *
from naoqi import ALProxy
import vision_definitions

# Vytvoření složky pro ukládání obrázků
image_folder = "vision-examples\images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

print("Creating ALVideoDevice proxy to", IP)
camProxy = ALProxy("ALVideoDevice", IP, PORT)

# Registrace video modulu
resolution = vision_definitions.kQVGA  # 320x240
colorSpace = vision_definitions.kBGRColorSpace  # RGB formát
fps = 30

nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)
print("Subscribed with ID:", nameId)

print("Getting images and saving them")
for i in range(5):
    image = camProxy.getImageRemote(nameId)
    if image is None:
        print("Failed to get image", str(i))
        continue
    
    width = image[0]
    height = image[1]
    array = np.frombuffer(image[6], dtype=np.uint8).reshape((height, width, 3))
    
    image_path = os.path.join(image_folder, "image_" + str(i) + ".png")
    cv2.imwrite(image_path, array)
    print("Saved: ", image_path)

camProxy.unsubscribe(nameId)
print("End of script")
