import socket
import time


class Robot:
    sock = socket.socket()
    connected = False

    def __init__(self, host):
        self.host = host
        self.connect()

    def connect(self):
        self.sock.connect((self.host, 10099))
        self.connected = True

    def disconnect(self):
        self.sock.close()
        self.connected = False

    def fist(self):
        self.sock.send(b'robot:motors:L.Finger.Index:posset:-45\n')
        self.sock.send(b'robot:motors:L.Finger.Middle:posset:-45\n')
        self.sock.send(b'robot:motors:L.Finger.Ring:posset:-45\n')
        self.sock.send(b'robot:motors:L.Finger.Little:posset:-45\n')
        self.sock.send(b'robot:motors:L.Finger.Thumb:posset:-55\n')

    def antifist(self):
        self.sock.send(b'robot:motors:L.Finger.Index:posset:0\n')
        self.sock.send(b'robot:motors:L.Finger.Middle:posset:0\n')
        self.sock.send(b'robot:motors:L.Finger.Ring:posset:0\n')
        self.sock.send(b'robot:motors:L.Finger.Little:posset:0\n')
        self.sock.send(b'robot:motors:L.Finger.Thumb:posset:0\n')

    def open_box(self):
        self.sock.send(b'robot:motors:L.ShoulderF:posset:10\n')
        self.sock.send(b'robot:motors:TorsoR:posset:50\n')
        self.sock.send(b'robot:motors:TorsoF:posset:-20\n')
        self.sock.send(b'robot:motors:L.WristF:posset:-20\n')
        self.sock.send(b'robot:motors:L.Elbow:posset:-50\n')
        self.sock.send(b'robot:motors:L.ShoulderS:posset:80\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:TorsoR:posset:-80\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:L.ShoulderS:posset:70\n')
        self.sock.send(b'robot:motors:L.WristS:posset:-20\n')
        time.sleep(1)
        self.fist()
        time.sleep(1)
        self.sock.send(b'robot:motors:L.ShoulderS:posset:100\n')
        self.sock.send(b'robot:motors:TorsoR:posset:-90\n')
        time.sleep(1)
        self.antifist()
        self.sock.send(b'robot:motors:L.WristS:posset:20\n')
        self.sock.send(b'robot:motors:L.Elbow:posset:0\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:R.ShoulderF:posset:-150\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:TorsoR:posset:40\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:R.ShoulderF:posset:-40\n')
        time.sleep(1)
        self.sock.send(b'robot:motors:TorsoR:posset:-60\n')
        self.sock.send(b'robot:motors:R.ShoulderF:posset:-60\n')
        time.sleep(1)


fedor = Robot('192.168.0.108')

fedor.open_box()
fedor.disconnect()
