import numpy as np
import dlib
import cv2
import datetime
import csv
import Constants as cn
from imutils import face_utils
import dlib
from vas_bluetooth import vas_bluetooth


class DriverDrowsiness:

    def __init__(self):
        self.perclos = 0
        self.ear = 0
        self.abn_blink = 0
        self.ear_counter = 0
        self.noface_counter = 0
        self.frame_count = 0
        self.ABN_BLINK = []
        self.EAR_LIST = []
        self.PERCLOS_LIST = []
        self.level = 0
        self.gray = 0

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart,
         self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.filename = 'data{}.csv'.format(
            datetime.datetime.now().strftime("%m%d%y%H%M%S"))

        with open(self.filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=["Frame",
                                                              "Ear Value", "Abnormal Blink", "PERCLOS", "Alarm Level"])
            csv_writer.writeheader()

        print("[INFO] loading face detector ...")
        self.detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_alt.xml")

        print("[INFO] loading facial landmark predictor ...")
        self.predictor = dlib.shape_predictor(
            "../shape_predictor_68_face_landmarks.dat")

        self.bt = vas_bluetooth("00:19:10:11:0E:3F")
        self.connected = bt.connect()

    def euclidean_dist(self, ptA, ptB):
        return np.linalg.norm(ptA - ptB)

    def eye_aspect_ratio(self, eye):
        A = self.euclidean_dist(eye[1], eye[5])
        B = self.euclidean_dist(eye[2], eye[4])
        C = self.euclidean_dist(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    def exportValue(self):

        with open(self.filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=["Frame",
                                                              "Ear Value", "Abnormal Blink", "PERCLOS", "Alarm Level"])
            info = {"Frame": self.frame_count,
                    "Ear Value": "{:.3f}".format(self.ear),
                    "Abnormal Blink": self.abn_blink,
                    "PERCLOS": "{:.2f}".format(self.perclos),
                    "Alarm Level": self.level}
            csv_writer.writerow(info)
        return

    def computerPerclos(self, i, N):
        if i >= 840:
            self.perclos = sum(self.ABN_BLINK[(i-N):])/N * 100
        else:
            self.perclos = 0
        self.PERCLOS_LIST.append(self.perclos)
        return self.perclos

    def isNoFaceThreshold(self):
        return self.noface_counter >= cn.NOFACE_THRESH

    def sendAlarm(self, level):
        self.level = level

        if not self.connected:
            print("[WARNING] Bluetooth alarm not connected")
            return

        print("[INFO] Sending Alarm Level: ", self.level)
        self.bt.send(level)
        return

    def detectFaces(self, frame):
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.detector.detectMultiScale(self.gray, 1.3, 5)

    def computeEAR(self, shape):
        leftEye = shape[self.lStart:self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)

        self.ear = (leftEAR + rightEAR) / 2.0

        return self.ear

    def detectFacialLandmarks(self, rect):
        shape = self.predictor(self.gray, rect)
        shape = face_utils.shape_to_np(shape)

        return shape

    def isBelowEARThreshold(self):
        return self.ear <= cn.EYE_AR_THRESH

    def isAbnormalBlink(self):
        return self.ear_counter >= cn.BLINK_THRESH

    def isLongBlink(self):
        return self.ear_counter >= cn.EYE_AR_CONSEC_FRAMES

    def updateLists(self):
        self.ABN_BLINK.append(self.abn_blink)
        self.EAR_LIST.append(self.ear)
        return

    def incrementFrame(self):
        self.frame_count += 1
        return
