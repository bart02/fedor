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
