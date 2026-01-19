import os
import cv2 as cv
import numpy as np

# Paths
DIR = r"F:\python\opn_cv_toturial\faces\train"  # training folder
haar_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# People list (make sure folder names match exactly)
people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']
print("People found:", people)

features = []
labels = []

def create_train():
    for person in people:
        path = os.path.join(DIR, person)
        if not os.path.exists(path):
            print(f"⚠️ Folder not found: {path}, skipping")
            continue

        label = people.index(person)

        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)

            # Only process jpg/png images
            if not (img_path.lower().endswith(".jpg") or img_path.lower().endswith(".png")):
                continue

            img = cv.imread(img_path)
            if img is None:
                print(f"⚠️ Cannot read image: {img_path}, skipping")
                continue

            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                faces_roi = cv.resize(faces_roi, (200, 200))  # consistent size
                features.append(faces_roi)
                labels.append(label)

create_train()
print("Training data prepared ✅")
print(f"Number of features: {len(features)}")
print(f"Number of labels: {len(labels)}")

if len(features) == 0:
    raise ValueError("No training data found! Check your folders and images.")

# Convert to numpy arrays
features = np.array(features, dtype="object")
labels = np.array(labels)

# Create and train LBPH recognizer
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.train(features, labels)

# Save model and data
face_recognizer.save(r"F:\python\opn_cv_toturial\face_trained.yml")
np.save(r"F:\python\opn_cv_toturial\features.npy", features, allow_pickle=True)
np.save(r"F:\python\opn_cv_toturial\labels.npy", labels)
np.save(r"F:\python\opn_cv_toturial\people.npy", people)

print("Training done ✅ Model saved at F:\\python\\opn_cv_toturial\\face_trained.yml")
