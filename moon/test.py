from robot import *
import cv2 as cv


def findBigContour(mask, limit=10):
    contours = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]
    if contours:
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        if cv.contourArea(contours[0]) > limit:
            return contours[0]
        else:
            return None
    else:
        return None


fedor = Robot('localhost', platform=True)


fedor.platform.go_time(25, 100, -5)
fedor.platform.go_time(20, 100, 60)


fedor.body.request('robot:motors:L.ShoulderF:posset:-77')
fedor.body.request('robot:motors:L.Elbow:posset:0')
for i in range(1):
    fedor.body.video_restart()
    while True:
        for i in range(6):  # buffer
            ret, frame = fedor.body.cap.read()

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # накладываем фильтр на кадр в модели HSV
        thresh = cv.inRange(hsv, (37, 40, 107), (81, 251, 184))

        cnt = findBigContour(thresh)
        if cnt is not None:
            x,y,w,h = cv.boundingRect(cnt)
            center = ((x + x + w) // 2, (y + y + h) // 2)
            inp = (center[0] - 400) * -1
            out = 150 - inp * 0.6
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



    fedor.platform.go_time(10, -100, 0)
fedor.body.cap.release()
cv.destroyAllWindows()

fedor.platform.gograd(700, 50)
fedor.platform.gograd(850)
fedor.platform.gograd(1700, 50)
fedor.platform.go_time(27, -100)