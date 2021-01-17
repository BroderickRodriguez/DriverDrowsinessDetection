from imutils.video import FileVideoStream
from imutils import face_utils
import cv2
import numpy as np
import argparse
import imutils
import time
import dlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import csv
import datetime

def euclidean_dist(ptA, ptB):
    # compute and return the euclidean distance between the two
    # points
    return np.linalg.norm(ptA - ptB)

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = euclidean_dist(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

#parsing arguments needed for the program
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help = "path to where the video source resides")
ap.add_argument("-c", "--cascade", required=True,
   help = "path to where the face cascade resides")
ap.add_argument("-p", "--shape-predictor", required=True,
    help="path to facial landmark predictor")
args = vars(ap.parse_args())

#loading haar cascade for face detection then loading shape predictor
#for facial landmarks
print("[INFO] loading facial landmark predictor ...")
detector = cv2.CascadeClassifier(args["cascade"])
predictor = dlib.shape_predictor(args["shape_predictor"])
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


#Variable/Constants
#############################################
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 16

EAR_COUNTER = 0


PERCLOS_INT = 2700  #PERCLOS time intervak
PERCLOS = 0         #PERCLOS value
PERCLOS_COUNTER = 0 #Counts the frames where ear is below threshold within PERCLOS_INT
PERCLOS_TF = 0      #Counts total frames

NOFACE_COUNTER = 0  
NOFACE_THRESH = 28

fr = 0
start_time = time.time()
ear = 0

#read video source from parsed location
#and start stream in a different thread
cap = FileVideoStream(args["video"]).start()
time.sleep(1.0)




############################################
while cap.more():
    #read every frame of the video
    #resize

    frame = cap.read()
    frame = imutils.resize(frame, width=360)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector.detectMultiScale(gray, 1.3, 5)
    
    if len(rects) == 0:
        NOFACE_COUNTER += 1
        if NOFACE_COUNTER >= NOFACE_THRESH:
            print("[WARNING] NO FACE DETECTED")
            
    else:
        NOFACE_COUNTER = 0
        
    for (x, y, w, h) in rects:
        #frame = cv2.rectangle(frame, (x,y), (x+w,y+h),(255,0,0),5)
        rect = dlib.rectangle(int(x), int(y), int(x + w),
            int(y + h))
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        cv2.putText(frame, "EAR: {:.3f}".format(ear), (95,30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if PERCLOS_TF >= PERCLOS_INT:
            PERCLOS = (PERCLOS_COUNTER / PERCLOS_TF) * 100
            PERCLOS_TF = 0
            PERCLOS_COUNTER = 0

        if ear <= EYE_AR_THRESH:
            EAR_COUNTER += 1
            PERCLOS_COUNTER += 1
            # if the eyes were closed for a sufficient number of
            # frames, then sound the alarm
            if EAR_COUNTER >= EYE_AR_CONSEC_FRAMES:
                # draw an alarm on the frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            COUNTER = 0
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (255,0,0), 2)
    fr = fr + 1
    PERCLOS_TF += 1
    print (PERCLOS_TF)
    #exportValue(ear)
    # cv2.putText(frame, "fps {:.3f}".format(fr/(time.time()-start_time)), (0,60),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "PERCLOS = {:.2f}".format(PERCLOS), (100,100),
             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.stop()
cv2.destroyAllWindows()
