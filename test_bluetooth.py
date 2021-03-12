import bluetooth
import time

print ("Searching for devices...")
print ("")

nearby_devices = bluetooth.discover_devices()

num = 0

print ("Select your device by entering its corresponding number ..")
for i in nearby_devices:
	num+=1
	print (num , ": " , bluetooth.lookup_name(i))


selection = int(input("> ")) - 1
print ("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]

port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

sock.connect((bd_addr, port))

time.sleep(2)

print ("sending 2 to device")
sock.send("2")

time.sleep(2)
print ("closing sock")
sock.close()
