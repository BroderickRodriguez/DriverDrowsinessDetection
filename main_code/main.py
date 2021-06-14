from imutils.video import FileVideoStream
from imutils.video import WebcamVideoStream
from imutils import face_utils
from DriverDrowsiness import DriverDrowsiness
from fps import FPS
import argparse
import imutils
import time
import cv2
import dlib
import Constants as cn

ap = argparse.ArgumentParser()
dd = DriverDrowsiness()
fps = FPS()

ap.add_argument("-v", "--video", required=False,
                help="path to where the video source resides")
ap.add_argument("-m", "--mode", required=True,
                help="choose if using video file or stream")
args = vars(ap.parse_args())

print("[INFO] starting video stream")
if args["mode"] == "file":
    cap = FileVideoStream(args["video"]).start()
else:
    cap = WebcamVideoStream(src=0).start()
time.sleep(1.0)
fps.start()
ear = 0

while True:
    sendAlarm = True
    frame = cap.read()
    frame = imutils.resize(frame, width=360)
    rects = dd.detectFaces(frame)

    dd.abn_blink = 0
    if len(rects) == 0:
        dd.noface_counter += 1
        if dd.isNoFaceThreshold():
            #print("[WARNING] NO FACE DETECTED")
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
            leftEyeHull = cv2.convexHull(dd.leftEye)
            rightEyeHull = cv2.convexHull(dd.rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            cv2.putText(frame, "EAR: {:.3f}".format(ear), (95, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # -----------------------------------------------------------

        if dd.isBelowEARThreshold():
            dd.ear_counter += 1

            if dd.isAbnormalBlink():
                dd.abn_blink = 1

                if dd.isLongBlink():
                    # draw an alarm on the frame
                    # cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                    #    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    sendAlarm = False
                    dd.sendAlarm(2)

        else:
            dd.abn_blink = 0
            dd.ear_counter = 0

        dd.updateLists()

        # if frame_count == 840:
        #     print('Average EAR for the first 1 minute:{:.2f}'.format(
        #         sum(dd.EAR_LIST)/840))

        PERCLOS = dd.computerPerclos(dd.frame_count, cn.TOTAL_WINDOW_FRAMES)
        level = 0 if PERCLOS < cn.slight_drowsy else 1 if PERCLOS < cn.drowsy else 2
        if sendAlarm:
            dd.sendAlarm(level)
        
        cv2.putText(frame, "PERCLOS: {:.3f}".format(PERCLOS), (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # exportValue()
        #print( 'PERCLOS: {:.2f}, Average fps: {:.2f}'.format(PERCLOS,frame_count/(time.time()-start_time )))
    dd.exportValue()
    dd.incrementFrame()
    fps.update()
    fps.stop()
    
    cv2.putText(frame, "Average FPS: {:.1f}".format(fps.fps()), (10, 240),
    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if args["mode"] == "file" and not cap.more():
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.stop()
cv2.destroyAllWindows()
