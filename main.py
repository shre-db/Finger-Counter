import cv2 as cv
import time
import os
import HT_module as htm

W_CAM, H_CAM = 640, 480

cap = cv.VideoCapture(0)
cap.set(3, W_CAM)
cap.set(4, H_CAM)

p_time = 0

detector = htm.HandDetector(detection_conf=0.75)
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lm_list = detector.findPosition(img, draw=False)
    # print(lm_list)

    if len(lm_list) != 0:
        fingers = []
        # Thumb
        if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for idx in range(1, 5):
            if lm_list[tip_ids[idx]][2] < lm_list[tip_ids[idx]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        total_fingers = fingers.count(1)
        print(total_fingers)

        cv.putText(img, f'Number: {total_fingers}', (50, 70), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv.putText(img, f'FPS: {int(fps)}', (400, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)
