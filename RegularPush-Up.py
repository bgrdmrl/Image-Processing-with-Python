import cv2
import PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
state = "Up"
color = (0, 0, 255)
colorBody = (0, 0, 255)

while True:
    success, img = cap.read()
    img = detector.FindPose(img, False)
    lmList = detector.FindPosition(img, False)

    if len(lmList) != 0:
        angleRightArm = detector.Find3Angle(img, 12, 14, 16, color)          # Vücudun sağına göre çalışıyor
        angleRightBody = detector.Find3AngleBodyCheck(img, 12, 24, 26, colorBody)
        per = np.interp(angleRightArm, (20, 170), (0, 100))
        bar = np.interp(angleRightArm, (30, 170), (450, 100))

        if 190 > angleRightBody > 170:
            colorBody = (0, 255, 0)
            if 160 > angleRightArm > 65:
                color = (0, 0, 255)

            if angleRightArm >= 160:
                color = (0, 255, 0)
                if state == "Up":
                    state = "Down"

            if angleRightArm <= 65:
                color = (0, 255, 0)
                if state == "Down":
                    count += 1
                    state = "Up"
        else:
            colorBody = (0, 0, 255)

        # Count
        cv2.rectangle(img, (0, 0), (150, 150), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # Draw Bar
        cv2.rectangle(img, (565, 100), (600, 450), color, 3)
        cv2.rectangle(img, (565, int(bar)), (600, 450), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (510, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

    cv2.imshow("Regular Push-Up", img)
    cv2.waitKey(1)
