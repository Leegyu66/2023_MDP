import cv2
import mediapipe as mp
import time
from pose_media import mediapipe_pose
import csv
import numpy as np
from coordinate import Coor

# mediapipe 불러오기
mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils
media = mediapipe_pose()
coor = Coor()

csv_path = "datasets\coords_dataset.csv"

start_time = time.time()

frame_counter = 0

use_coord = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
# pose 랜드마크를 찍어주는 함수
def pose_landmark(img, label):
    global frame_counter
    frame_counter += 1
    img_height, img_width, _ = img.shape
    img = cv2.resize(img, (int(img_width * (400 / img_height)), 400))
    # 홀리스틱으로 landmark 찾아주는 함수
    image, results = media.drawing_holistic(img, holistic)


    coor.record_coordinates(results, csv_path, label, use_coord)

    # landmark draw 해주는 함수
    media.draw_styled_landmarks(image, results)

    # fps counter
    cTime = time.time()
    fps = frame_counter / (time.time() - start_time)
    pTime = cTime
    cv2.putText(image,"FPS:" +str(int(fps)),(10,100), cv2.FONT_HERSHEY_PLAIN, 2,(255,0,190),2,cv2.LINE_AA)
    return image

mp4_list = ['happy.mp4', 'hello.mp4']

# Holistic 오픈
coor.save_csv(csv_path, use_coord)
for i in range(2):
    cap = cv2.VideoCapture(mp4_list[i])
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while True:
                ret, img = cap.read()
                if not ret:
                    break 
                image = pose_landmark(img, mp4_list[i].split('.')[0])
                print(mp4_list[i].split('.')[0])

                cv2.imshow('Video', image)

                if cv2.waitKey(1) == ord('q'):
                    break

# print(coor)

cap.release()