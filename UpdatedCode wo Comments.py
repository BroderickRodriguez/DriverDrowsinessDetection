from imutils.video import FileVideoStream
from imutils import face_utils
from DriverDrowsiness import DriverDrowsiness
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
dd = DriverDrowsiness()

ap.add_argument("-v", "--video", required=True,
                help="path to where the video source resides")
args = vars(ap.parse_args())


print("[INFO] starting video stream")
cap = FileVideoStream(args["video"]).start()
time.sleep(1.0)

ear = 0

while cap.more():

    frame = cap.read()
    frame = imutils.resize(frame, width=360)
    rects = dd.detectFaces(frame)

    dd.abn_blink = 0
    if len(rects) == 0:
        dd.noface_counter += 1
        if dd.isNoFaceThreshold():
            print("[WARNING] NO FACE DETECTED")
            dd.sendAlarm(3)
        dd.updateLists()

    else:

        dd.noface_counter = 0

        for (x, y, w, h) in rects:

            rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
            shape = dd.detectFacialLandmarks(rect)
            ear = dd.computeEAR(shape)

            # Display purposes
            # ---------OPTIONAL------------------------------------------
            # leftEyeHull = cv2.convexHull(leftEye)
            # rightEyeHull = cv2.convexHull(rightEye)
            # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # cv2.putText(frame, "EAR: {:.3f}".format(ear), (95, 30),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # -----------------------------------------------------------

        if dd.isBelowEARThreshold():
            dd.ear_counter += 1

            if dd.isAbnormalBlink():
                dd.abn_blink = 1

                if dd.isLongBlink():
                    # draw an alarm on the frame
                    # cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                    #    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    dd.sendAlarm(2)
        else:
            dd.abn_blink = 0
            dd.ear_counter = 0

        dd.updateLists()

        # if frame_count == 840:
        #     print('Average EAR for the first 1 minute:{:.2f}'.format(
        #         sum(dd.EAR_LIST)/840))

        PERCLOS = dd.computerPerclos(dd.frame_count, 840)
        level = 0 if PERCLOS < cn.slight_drowsy else 1 if PERCLOS < cn.drowsy else 2
        dd.sendAlarm(level)

        # exportValue()
        #print( 'PERCLOS: {:.2f}, Average fps: {:.2f}'.format(PERCLOS,frame_count/(time.time()-start_time )))

    dd.incrementFrame()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.stop()
cv2.destroyAllWindows()
