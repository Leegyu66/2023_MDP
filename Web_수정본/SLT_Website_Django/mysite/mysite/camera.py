from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

import cv2
import mediapipe as mp
import time
from mysite.pose_media import mediapipe_pose
import csv
import numpy as np
from mysite.coordinate import Coor
import os
from keras.models import load_model
from keras import Sequential
from mysite.train_dataset import pose_landmark_dataset
import random
import io
import PIL.Image as Image

# mediapipe 불러오기
mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils
media = mediapipe_pose()
coor = Coor()

model_path = os.path.join('mysite', 'models2', 'model.h5')

seq = []
action_seq = []
seq_length = 30
action = "?"

actions = np.array(['stand', 'hello', 'happy', 'iloveyou'])
model = load_model(model_path, compile=False)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
          
    def __del__(self):
        self.video.release()
    
    def get_frame(self, holistic):
        grabbed, frame = self.video.read()
        image, data = pose_landmark_dataset(frame, actions, holistic=holistic)
        return image, data
            

def gen(camera):

    global seq, action_seq, seq_length, action, actions
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            image, data = camera.get_frame(holistic)
            

            # _, jpeg = cv2.imencode('.jpg', image)
            # jpeg = jpeg.tobytes()

            # yield(b'--frame\r\n'b'Content-type:image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n') 

            stop_start_state = "Stop"
            
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
                    image, data = camera.get_frame(holistic)

                    pre_list.append(data)

                    stop_start_state = "Start"
                    cv2.putText(image, stop_start_state, org=(30, 65), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)

                    _, jpeg = cv2.imencode('.jpg', image)
                    jpeg = jpeg.tobytes()
                    yield(b'--frame\r\n'b'Content-type:image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')
                    cv2.waitKey(1)

                input_data = np.expand_dims(np.array(pre_list), axis=0)
                y_pred = model.predict(input_data)
                y_pred = y_pred.squeeze(0)  
                i_pred = int(np.argmax(y_pred))
                action = actions[i_pred]
                cv2.waitKey(1500)
                
            

            cv2.putText(image, f'{action.upper()}', org=(30, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)  
            
            # if conf < 0.8:
            #     continue
                
            stop_start_state = "Stop"
            cv2.putText(image, stop_start_state, org=(30, 65), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)
            
            
            _, jpeg = cv2.imencode('.jpg', image)
            jpeg = jpeg.tobytes()
            yield(b'--frame\r\n'b'Content-type:image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

                     
    