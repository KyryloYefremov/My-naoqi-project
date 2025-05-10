# -*- encoding: UTF-8 -*- 
# This test demonstrates how to use the ALFaceDetection module.
# Note that you might not have this module depending on your distribution
#
# - We first instantiate a proxy to the ALFaceDetection module
#     Note that this module should be loaded on the robot's naoqi.
#     The module output its results in ALMemory in a variable
#     called "FaceDetected"

# - We then read this ALMemory value and check whether we get
#   interesting things.
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *
import time

from naoqi import ALProxy


# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:  # type: ignore
  print "Error when creating face detection proxy:"  # type: ignore
  print str(e) # type: ignore
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFacedetection modules
# outputs its results
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e: # type: ignore
  print "Error when creating memory proxy:" # type: ignore
  print str(e) # type: ignore
  exit(1)


# A simple loop that reads the memValue and checks whether faces are detected.
for i in range(0, 20):
  time.sleep(0.5)
  val = memoryProxy.getData(memValue)

  print ""  # type: ignore
  print "*****"  # type: ignore
  print ""  # type: ignore

  # Check whether we got a valid output.
  if(val and isinstance(val, list) and len(val) >= 2):

    # We detected faces !
    # For each face, we can read its shape info and ID.

    # First Field = TimeStamp.
    timeStamp = val[0]

    # Second Field = array of face_Info's.
    faceInfoArray = val[1]

    try:
      # Browse the faceInfoArray to get info on each detected face.
      for j in range( len(faceInfoArray)-1 ):
        faceInfo = faceInfoArray[j]

        # First Field = Shape info.
        faceShapeInfo = faceInfo[0]

        # Second Field = Extra info (empty for now).
        faceExtraInfo = faceInfo[1]

        print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])  # type: ignore
        print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])  # type: ignore

    except Exception, e:  # type: ignore
      print "faces detected, but it seems getData is invalid. ALValue ="  # type: ignore
      print val  # type: ignore
      print "Error msg %s" % (str(e))  # type: ignore
  else:
    print "No face detected"  # type: ignore

# Unsubscribe the module.
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."  # type: ignore