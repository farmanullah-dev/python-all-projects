import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

# Load your trained model
model_path = r"F:\python\brain_tumor_model.h5"  # Updated path
model = tf.keras.models.load_model(model_path)

# Define classes (must match the order used in your training)
classes = ['glioma', 'meningioma', 'no_tumor', 'pituitary']

# Function to predict image
def predict_image(file_path):
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = classes[np.argmax(predictions)]
    confidence = predictions[0][np.argmax(predictions)]

    confidence_report = "\n".join([f"{classes[i]}: {predictions[0][i]*100:.2f}%" for i in range(len(classes))])
    
    result_label.config(text=f"Tumor Type: {predicted_class}\nConfidence: {confidence*100:.2f}%\n\nFull Report:\n{confidence_report}")

# Function to open file dialog
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the image in GUI
        img = Image.open(file_path)
        img = img.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Predict tumor type
        predict_image(file_path)


root = tk.Tk()
root.title("Brain Tumor Detection")
root.geometry("500x600")

title_label = Label(root, text="Brain Tumor Detection", font=("Helvetica", 20))
title_label.pack(pady=10)

upload_btn = Button(root, text="Upload Image", command=upload_image, font=("Helvetica", 14))
upload_btn.pack(pady=10)

image_label = Label(root)
image_label.pack(pady=10)

result_label = Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
