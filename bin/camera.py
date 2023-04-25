import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    _, frame = cap.read()
    # Display the resulting frame
    cv.imshow('frame', frame)
    # MUST call waitKey, even if you don't use it
    if cv.waitKey(1) == ord('q'): break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
