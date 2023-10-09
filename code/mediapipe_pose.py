import cv2
import mediapipe as mp
import time
from pose_media import mediapipe_pose

# mediapipe 불러오기
mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils
media = mediapipe_pose()

cap = cv2.VideoCapture(0)

start_time = time.time()

frame_counter = 0

# Holistic 오픈
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
            ret, img = cap.read()
            frame_counter += 1

            # 홀리스틱으로 landmark 찾아주는 함수
            image, results = media.drawing_holistic(img, holistic)

            # landmark draw 해주는 함수
            media.draw_styled_landmarks(image, results)

            # fps counter
            cTime = time.time()
            fps = frame_counter / (time.time() - start_time)
            pTime = cTime
            cv2.putText(image,"FPS:" +str(int(fps)),(10,100), cv2.FONT_HERSHEY_PLAIN, 2,(255,0,190),2,cv2.LINE_AA)

            cv2.imshow('Video', image)
            
            if cv2.waitKey(1) == ord('q'):
                    break

cap.release()
