import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from skimage.feature import hog
import xgboost as xgb
from imblearn.over_sampling import SMOTE # type: ignore
from sklearn.utils import class_weight

# Function to enhance and augment images
def augment_image(image):
    # Randomly change brightness
    alpha = np.random.uniform(0.8, 1.2)
    new_image = cv2.convertScaleAbs(image, alpha=alpha)

    # Additional augmentations: flip and rotation
    if np.random.rand() > 0.5:
        new_image = cv2.flip(new_image, 1)  # Horizontal flip
    if np.random.rand() > 0.5:
        angle = np.random.uniform(-15, 15)
        M = cv2.getRotationMatrix2D((new_image.shape[1] // 2, new_image.shape[0] // 2), angle, 1)
        new_image = cv2.warpAffine(new_image, M, (new_image.shape[1], new_image.shape[0]))
    
    return new_image

# Function to preprocess and extract HOG features
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
pca = PCA(n_components=0.90)  # Retain 95% variance
data = pca.fit_transform(data)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Handle class imbalance using SMOTE
smote = SMOTE()
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Convert labels to numeric for XGBoost
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y_train_res = label_encoder.fit_transform(y_train_res)
y_test = label_encoder.transform(y_test)

# Train an XGBoost classifier
xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', n_estimators=400, learning_rate=0.1)
xgb_model.fit(X_train_res, y_train_res)

# Predict the labels of the test set
y_pred = xgb_model.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
