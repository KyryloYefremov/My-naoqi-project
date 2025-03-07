import cv2
import mediapipe as mp
from computer_vision import HandDetector


hand_detector = HandDetector()
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        exit(1)

    img = hand_detector.find_hands(img)
    land_mark_list = hand_detector.find_position(img, draw=False)
    # print(land_mark_list)
    fingers_up = hand_detector.fingers_up()
    # print(fingers_up)

    if fingers_up is not None:
        max_fingers_up_count = sum(fingers_up)



        cv2.putText(img, f"Fingers up: {max_fingers_up_count}", (100, 100),  cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    