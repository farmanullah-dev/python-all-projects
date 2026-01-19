import os
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight

# Path to the Bird Species Dataset
data_path = "F:\\python\\Bird Speciees Dataset"
class_names = os.listdir(data_path)
class_names.sort()

# Create a list of all the images and their corresponding labels
images = []
labels = []
for class_name in class_names:
    class_path = os.path.join(data_path, class_name)
    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)
        img = Image.open(img_path)
        img = img.resize((224, 224))  # Resize to match the model's input size
        img = np.array(img)
        images.append(img)
        labels.append(class_name)  # Label each image with its class name

# Convert the list of images to a numpy array
images = np.array(images)

# Encode the labels
le = LabelEncoder()
labels = le.fit_transform(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Apply PCA to reduce the dimensionality of the data
pca = PCA(n_components=150)  # Increase components for better performance
X_train = pca.fit_transform(X_train.reshape(X_train.shape[0], -1))  # Flatten the images for PCA
X_test = pca.transform(X_test.reshape(X_test.shape[0], -1))

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Compute class weights (useful if data is imbalanced)
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(zip(np.unique(y_train), class_weights))

# Define the random forest classifier
rfc = RandomForestClassifier(n_estimators=500, random_state=42, max_depth=20, class_weight='balanced')

# Define the hyperparameters to tune
param_dist = {
    "n_estimators": [200, 300, 400, 500],
    "max_depth": [10, 20, 30, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "bootstrap": [True, False],
    "criterion": ["gini", "entropy"]
}

# Define the randomized search cross-validation
rs = RandomizedSearchCV(rfc, param_distributions=param_dist, n_iter=20, cv=5, random_state=42, n_jobs=-1)

# Fit the randomized search cross-validation to the training data
rs.fit(X_train, y_train)

# Print the best hyperparameters
print("Best hyperparameters:", rs.best_params_)

# Use the best hyperparameters to train the random forest classifier
rfc = RandomForestClassifier(**rs.best_params_, random_state=42, class_weight='balanced')
rfc.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rfc.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(f"Overall Accuracy: {accuracy * 100:.2f}%")

# Print the classification report
print(classification_report(y_test, y_pred, target_names=class_names))
