import cv2

cap = cv2.VideoCapture("기쁘다.mp4")

while True:
    ret, img = cap.read()

    if not ret:
        break

    cv2.imshow('video', img)

    if cv2.waitKey(20) == ord('q'):
        break