import vas_bluetooth
import time
import random


bt = vas_bluetooth("00:19:10:11:0E:3F")


if bt.connect():

    for count in range(0, 10):
        alarm = random.randint(0, 3)

        print("Sending alarm level: ", alarm)
        bt.send(alarm)

        time.sleep(1)

bt.disconnect()
