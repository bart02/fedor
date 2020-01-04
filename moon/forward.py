import socket
import time


class Robot:
    sock = socket.socket()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connected = False

    t = 0

    def __init__(self, host):
        self.host = host

    def connect(self):
        self.sock.connect((self.host, 10099))
        self.connected = True

    def disconnect(self):
        self.sock.close()
        self.connected = False

    def connect1(self):
        self.sock.connect((self.host, 11099))
        self.connected = True

    def disconnect1(self):
        self.sock.close()
        self.connected = False

    def forward(self, t):
        while t > 0:
            self.sock.send(b'robot:motors:R.WheelF:velset:100\n')
            self.sock.send(b'robot:motors:R.WheelB:velset:100\n')
            self.sock.send(b'robot:motors:L.WheelF:velset:100\n')
            self.sock.send(b'robot:motors:L.WheelB:velset:100\n')
            time.sleep(1)
            self.sock.send(b'version:shell\n')
            t -= 1

    def stop(self):
        self.sock.send(b'robot:motors:R.WheelF:velset:0\n')
        self.sock.send(b'robot:motors:R.WheelB:velset:0\n')
        self.sock.send(b'robot:motors:L.WheelF:velset:0\n')
        self.sock.send(b'robot:motors:L.WheelB:velset:0\n')
        time.sleep(0.1)

    def reset(self):
        self.client.sendto(b'scene:reset\n', (self.host, 10000))
        time.sleep(3)
        self.client.close()


fedor = Robot('192.168.0.108')
fedor.reset()

#fedor.connect1()
#fedor.disconnect1()

fedor.connect1()
fedor.stop()
fedor.disconnect1()
