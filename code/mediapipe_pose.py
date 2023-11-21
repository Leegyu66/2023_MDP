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

csv_path = "datasets\coords_dataset_test.csv"

start_time = time.time()

frame_counter = 0

data = []

use_coord = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
# pose 랜드마크를 찍어주는 함수
def pose_landmark(img, label):
    global frame_counter
    frame_counter += 1
    img_height, img_width, _ = img.shape
    img = cv2.resize(img, (int(img_width * (400 / img_height)), 400))
    # 홀리스틱으로 landmark 찾아주는 함수
    image, results = media.drawing_holistic(img, holistic)


    data.append(coor.record_coordinates(results, csv_path, label, use_coord))
    
    # landmark draw 해주는 함수
    media.draw_styled_landmarks(image, results)

    # fps counter
    cTime = time.time()
    fps = frame_counter / (time.time() - start_time)

    # cv2.putText(image,"FPS:" +str(int(fps)),(10,100), cv2.FONT_HERSHEY_PLAIN, 2,(255,0,190),2,cv2.LINE_AA)
    return image

label = ['hello', 'happy']

# Holistic 오픈
coor.save_csv(csv_path, use_coord)
for i in range(2):
    e_time = 0
    count = 0
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            s_time = time.time()
            while True:
                e_time = time.time()
                if int(e_time - s_time) > 4 or count == 60:
                    break
                ret, img = cap.read()
                image = pose_landmark(img, label[i])
                
                count += 1
                cv2.imshow('Video', image)

                if not ret:
                    break
                if cv2.waitKey(1) == ord('q'):
                    break
    print(count)
data = np.array(data)
print(data.shape)
print(data)
# print(coor)

cap.release()