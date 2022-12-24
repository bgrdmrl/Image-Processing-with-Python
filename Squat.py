import cv2
import PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()
count = 0
state = "Up"
color = (0, 0, 255)

while True:
    success, img = cap.read()
    img = detector.FindPose(img, False)
    lmList = detector.FindPosition(img, False)

    if len(lmList) != 0:
        angleRightLeg = detector.Find3Angle(img, 24, 26, 28, color)  # Sağ bacak ama vücudun soluna göre çalışıyor
        per = np.interp(angleRightLeg, (20, 170), (0, 100))
        bar = np.interp(angleRightLeg, (30, 170), (450, 100))

        color = (0, 0, 255)

        if angleRightLeg >= 170:
            color = (0, 255, 0)
            if state == "Up":
                state = "Down"

        if angleRightLeg <= 90:
            color = (0, 255, 0)
            if state == "Down":
                count += 1
                state = "Up"

        # Count
        cv2.rectangle(img, (0, 0), (150, 150), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # Draw Bar
        cv2.rectangle(img, (565, 100), (600, 450), color, 3)
        cv2.rectangle(img, (565, int(bar)), (600, 450), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (510, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

    cv2.imshow("Squat", img)
    cv2.waitKey(1)
