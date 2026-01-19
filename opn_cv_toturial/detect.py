import os
import cv2 as cv

# Haar Cascade
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# People list (must match training order)
people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']

# Load trained recognizer
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read(r"F:\python\opn_cv_toturial\face_trained.yml")

# Path to validation dataset
VAL_DIR = r"F:\python\opn_cv_toturial\faces\val"

# Loop through each person folder in val
for person in os.listdir(VAL_DIR):
    person_path = os.path.join(VAL_DIR, person)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        img = cv.imread(img_path)
        if img is None:
            print(f"⚠️ Skipping unreadable file: {img_path}")
            continue

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in faces_rect:
            faces_roi = gray[y:y+h, x:x+w]

            label, confidence = face_recognizer.predict(faces_roi)
            print(f"Prediction: {people[label]} (Confidence: {confidence:.2f}) — File: {img_name}")

            cv.putText(img, people[label], (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
            cv.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

        cv.imshow("Detected Face", img)
        cv.waitKey(1000)  # show each image for 1 second

cv.destroyAllWindows()
