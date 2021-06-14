from vas_bluetooth import vas_bluetooth
import datetime

bt = vas_bluetooth("00:19:10:11:0E:3F")
connected = bt.connect()

# TODO: send sample data with timestamp
bt.send(1)
print("Sample data sent at ", datetime.datetime.now())

# TODO: vas version for this