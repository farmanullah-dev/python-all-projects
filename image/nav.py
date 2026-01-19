import os
import cv2
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from skimage.feature import hog
from skimage import exposure

# Function to enhance and augment images
def augment_image(image):
    # Randomly change brightness
    alpha = np.random.uniform(0.8, 1.2)
    new_image = cv2.convertScaleAbs(image, alpha=alpha)
    return new_image

# Function to preprocess and extract HOG features with enhanced image contrast
def preprocess_image(img):
    # Histogram equalization for better contrast
    img = cv2.equalizeHist(img)
    features = hog(img, orientations=9, pixels_per_cell=(8, 8), 
                   cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
    return features

# Function to load and preprocess the dataset
def load_dataset(path):
    data = []
    labels = []
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):  # Ensure it's a folder
            for image in os.listdir(folder_path):
                img_path = os.path.join(folder_path, image)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.resize(img, (64, 64))  # Increase size for better HOG extraction
                    img = augment_image(img)  # Augment the image
                    features = preprocess_image(img)
                    data.append(features)
                    labels.append(folder)
    return np.array(data), np.array(labels)

# Load the dataset
dataset_path = "F:\\python\\Bird Speciees Dataset"
data, labels = load_dataset(dataset_path)

# Normalize the features
scaler = StandardScaler()
data = scaler.fit_transform(data)

# Reduce dimensionality using PCA
pca = PCA(n_components=0.95)  # Retain 95% variance
data = pca.fit_transform(data)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Train a Gaussian Naive Bayes classifier
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Predict the labels of the test set
y_pred = gnb.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
