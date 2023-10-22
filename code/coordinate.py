import cv2
import mediapipe as mp
import time
from pose_media import mediapipe_pose
import csv
import numpy as np

# mediapipe 불러오기
mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils
media = mediapipe_pose()

class Coor():
    def __init__(self):
        pass
    # csv에 X{}, Y{}, Z{}을 31까지 저장
    def save_csv(self, create_csv, use_coord):
        try:
            num_coords = len(use_coord) # num_coords: 33

            landmarks = ['class']
            for val in use_coord:
                landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val)]

            with open(create_csv, mode='w', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(landmarks)
        except:
            print("으익")


    # 좌표를 따서 저장해주는 함수
    def record_coordinates(self, results, csv_file, class_name, use_coord):
        count = 1
        repo = []
        # try:
        pose_row = []
        pose = results.pose_landmarks.landmark
        # pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
        for landmark in pose:
            if count in use_coord:
                pose_row.append(landmark.x)
                pose_row.append(landmark.y)
                pose_row.append(landmark.z)
            else:
                pass
            count += 1
            
        pose_row = np.array(pose_row)

        for i in pose_row:
            repo.append(round(i, 3))

        repo.insert(0, class_name)
            

        with open(csv_file, mode='a', newline='') as f:
            
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(repo)

        # except:
        #     print("으익")