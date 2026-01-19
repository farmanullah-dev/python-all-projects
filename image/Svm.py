import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from skimage.feature import hog
from skimage import exposure
from sklearn.utils import class_weight

# Function to enhance and augment images
def augment_image(image):
    # Randomly change brightness
    alpha = np.random.uniform(0.8, 1.2)
    new_image = cv2.convertScaleAbs(image, alpha=alpha)
    return new_image

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
                    features = hog(img, orientations=9, pixels_per_cell=(8, 8), 
                    cells_per_block=(2, 2), block_norm='L2-Hys', visualize=False)
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

# Calculate class weights for handling class imbalance
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)

# Perform hyperparameter tuning for SVM
param_grid = {
    'C': [0.1, 1, 10, 100,110,120,130,140,150,160,170,180,190,200],
    'kernel': ['linear', 'rbf', 'poly'],
    'gamma': ['scale', 'auto']
}
grid_search = GridSearchCV(SVC(class_weight='balanced'), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Train the best model on the training set
best_clf = grid_search.best_estimator_
best_clf.fit(X_train, y_train)

# Predict the labels of the test set
y_pred = best_clf.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Best Params:", grid_search.best_params_)
print("Accuracy:", accuracy)
