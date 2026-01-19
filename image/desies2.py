

import tensorflow as tf
import pandas as pd
import os
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.utils import class_weight
import numpy as np

# ---------------------------
# 1. Data Loading and Preparation
# ---------------------------

# Path to your root folder containing the subfolders 'Normal' and 'Tuberculosis'
data_dir = r"F:\\python\\archive\\TB_Chest_Radiography_Database"

# Paths to the Excel metadata files
normal_metadata_csv = os.path.join(data_dir, 'Normal.metadata.xlsx')
tuberculosis_metadata_csv = os.path.join(data_dir, 'Tuberculosis.metadata.xlsx')

# Check if the Excel files exist
if not os.path.isfile(normal_metadata_csv):
    print(f"File not found: {normal_metadata_csv}")

if not os.path.isfile(tuberculosis_metadata_csv):
    print(f"File not found: {tuberculosis_metadata_csv}")

# Load Excel files using pandas if they exist
def load_xlsx(xlsx_path):
    return pd.read_excel(xlsx_path)  # Load Excel file

# Load the metadata from Excel files
normal_metadata = load_xlsx(normal_metadata_csv) if os.path.isfile(normal_metadata_csv) else None
tuberculosis_metadata = load_xlsx(tuberculosis_metadata_csv) if os.path.isfile(tuberculosis_metadata_csv) else None

if normal_metadata is not None:
    print("Normal Metadata:")
    print(normal_metadata.head())
else:
    print("No Normal Metadata loaded.")

if tuberculosis_metadata is not None:
    print("Tuberculosis Metadata:")
    print(tuberculosis_metadata.head())
else:
    print("No Tuberculosis Metadata loaded.")

# Parameters
batch_size = 32
img_size = (224, 224)  # Adjust the image size as needed
validation_split = 0.2  # 20% for validation
seed = 123  # For reproducibility

# Load dataset from directory with training and validation splits
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=validation_split,
    subset="training",
    seed=seed,
    image_size=img_size,
    batch_size=batch_size,
    label_mode='int',  # 'int' for integer labels
    shuffle=True
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=validation_split,
    subset="validation",
    seed=seed,
    image_size=img_size,
    batch_size=batch_size,
    label_mode='int',
    shuffle=True
)

# Check the classes assigned based on folder names
class_names = train_ds.class_names
print("Class Names:", class_names)

# Prefetching for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# ---------------------------
# 2. Data Augmentation
# ---------------------------

# Define data augmentation layers
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# (Optional) Visualize some augmented images
plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    augmented_images = data_augmentation(images)
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(augmented_images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")
plt.show()

# ---------------------------
# 3. Model Building with Custom CNN
# ---------------------------

# Build your custom model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)),  # Adjust input shape
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # Single output for binary classification
])

model.summary()

# ---------------------------
# 4. Model Compilation
# ---------------------------

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',  # Use this for binary classification
    metrics=['accuracy']
)

# ---------------------------
# 5. Handling Class Imbalance (Optional)
# ---------------------------

# Compute class weights to handle class imbalance
labels = []
for _, label_batch in train_ds:
    labels.extend(label_batch.numpy())

class_weights_values = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = dict(enumerate(class_weights_values))
print("Class Weights:", class_weights)

# ---------------------------
# 6. Model Training
# ---------------------------

# Define callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
checkpoint_path = "best_model.keras"  # Change .h5 to .keras
model_checkpoint = ModelCheckpoint(
    filepath=checkpoint_path,
    monitor='val_loss',
    save_best_only=True
)

# Train the model
epochs = 10  # You can increase this as needed
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[early_stopping, model_checkpoint],
    class_weight=class_weights  # Include if using class weights
)

# ---------------------------
# 7. Model Evaluation
# ---------------------------

# Load the best model
model.load_weights(checkpoint_path)

# Evaluate the model
loss, accuracy = model.evaluate(val_ds)
print(f"Validation Loss: {loss:.4f}", flush=True)
print(f"Validation Accuracy: {accuracy:.4f}", flush=True)

# ---------------------------
# 8. Print Accuracy at Each Epoch
# ---------------------------

# Print accuracy at each epoch
for epoch in range(epochs):
    print(f"Epoch {epoch + 1}:")
    print(f"  Training Accuracy: {history.history['accuracy'][epoch]:.4f}", flush=True)
    print(f"  Validation Accuracy: {history.history['val_accuracy'][epoch]:.4f}", flush=True)

# ---------------------------
# 9. Visualizing Training History
# ---------------------------

# Plot training and validation accuracy and loss
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss_history = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(12, 6))

# Accuracy Plot
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

# Loss Plot
plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss_history, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.show()

# ---------------------------
# 10. Saving the Final Model
# ---------------------------

# Save the final model
model.save('tb_classification_model.keras')  # Change to .keras format
print("Model saved as tb_classification_model.keras", flush=True)

# ---------------------------
# 11. Model Inference: Making Predictions on New Data
# ---------------------------

# Function to load and preprocess a single image
def load_and_preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(
        image_path, target_size=img_size
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

# Function to predict a single image
def predict_image(image_path, model):
    img = load_and_preprocess_image(image_path)
    prediction = model.predict(img)
    score = prediction[0]
    if score >= 0.5:
        label = 'Tuberculosis'
        confidence = score
    else:
        label = 'Normal'
        confidence = 1 - score
    return label, confidence

# Example usage
example_image_path = r"F:\\python\\archive\\TB_Chest_Radiography_Database\\Normal\\normal_image.png"  # Full path to the image file
predicted_label, confidence = predict_image(example_image_path, model)
print(f"Predicted label: {predicted_label}, Confidence: {confidence:.4f}", flush=True)

  # Full path to the image file
example_image_path = r"F:\\python\\archive\\TB_Chest_Radiography_Database\\Tuberculosis\\tuberculosis_image.png"
predicted_label, confidence = predict_image(example_image_path, model)
print(f"Predicted label: {predicted_label}, Confidence: {confidence:.4f}", flush=True)
