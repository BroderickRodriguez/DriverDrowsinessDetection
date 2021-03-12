import bluetooth


class vas_bluetooth:

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1

    def __init__(self, addr, tries=5):
        self.addr = addr
        self.tries = tries

    def connect(self):

        print("[INFO] Searching for devices ...")
        nearby_devices = bluetooth.discover_devices()
        num = 0
        while (self.addr not in nearby_devices):

            print("[INFO] Searching for devices ...")
            nearby_devices = bluetooth.discover_devices()
            num += 1

            if (num == tries):
                return False

        self.sock.connect((self.addr, self.port))
        print("[INFO] Successfully connected to VAS, ",
              bluetooth.lookup_name(self.addr))
        return True

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()

    def send(self, level):
	self.sock.send(str(level).encode())
