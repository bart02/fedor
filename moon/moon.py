import sys
sys.path.insert(0, '..')
from helpers.robot import *
import cv2 as cv
from helpers.utils import findBigContour


# Connect
fedor = Robot('localhost', platform=True)

# Go directly (without sensors)
fedor.platform.go_time(25, 100, -5)
fedor.platform.go_time(20, 100, 60)

fedor.body.request('robot:motors:L.ShoulderF:posset:-77')
fedor.body.request('robot:motors:L.Elbow:posset:0')

# OpenCV button alignment
for _ in range(2):  # If you need, you can edit number of tryings of button click
    fedor.body.video_restart()
    while True:
        for _ in range(6):  # buffer
            ret, frame = fedor.body.cap.read()

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        thresh = cv.inRange(hsv, (37, 40, 107), (81, 251, 184))

        cnt = findBigContour(thresh)
        if cnt is not None:
            x, y, w, h = cv.boundingRect(cnt)
            center = ((x + (x + w)) // 2, (y + (y + h)) // 2)
            inp = (center[0] - 400) * -1
            out = 140 - inp * 0.6
            if out > 60:
                out = 60
            if out < -60:
                out = -60
            print(out)
            fedor.platform.go(50, out)
            # cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # cv.drawContours(frame, cnt, -1, (0, 0, 255), 3)
            cv.circle(frame, center, 2, (255, 0, 0), 2)
        else:
            fedor.platform.go(50, 0)
            if float(fedor.body.get_sensor_data('imu')['Roll'].replace(',', '.')) > 7:
                fedor.platform.stop()
                break

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    fedor.body.cap.release()
    cv.destroyAllWindows()

    fedor.platform.go_time(10, -100, 0)

fedor.platform.go_time(7, 100, 50)
fedor.platform.go_time(7, 100, 0)
fedor.platform.go_time(15, 100, 60)
fedor.platform.go_time(25, -100, -5)
