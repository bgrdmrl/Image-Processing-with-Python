import cv2
import PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
state = "Up"
color = (0, 0, 255)
colorBodyCheck = (0, 0, 255)

while True:
    success, img = cap.read()
    img = detector.FindPose(img, False)
    lmList = detector.FindPosition(img, False)

    if len(lmList) != 0:
        angleRightBody = detector.Find3Angle(img, 12, 24, 26, color)
        angleLegCheck = detector.Find3AngleBodyCheck(img, 24, 26, 28, colorBodyCheck)
        per = np.interp(angleRightBody, (20, 130), (0, 100))     # Vücudun sağına göre çalışıyor
        bar = np.interp(angleRightBody, (30, 130), (450, 100))

        color = (0, 0, 255)

        if angleLegCheck > 300:
            colorBodyCheck = (0, 255, 0)
            if 120 > angleRightBody > 110:
                color = (0, 0, 255)

            if angleRightBody >= 120:
                color = (0, 255, 0)
                if state == "Up":
                    state = "Down"

            if angleRightBody <= 110:
                color = (0, 255, 0)
                if state == "Down":
                    count += 1
                    state = "Up"
        else:
            colorBodyCheck = (0, 0, 255)

        # Count
        cv2.rectangle(img, (0, 0), (150, 150), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # Draw Bar
        cv2.rectangle(img, (565, 100), (600, 450), color, 3)
        cv2.rectangle(img, (565, int(bar)), (600, 450), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (510, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

    cv2.imshow("Crunch", img)
    cv2.waitKey(1)
