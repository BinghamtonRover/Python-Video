import cv2
import time

import sys

def showCamera(i):
    cam = cv2.VideoCapture(i)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
    while True:
        time.sleep(1/10)
        print(f"Displaying camera {i}")
        success, frame = cam.read()
        if not success:
            print(f"Camera {i} stopped responding!")
        else: cv2.imshow(f"Camera: {i}", frame)
        if cv2.waitKey(1) == ord('q'):
            cam.release()
            break

showCamera(sys.argv[1])
print("Closing")
