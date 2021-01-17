from imutils.video import FileVideoStream
from imutils import face_utils
import cv2
import numpy as np
import argparse
import imutils
import time
import dlib
import csv
import datetime
import Constants as cn


def euclidean_dist(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

def eye_aspect_ratio(eye):
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])
    C = euclidean_dist(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def sendValue(value)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help = "path to where the video source resides")
args = vars(ap.parse_args())


#filename = 'data{}.csv'.format(datetime.datetime.now().strftime("%m%d%y%H%M%S"))
#with open(filename, 'w') as csv_file:
#    csv_writer = csv.DictWriter(csv_file, fieldnames=["Frame", 
#    "Ear Value", "PERCLOS"])
#    csv_writer.writeheader()

def exportValue():
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=["Frame", 
        "Ear Value", "PERCLOS"])
        info = {"Frame": frame_count,
                "Ear Value": "{:.3f}".format(ear),
                "PERCLOS": "{:.2f}".format(PERCLOS)}
        csv_writer.writerow(info)
    return

#Moving computation of PERCLOS

def computePerclos(i, N):
    return ((ABN_CUMSUM[i]-ABN_CUMSUM[i-N])/N)*100

print("[INFO] loading face detector ...")
detector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

print("[INFO] loading facial landmark predictor ...")
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


print("[INFO] starting video stream")
cap = FileVideoStream(args["video"]).start()
time.sleep(1.0)

############################################
# All variables/constants needed
PERCLOS = 0
ABN_BLINK = 0
ear = 0
COUNTER = 0
NOFACE_COUNTER = 0
ABN_CUMSUM = list()
EAR_LIST = list()
PERCLOS_LIST = list()
frame_count = 0


while cap.more():
   
    frame = cap.read()
    frame = imutils.resize(frame, width=360)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector.detectMultiScale(gray, 1.3, 5)

    if len(rects) == 0:
        
        NOFACE_COUNTER += 1
        
        if NOFACE_COUNTER >= cn.NOFACE_THRESH:
            print("[WARNING] NO FACE DETECTED")
            sendValue(3)
            
        ABN_CUMSUM.append(ABN_BLINK)
        ear = 0
        EAR_LIST.append(ear)
        
    else:
        
        NOFACE_COUNTER = 0
        
        for (x, y, w, h) in rects:
            rect = dlib.rectangle(int(x), int(y), int(x + w),
            int(y + h))
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0
            
            EAR_LIST.append(ear)
            
            #---------OPTIONAL------------------------------------------
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                    
            cv2.putText(frame, "EAR: {:.3f}".format(ear), (95,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #-----------------------------------------------------------

        if ear <= cn.EYE_AR_THRESH:
            COUNTER += 1
            
            if COUNTER >= cn.BLINK_THRESH:
                ABN_BLINK += 1
                ABN_CUMSUM.append(ABN_BLINK)
                
                if COUNTER >= cn.EYE_AR_CONSEC_FRAMES:
                    # draw an alarm on the frame
                    #cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                    #    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    sendValue(2)
            else:
                ABN_CUMSUM.append(ABN_BLINK)            
        else:
            COUNTER = 0
            ABN_CUMSUM.append(ABN_BLINK)
        
        if frame_count == 840:
            print('Average EAR for 1 minutes:{:.2f}'.format(sum(EAR_LIST)/840))
        
        PERCLOS = computerPerclos(frame_count, 840) if frame_count >=840 else 0
        level = 0 if PERCLOS < cn.slight_drowsy else 1 if PERCLOS < cn.drowsy else 2
        sendValue(level)
      
        #exportValue()
        #print( 'PERCLOS: {:.2f}, Average fps: {:.2f}'.format(PERCLOS,frame_count/(time.time()-start_time )))

        
    frame_count += 1
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.stop()
cv2.destroyAllWindows()
