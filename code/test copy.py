import cv2
import mediapipe as mp
import time
from pose_media import mediapipe_pose
import csv
import numpy as np
from coordinate import Coor
import os
from keras.models import load_model
from keras import Sequential
from train_dataset import pose_landmark_dataset
import random

# mediapipe 불러오기
mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils
media = mediapipe_pose()
coor = Coor()

cap = cv2.VideoCapture(0)

model_path = os.path.join('models2', 'model.h5')


seq = []
action_seq = []
seq_length = 30
action = "?"

actions = np.array(['stand', 'hello', 'happy', 'iloveyou'])
model = load_model(model_path, compile=False)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        img_height, img_width, _ = frame.shape

        stop_start_state = "Stop"

        img = cv2.resize(frame, (int(img_width * (400 / img_height)), 400))

        image, data = pose_landmark_dataset(frame, actions, holistic=holistic)
        
        try:
            if data == None:
                continue
        except:
            pass
        
        seq.append(data)
        
        if len(seq) < seq_length:
            continue
        
        if (data[61] < data[53] or data[65] < data[57]) and (data[55] > 0 and data[59] > 0) :
            
            pre_list = []
            for i in range(30):
                ret, frame = cap.read()
                image, data = pose_landmark_dataset(frame, actions, holistic=holistic)
                pre_list.append(data)

                stop_start_state = "Start"
                cv2.putText(image, stop_start_state, org=(30, 65), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)

                cv2.imshow('OpenCV', image)
                cv2.waitKey(10)

            input_data = np.expand_dims(np.array(pre_list), axis=0)
            y_pred = model.predict(input_data)
            y_pred = y_pred.squeeze(0)  
            i_pred = int(np.argmax(y_pred))
            action = actions[i_pred]
            cv2.waitKey(2000)
            
        

        cv2.putText(image, f'{action.upper()}', org=(30, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)  
        
        # if conf < 0.8:
        #     continue
            
        stop_start_state = "Stop"
        cv2.putText(image, stop_start_state, org=(30, 65), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)
        
        
        cv2.imshow('OpenCV', image)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()