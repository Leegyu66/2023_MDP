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

csv_path = "C:/Users/user/mdp/datasets/coords_dataset.csv"

cap = cv2.VideoCapture(0)

start_time = time.time()

frame_counter = 0

def pose_landmark(img):
    global frame_counter
    frame_counter += 1
    img_height, img_width, _ = img.shape
    img = cv2.resize(img, (int(img_width * (400 / img_height)), 400))
    # 홀리스틱으로 landmark 찾아주는 함수
    image, results = media.drawing_holistic(img, holistic)
    save_csv(results, csv_path)
    # coor = media.extract_keypoints(results)
    record_coordinates(results, csv_path, 1)

    # landmark draw 해주는 함수
    media.draw_styled_landmarks(image, results)

    # fps counter
    cTime = time.time()
    fps = frame_counter / (time.time() - start_time)
    pTime = cTime
    cv2.putText(image,"FPS:" +str(int(fps)),(10,100), cv2.FONT_HERSHEY_PLAIN, 2,(255,0,190),2,cv2.LINE_AA)
    return image

def save_csv(results, create_csv):
    try:
        num_coords = len(results.pose_landmarks.landmark) # num_coords: 33

        landmarks = ['class'] # Create first rows data.
        for val in range(1, num_coords+1):
            landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val)]
        
        # E.g., (pose+face)2005=1+501*4, (pose+r_hand)217=1+54*4, 133=1+33*4
        # print(f'len(landmarks): {len(landmarks)}')

        # Define first class rows in csv file.
        with open(create_csv, mode='w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(landmarks)
    except:
        pass
    
def record_coordinates(results, csv_file, class_name):
    repo = []
    try:
        # Extract Pose landmarks
        pose = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

        # Extract Face landmarks
        # face = results.face_landmarks.landmark
        # face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
        
        # Concate rows
        # row = pose_row+face_row
        row = pose_row

        # Append class name.
        for i in pose_row:
            repo.append(round(i, 3))
        repo.insert(0, class_name)
            

        # Export to CSV
        with open(csv_file, mode='a', newline='') as f:
            
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(repo) 

    except:
        print("으익")

# Holistic 오픈
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        img = cv2.imread("test.jpg")

        image = pose_landmark(img)

        cv2.imshow('Video', image)

        if cv2.waitKey(1) == ord('q'):
            break

# print(coor)

cap.release()