import os
import colorama


colorama.init(autoreset=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


from ultralytics import YOLO
import cv2 

model = YOLO('yolov8l.pt')
cap = cv2.VideoCapture(0)

# Create a named window and set it to fullscreen
cv2.namedWindow('YOLOv8 Detection', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('YOLOv8 Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = model(frame, conf=0.8, save=True)

    # Display the annotated frame
    cv2.imshow('YOLOv8 Detection', result[0].plot())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
