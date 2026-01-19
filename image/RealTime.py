from ultralytics import YOLO
import cv2

# Load the pre-trained YOLOv8 model
model = YOLO('yolov8n.pt')

# Path to your video file
video_path = 'F:/python/image/Cars Moving On Road Stock Footage - Free Download.mp4'


# Open the video file
cap = cv2.VideoCapture(video_path)

cv2.namedWindow('YOLOv8 Object Detection', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('YOLOv8 Object Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Loop through the video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if no frame is returned (end of video)

    # Run YOLOv8 on the frame
    results = model(frame)

    # Get the annotated frame with detections
    annotated_frame = results[0].plot()

    # Display frame
    cv2.imshow('YOLOv8 Object Detection', annotated_frame)

    # Press 'q' to quit the video early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
