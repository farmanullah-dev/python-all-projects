import os
import numpy as np
import pandas as pd
from collections import Counter
from tkinter import Tk, filedialog, Button, Label, Frame, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model # type: ignore

# ------------------------------
# 1) Load saved model
# ------------------------------
model_path = r"F:\python\Heartbeat\heartbeat_model.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}")

model = load_model(model_path)
print("Model loaded successfully!")

# ------------------------------
# 2) Class mapping and colors
# ------------------------------
class_mapping = {
    0: "Normal",
    1: "Supraventricular Premature Beat (SPB)",
    2: "Premature Ventricular Contraction (PVC)",
    3: "Fusion Beat",
    4: "Unknown / Q Beat"
}

color_mapping = {
    "Normal": "green",
    "SPB": "red",
    "PVC": "red",
    "Fusion Beat": "red",
    "Unknown / Q Beat": "yellow"
}

# ------------------------------
# 3) Preprocess ECG data function
# ------------------------------
def preprocess_ecg(file_path):
    df = pd.read_csv(file_path)
    X = df.values  # Assuming last column is label, ignore if predicting new ECG
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))
    return X_scaled

# ------------------------------
# 4) Prediction function
# ------------------------------
def predict_ecg(file_path):
    try:
        X_new = preprocess_ecg(file_path)
        preds = model.predict(X_new)
        predicted_classes = np.argmax(preds, axis=1)
        readable_pred = [class_mapping[c] for c in predicted_classes]
        counts = Counter(readable_pred)
        total_beats = sum(counts.values())
        percentages = {k: round(v / total_beats * 100, 2) for k, v in counts.items()}
        return counts, percentages
    except Exception as e:
        messagebox.showerror("Error", f"Failed to predict ECG: {e}")
        return None, None

# ------------------------------
# 5) Display results in GUI
# ------------------------------
def analyze_file():
    file_path = filedialog.askopenfilename(title="Select ECG CSV File", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    counts, percentages = predict_ecg(file_path)
    if counts is None:
        return

    # Clear previous chart
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Pie chart
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = [color_mapping.get(l, "gray") for l in labels]

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Summary text
    summary_text = ""
    for k, v in counts.items():
        summary_text += f"{k}: {v} beats ({percentages[k]}%)\n"

    summary_label.config(text=summary_text)

    # Warning
    abnormal_beats = sum([v for k, v in counts.items() if k != "Normal"])
    if abnormal_beats / sum(counts.values()) > 0.10:  # Threshold 10%
        warning_label.config(text="⚠️ High number of abnormal heartbeats detected! Consult a doctor.", fg="red")
    else:
        warning_label.config(text="✅ Most heartbeats are normal.", fg="green")

# ------------------------------
# 6) GUI Setup
# ------------------------------
root = Tk()
root.title("ECG Heartbeat Dashboard")
root.geometry("700x600")

# Instructions
Label(root, text="Step 1: Upload ECG CSV file.\nStep 2: Click Analyze.\nStep 3: View heartbeat summary and chart.", font=("Arial", 12)).pack(pady=10)

# Analyze button
Button(root, text="Analyze ECG", command=analyze_file, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

# Summary frame
summary_label = Label(root, text="", font=("Arial", 12), justify="left")
summary_label.pack(pady=10)

# Warning label
warning_label = Label(root, text="", font=("Arial", 12))
warning_label.pack(pady=5)

# Chart frame
chart_frame = Frame(root)
chart_frame.pack(pady=10)

root.mainloop()
