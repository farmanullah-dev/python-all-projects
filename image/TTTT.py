import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as kimage
import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox, scrolledtext
from PIL import Image, ImageTk

# -------------------- CONFIG --------------------
MODEL_PATH = r"F:\python\brain_tumor_model.h5"         # your .h5
TRAIN_DIR = r"F:\python\archive2\Training"            # set to your training folder if available
INPUT_SCALE = '0-1'   # '0-1' => divide by 255, 'minus1-1' => scale to [-1,1] (change if your model used that)
AUG_ROTATIONS = [0, 10, -10]   # augment angles (0 means original)
USE_FLIP = True                # also include horizontal flip
# ------------------------------------------------

# Load model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    messagebox.showerror("Model load error", f"Could not load model at {MODEL_PATH}:\n{e}")
    raise

# Inspect model input shape
# model.input_shape often like (None, 224, 224, 3)
input_shape = model.input_shape
if isinstance(input_shape, list):
    # handle models with multiple inputs - we only handle single input here
    input_shape = input_shape[0]
_, IMG_H, IMG_W, IMG_C = input_shape
print(f"[DEBUG] Model expects input shape HxWxC = {IMG_H}x{IMG_W}x{IMG_C}")

# Get class names in the same order used during training.
def get_class_names_from_training_dir(train_dir):
    if not os.path.isdir(train_dir):
        return None
    # flow_from_directory sorts classes by folder name by default
    folders = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    if not folders:
        return None
    folders_sorted = sorted(folders)
    return folders_sorted

class_names = get_class_names_from_training_dir(TRAIN_DIR)
if class_names is None:
    # fallback (original order you used before) — adjust if you know the correct order
    class_names = ['glioma', 'meningioma', 'no_tumor', 'pituitary']
    print("[DEBUG] Could not read training dir; falling back to default class order.")
else:
    print(f"[DEBUG] Class names loaded from training dir: {class_names}")

# Preprocess single PIL-like image array to model input
def preprocess_array(arr):
    # arr is float array shape (H, W, C) in range 0-255 (uint8 usually)
    arr = arr.astype('float32')
    if INPUT_SCALE == '0-1':
        arr = arr / 255.0
    elif INPUT_SCALE == 'minus1-1':
        arr = (arr / 127.5) - 1.0
    else:
        raise ValueError("Unknown INPUT_SCALE value")
    return arr

# Create augmented variants for test-time augmentation
def create_augmented_images(img_path):
    pil_img = Image.open(img_path).convert('RGB')  # open as RGB (we will convert later if needed)
    pil_img = pil_img.resize((IMG_W, IMG_H))
    arr = np.array(pil_img)  # shape H,W,3

    variants = []
    meta = []

    for angle in AUG_ROTATIONS:
        if angle == 0:
            candidate = pil_img
        else:
            candidate = pil_img.rotate(angle, resample=Image.BILINEAR, expand=False)
        cand_arr = np.array(candidate)
        variants.append(cand_arr.copy())
        meta.append(f"rot_{angle}")

        if USE_FLIP:
            flipped = candidate.transpose(Image.FLIP_LEFT_RIGHT)
            variants.append(np.array(flipped).copy())
            meta.append(f"rot_{angle}_flip")

    variants = np.array(variants)  # (N, H, W, 3)
    # Convert to grayscale if model expects single channel
    if IMG_C == 1:
        # convert by averaging channels or using luminance
        variants = np.dot(variants[...,:3], [0.2989, 0.5870, 0.1140])  # (N,H,W)
        variants = np.expand_dims(variants, axis=-1)  # (N,H,W,1)
    elif IMG_C == 3:
        # already RGB
        pass
    else:
        # Unexpected channel number - attempt to slice or tile
        if IMG_C < 3:
            # take first channels and expand
            variants = variants[..., :IMG_C]
        else:
            # tile channels
            variants = np.tile(variants[..., :1], (1,1,1,IMG_C))
    # Preprocess each
    variants = np.array([preprocess_array(v) for v in variants])
    return variants, meta

# Predict using the model with TTA and return diagnostics
def predict_with_debug(img_path):
    imgs, meta = create_augmented_images(img_path)
    # model.predict expects batch shape (N, H, W, C)
    preds = model.predict(imgs, verbose=0)  # shape (N, num_classes)
    avg_pred = preds.mean(axis=0)

    # debug prints to console
    print("[DEBUG] Augmented variants:", meta)
    for i, m in enumerate(meta):
        arr = preds[i]
        sorted_idx = np.argsort(arr)[::-1]
        print(f"[DEBUG] Variant {i} ({m}) top3:")
        for j in sorted_idx[:3]:
            print(f"    {class_names[j]}: {arr[j]*100:.2f}%")
    print("[DEBUG] Averaged prediction:")
    for idx, p in enumerate(avg_pred):
        print(f"    {class_names[idx]}: {p*100:.2f}%")

    return preds, avg_pred, meta

# Helper to format results for display
def format_report(preds, avg_pred, meta, top_n=3):
    lines = []
    # show each augmented variant
    for i, m in enumerate(meta):
        arr = preds[i]
        top_idx = np.argsort(arr)[::-1][:top_n]
        line = f"{m}: " + ", ".join([f"{class_names[k]} {arr[k]*100:.2f}%" for k in top_idx])
        lines.append(line)
    # averaged
    lines.append("")
    lines.append("Averaged (final):")
    sorted_avg = np.argsort(avg_pred)[::-1]
    lines.append(", ".join([f"{class_names[k]} {avg_pred[k]*100:.2f}%" for k in sorted_avg[:len(class_names)]]))
    # Top single class
    top0 = sorted_avg[0]
    lines.append(f"\nPredicted class: {class_names[top0]} ({avg_pred[top0]*100:.2f}%)")
    return "\n".join(lines)

# -------------------- Tkinter GUI --------------------
root = tk.Tk()
root.title("Brain Tumor Detection - Robust (TTA & Detect)")
root.geometry("700x750")

title_label = Label(root, text="Brain Tumor Detection (TTA, auto-detect)", font=("Helvetica", 18))
title_label.pack(pady=8)

upload_btn = Button(root, text="Upload Image", font=("Helvetica", 14))
upload_btn.pack(pady=6)

image_label = Label(root)
image_label.pack(pady=6)

report_box = scrolledtext.ScrolledText(root, width=80, height=20, font=("Consolas", 11))
report_box.pack(pady=8)

# Display top probabilities as simple labels
top_label = Label(root, text="", font=("Helvetica", 14))
top_label.pack(pady=6)

def on_upload():
    filepath = filedialog.askopenfilename(filetypes=[("Image files","*.png;*.jpg;*.jpeg;*.bmp"), ("All files","*.*")])
    if not filepath:
        return
    # show image
    pil_img = Image.open(filepath).convert('RGB')
    display_img = pil_img.resize((300,300))
    tkimg = ImageTk.PhotoImage(display_img)
    image_label.config(image=tkimg)
    image_label.image = tkimg

    try:
        preds, avg_pred, meta = predict_with_debug(filepath)
    except Exception as e:
        messagebox.showerror("Prediction error", f"Error during prediction: {e}")
        raise

    report = format_report(preds, avg_pred, meta, top_n=3)
    report_box.delete('1.0', tk.END)
    report_box.insert(tk.END, report)

    # show top class prominently
    top_idx = np.argmax(avg_pred)
    top_label.config(text=f"Prediction: {class_names[top_idx]}  —  Confidence {avg_pred[top_idx]*100:.2f}%", fg="blue")

upload_btn.config(command=on_upload)

# Run
root.mainloop()
