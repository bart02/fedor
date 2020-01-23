import socket
from time import sleep
from cv2 import VideoCapture


class Connection:
    sock = socket.socket()
    connected = False

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.connected = True

    def disconnect(self):
        self.sock.close()
        self.connected = False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def request(self, req):
        while True:
            try:
                self.sock.send((req + '\n').encode())
                sleep(0.01)
                data = self.sock.recv(1024)
                if b'\xf0' in data:
                    return None
                elif b'\xf1' in data:
                    return data.replace(b'\xf1', b'').replace(b'\r\n', b'').decode()
                elif data == b'':
                    self.reconnect()
                else:
                    raise BaseException(b'Request error: ' + data)
            except (ConnectionResetError, ConnectionAbortedError):
                self.reconnect()


class Platform(Connection):
    def __init__(self, host):
        self.host = host
        super().__init__(self.host, 11099)

    def go(self, speed=None, dir=None):
        if speed is not None:
            self.request('robot:motors:R.WheelF:velset:' + str(speed))
            self.request('robot:motors:R.WheelB:velset:' + str(speed))
            self.request('robot:motors:L.WheelF:velset:' + str(speed))
            self.request('robot:motors:L.WheelB:velset:' + str(speed))
        if dir is not None:
            self.request('robot:motors:R.DriveWheelF:posset:' + str(dir))
            self.request('robot:motors:L.DriveWheelF:posset:' + str(dir))


    def gograd(self, deg, pov=None):
        plus = 0
        lastpos = 0
        d = 0
        s = 0
        while d < deg:
            if deg - d < 100:
                s = 40
            else:
                s = 100
            self.go(s, pov)
            pos = (float(self.request('robot:motors:R.WheelF:posget')[:-1]))
            if pos < 0:
                if lastpos > 0:
                    plus += 180
                posv = 180 + pos
            else:
                if lastpos < 0:
                    plus += 180
                posv = pos
            lastpos = pos
            d = posv + plus
            print(d)
        self.stop()

    def stop(self):
        self.go(speed=0, dir=0)

    def go_time(self, t, speed=None, dir=None):
        self.go(speed, dir)
        sleep(t)
        self.stop()


class Body(Connection):
    def __init__(self, host):
        self.host = host
        super().__init__(self.host, 10099)
        self.motors = self.get_all_motors_data()
        self.cap = VideoCapture('http://{}:800/'.format(self.host))

    def video_restart(self):
        self.cap.release()
        self.cap = VideoCapture('http://{}:800/'.format(self.host))

    def get_sensor_data(self, sensor):
        head = self.request('robot:sensors:{}:list'.format(sensor))
        head = head.split(';')

        data = self.request('robot:sensors:{}'.format(sensor))
        data = data.split(';')

        if len(head) != len(data):
            raise BaseException('Length is not equal')

        return dict(zip(head, data))

    def get_all_motors_data(self):
        motors = self.request('robot:motors:list').split(';')
        motors.pop(-1)

        M = {}
        for e in motors:
            M[e] = round(float(self.request('robot:motors:{}:posget'.format(e)).replace(';', '')))

        return M

    def index(self):
        for e in self.motors:
            self.request('robot:motors:{}:posset:{}'.format(e, self.motors[e]))

    def fist(self):
        self.request('robot:motors:L.Finger.Index:posset:-45')
        self.request('robot:motors:L.Finger.Middle:posset:-45')
        self.request('robot:motors:L.Finger.Ring:posset:-45')
        self.request('robot:motors:L.Finger.Little:posset:-45')
        self.request('robot:motors:L.Finger.Thumb:posset:-55')

    def antifist(self):
        self.request('robot:motors:L.Finger.Index:posset:0')
        self.request('robot:motors:L.Finger.Middle:posset:0')
        self.request('robot:motors:L.Finger.Ring:posset:0')
        self.request('robot:motors:L.Finger.Little:posset:0')
        self.request('robot:motors:L.Finger.Thumb:posset:0')

    def open_box(self):
        self.request('robot:motors:L.ShoulderF:posset:10')
        self.request('robot:motors:TorsoR:posset:50')
        self.request('robot:motors:TorsoF:posset:-20')
        self.request('robot:motors:L.WristF:posset:-20')
        self.request('robot:motors:L.Elbow:posset:-50')
        self.request('robot:motors:L.ShoulderS:posset:80')
        sleep(1)
        self.request('robot:motors:TorsoR:posset:-80')
        sleep(1)
        self.request('robot:motors:L.ShoulderS:posset:70')
        self.request('robot:motors:L.WristS:posset:-20')
        sleep(1)
        self.fist()
        sleep(1)
        self.request('robot:motors:L.ShoulderS:posset:100')
        self.request('robot:motors:TorsoR:posset:-90')
        sleep(1)
        self.antifist()
        self.request('robot:motors:L.WristS:posset:20')
        self.request('robot:motors:L.Elbow:posset:0')
        sleep(1)
        self.request('robot:motors:R.ShoulderF:posset:-150')
        sleep(1)
        self.request('robot:motors:TorsoR:posset:40')
        sleep(1)
        self.request('robot:motors:R.ShoulderF:posset:-40')
        sleep(1)
        self.request('robot:motors:TorsoR:posset:-60')
        self.request('robot:motors:R.ShoulderF:posset:-60')
        sleep(1)


class Scene:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, host):
        self.host = host

    def reset(self):
        self.sock.sendto(b'scene:reset\n', (self.host, 10000))
        sleep(3)


class Robot:
    def __init__(self, host, platform=False):
        self.host = host

        self.body = Body(self.host)

        if platform:
            self.platform = Platform(self.host)
        else:
            self.request = self.body.request

        self.scene = Scene(self.host)
        self.reset = self.scene.reset
