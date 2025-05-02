# -*- encoding: UTF-8 -*-

import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

# This is just an example script that shows how images can be accessed
# through ALVideoDevice in python.
# Nothing interesting is done with the images in this example.

import numpy as np
import cv2
from config import *
from naoqi import ALProxy
import vision_definitions
import time


# Vytvoření složky pro ukládání obrázků
image_folder = "examples\\vision-tests\images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

start = time.time()

print("Creating ALVideoDevice proxy to", IP)
camProxy = ALProxy("ALVideoDevice", IP, PORT)

# Registrace video modulu
resolution = vision_definitions.kQVGA  # 320x240
colorSpace = vision_definitions.kBGRColorSpace  # RGB formát
fps = 30

camProxy.unsubscribe("python_GVM_0")
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

end = time.time()
print("Execution time: {:.3f} seconds".format(end - start))