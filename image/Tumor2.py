
import os
import colorama


colorama.init(autoreset=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging




import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

# Define directories
train_dir = r"F:\\python\\archive2\\Training"
test_dir = r"F:\\python\\archive2\\Testing"

# Define ImageDataGenerators
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Load training images
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),  # Adjust based on the image size
    batch_size=32,
    class_mode='categorical'  # Use 'categorical' for multiple classes
)

# Load testing images
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'  # Same for testing
)

# Display a batch of images
def display_images(generator, num_images=9):
    images, labels = next(generator)  # Get the next batch of images and labels
    plt.figure(figsize=(10, 10))
    
    for i in range(num_images):
        plt.subplot(3, 3, i + 1)  # Create a subplot
        plt.imshow(images[i])  # Display the image
        plt.title(np.argmax(labels[i]))  # Show the class label
        plt.axis('off')  # Turn off axis

    plt.tight_layout()
    plt.show()

# Display images from the training set
display_images(train_generator)

# CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.BatchNormalization(), 
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(224, 224, 3)), 
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', input_shape=(224, 224, 3)),  # Adjusted input shape
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (5, 5), activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(4, activation='softmax') 
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(train_generator, epochs=20, validation_data=test_generator)
