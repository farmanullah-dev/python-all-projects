import cv2
import face_recognition  # type: ignore
import numpy as np

# Load known face images and encode them
known_face_encodings = []
known_face_names = []

# Load images of known faces (replace with your own images)
person1_image = face_recognition.load_image_file("D:\\#PICS\Peshawar ZOO\\_MG_0245.JPG")
person1_encoding = face_recognition.face_encodings(person1_image)[0]
known_face_encodings.append(person1_encoding)
known_face_names.append("Person 1")

person2_image = face_recognition.load_image_file("person2.jpg")
person2_encoding = face_recognition.face_encodings(person2_image)[0]
known_face_encodings.append(person2_encoding)
known_face_names.append("Person 2")

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Resize frame for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all face locations and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # Check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance (i.e., closest match)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale face locations back to the original frame size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with the person's name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Quit the video window by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
