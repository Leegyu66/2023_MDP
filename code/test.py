import cv2
import mediapipe as mp
import time
from pose_media import mediapipe_pose
import csv
import numpy as np
from coordinate import Coor
import os
from keras.models import load_model
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

actions = np.array(['stand', 'hello', 'happy', 'iloveyou'])
model = load_model(model_path)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        img_height, img_width, _ = frame.shape
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
        
        input_data = np.expand_dims(np.array(seq[-30:]), axis=0)
        y_pred = model.predict(input_data)
        y_pred = y_pred.squeeze(0)
        i_pred = int(np.argmax(y_pred))

        conf = y_pred[i_pred]        
        
        # if conf < 0.8:
        #     continue
            
        action = actions[i_pred]
        action_seq.append(action)

        if len(action_seq) < 3:
                continue

        this_action = '?'
        if action_seq[-1] == action_seq[-2] == action_seq[-3]:
            this_action = action
        
        if conf > 0.9:
            print(conf)
            cv2.putText(image, f'{this_action.upper()}', org=(random.randint(50, 300), random.randint(50, 400)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)


        cv2.imshow('OpenCV', image)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()