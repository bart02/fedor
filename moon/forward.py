import socket
import time


class Robot:
    sock = socket.socket()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connected = False

    t = 0

    def __init__(self, host):
        self.host = host

    def connect_body(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, 10099))
        self.connected = True

    def disconnect(self):
        self.sock.close()
        self.connected = False

    def connect_base(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, 11099))
        self.connected = True

    def request(self, req):
        self.sock.send(req.encode())
        time.sleep(0.01)
        data = self.sock.recv(1024)
        if b'\xf0' in data:
            return None
        elif b'\xf1' in data:
            return data.replace(b'\xf1', b'').replace(b'\r\n', b'').decode()
        else:
            raise BaseException('Request error: ' + data.decode())

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

    def get_sensor_data(self, sensor):
        head = self.request('robot:sensors:{}:list\n'.format(sensor))
        head = head.split(';')

        data = self.request('robot:sensors:{}\n'.format(sensor))
        data = data.split(';')

        if len(head) != len(data):
            raise BaseException('Length is not equal')

        return dict(zip(head, data))


fedor = Robot('192.168.0.108')
fedor.reset()

#fedor.connect1()
#fedor.disconnect1()

fedor.connect_base()
fedor.stop()
fedor.disconnect()

fedor.connect_body()
print(fedor.get_sensor_data('imu'))
fedor.disconnect()
