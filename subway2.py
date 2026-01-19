import cv2
import mediapipe as mp
import numpy as np
import time
from pynput.keyboard import Key, Controller

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize Mediapipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose(model_complexity=0, smooth_landmarks=True)
mpDraw = mp.solutions.drawing_utils

# Keyboard controller
keyboard = Controller()

# For FPS and movement counters
pTime = 0
upCount = downCount = leftCount = rightCount = 0

# Marker zones (adjust according to your distance from camera)
topMarker = 150
bottomMarker = 300
leftMarker = 200
rightMarker = 440

# State flags
pStateY = cStateY = 1
pStateX = cStateX = 1

# Keys for Subway Surfers
upKey = Key.up
downKey = Key.down
leftKey = Key.left
rightKey = Key.right

DRAW_LANDMARKS = True

while True:
    ret, img = cap.read()
    if not ret:
        continue

    # Flip for mirror effect
    img = cv2.flip(img, 1)

    # Draw guide lines
    cv2.line(img, (0, topMarker), (640, topMarker), (255, 255, 255), 2)
    cv2.line(img, (0, bottomMarker), (640, bottomMarker), (0, 0, 255), 2)
    cv2.line(img, (leftMarker, 0), (leftMarker, 480), (0, 255, 0), 2)
    cv2.line(img, (rightMarker, 0), (rightMarker, 480), (255, 0, 0), 2)

    # Convert to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        if DRAW_LANDMARKS:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        h, w, c = img.shape

        # Use RIGHT HAND wrist point
        rightWrist = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST]
        x, y = int(rightWrist.x * w), int(rightWrist.y * h)

        # Draw circle at wrist
        cv2.circle(img, (x, y), 12, (0, 0, 255), cv2.FILLED)

        # --- Vertical Movement Detection ---
        if y < topMarker:  # Jump
            cStateY = 0
            if pStateY > cStateY:
                keyboard.press(upKey)
                keyboard.release(upKey)
                print("Jump ↑")
                upCount += 1
                pStateY = cStateY

        elif y > bottomMarker:  # Roll
            cStateY = 2
            if pStateY < cStateY:
                keyboard.press(downKey)
                keyboard.release(downKey)
                print("Roll ↓")
                downCount += 1
                pStateY = cStateY

        else:
            cStateY = 1
            pStateY = 1

        # --- Horizontal Movement Detection ---
        if x < leftMarker:  # Move Left
            cStateX = 0
            if pStateX > cStateX:
                keyboard.press(leftKey)
                keyboard.release(leftKey)
                print("Move Left ←")
                leftCount += 1
                pStateX = cStateX

        elif x > rightMarker:  # Move Right
            cStateX = 2
            if pStateX < cStateX:
                keyboard.press(rightKey)
                keyboard.release(rightKey)
                print("Move Right →")
                rightCount += 1
                pStateX = cStateX

        else:
            cStateX = 1
            pStateX = 1

    # FPS calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime
    # Show info
    cv2.putText(img, f"FPS: {int(fps)}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f"Up: {upCount}  Down: {downCount}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, f"Left: {leftCount}  Right: {rightCount}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Subway Surfers Control", img)
    cv2.setWindowProperty("Subway Surfers Control", cv2.WND_PROP_TOPMOST, 1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
