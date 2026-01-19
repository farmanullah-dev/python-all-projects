import os
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from PIL import Image

# Path to the Bird Species Dataset
data_path = "F:\\python\\Bird Speciees Dataset"

# Image dimensions for resizing
img_height, img_width = 64, 64

# Load dataset: Assuming images are inside subfolders, where folder names represent the species
image_paths = []
labels = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            image_paths.append(os.path.join(root, file))
            labels.append(os.path.basename(root))

# Resize and flatten images
images = []
for img_path in image_paths:
    try:
        img = Image.open(img_path).convert('RGB')
        img_resized = img.resize((img_width, img_height))
        images.append(np.array(img_resized).flatten())
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

# Convert to NumPy arrays
X = np.array(images)
y = np.array(labels)

# Normalize pixel values
X = X / 255.0

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Apply PCA for dimensionality reduction (optional but can improve performance)
pca = PCA(n_components=15)  # You could try a fixed number of components
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Define hyperparameter grid for Decision Tree (extended search)
param_grid = {
    'max_depth': [5, 6, 7, 8, 9, 10, 12, 15, 20, 25],  # Depth of the tree (increase max_depth range)
    'min_samples_split': [2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30],  # More values for splitting
    'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # More granular control on leaf nodes
    'criterion': ['gini', 'entropy'],  # Keep these two for now
    'max_features': ['sqrt', 'log2', None],  # Test these options
    'splitter': ['best', 'random'],  # Explore both splitting strategies
    'class_weight': [None, 'balanced']  # Try balanced class weights to handle class imbalances
}

# Initialize Decision Tree Classifier
dtc = DecisionTreeClassifier(random_state=42)

# Hyperparameter tuning using RandomizedSearchCV for faster performance
random_search = RandomizedSearchCV(dtc, param_grid, n_iter=100, cv=10, n_jobs=-1, verbose=1, random_state=42)
random_search.fit(X_train_pca, y_train)

# Get the best model from RandomizedSearchCV
best_dtc = random_search.best_estimator_

# Make predictions
y_pred = best_dtc.predict(X_test_pca)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Decision Tree Accuracy after tuning: {accuracy * 100:.2f}%")
