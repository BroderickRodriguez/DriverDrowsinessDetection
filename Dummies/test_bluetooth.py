from vas_bluetooth import vas_bluetooth
import time
import random


bt = vas_bluetooth("00:19:10:11:0E:3F")


if bt.connect():

    for count in range(0, 10):

        print("Sending Alarm Level 0: Awake")
        for i in range(0,5):
                bt.send(0)
                time.sleep(1)
        print("Sending Alarm Level 1: Slightly Drowsy")
        for j in range(0,10):
                bt.send(1)
                time.sleep(1)
        print("Sending Alarm Level 2: Drowsy")
        for k in range(0,10):
                bt.send(2)
                time.sleep(1)
        print("Sending Alarm Level 3: No Face Detected")
        for l in range(0,10):
                bt.send(3)
                time.sleep(1)
                


bt.disconnect()
