import os
import colorama
colorama.init(autoreset=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore

# Define directories
train_dir = r"F:\\python\\Bird Speciees Dataset"  # Main dataset folder path
test_dir = r"F:\\python\\Bird Speciees Dataset"  # Can be the same as training or separate

# Define ImageDataGenerators
train_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load training images
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),  # Resize to match input size for CNN
    batch_size=32,
    class_mode='categorical'  # Use 'categorical' for multiple classes
)

# Load testing images (use a separate test folder if available)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'  # Same for testing
)

# CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')  # 4 classes: Flamingo, Downy Woodpecker, Carmine Bee-Eater, American Goldfinch
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(train_generator, epochs=10, validation_data=test_generator)
