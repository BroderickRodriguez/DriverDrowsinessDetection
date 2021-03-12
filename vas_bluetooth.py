import bluetooth


class VAS:

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def __init__(self, addr):
        print "[INFO] Searching for devices ..."
        self.addr = addr
        while !self.connect():
            pass

    def connect(self):

        nearby_devices = bluetooth.discover_devices()
        if vas_addr in nearby_devices:
            self.sock.connect((self.addr))
            print "[INFO] Successfully connected to VAS "
            return True
        return False

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()

    def send(self, level):
        self.sock.send(data)
