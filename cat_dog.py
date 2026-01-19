import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --- API Functions ---
def get_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    data = response.json()
    return data[0]["url"]

def get_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = response.json()
    return data["message"]

# --- Show Image in GUI ---
def show_image(api_func):
    global current_image
    try:
        img_url = api_func()
        response = requests.get(img_url)
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((300, 300))
        img = ImageTk.PhotoImage(img_data)

        image_label.config(image=img)
        image_label.image = img
        current_image = img_data
        info_label.config(text=f"Loaded from:\n{img_url}")
    except Exception as e:
        image_label.config(text=f"Error loading image: {e}")
        current_image = None

# --- Save Image Function ---
def save_image():
    if current_image is None:
        messagebox.showwarning("No Image", "Please load a cat or dog image first!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
    )

    if file_path:
        current_image.save(file_path)
        messagebox.showinfo("Saved", f"✅ Image saved successfully at:\n{file_path}")

# --- GUI Setup ---
root = tk.Tk()
root.title("🐾 Cat & Dog Image Viewer")
root.geometry("450x500")
root.config(bg="#F7EFE5")

current_image = None

tk.Label(root, text="Click a Button to See an Image", font=("Arial", 15, "bold"), bg="#F7EFE5").pack(pady=10)

btn_frame = tk.Frame(root, bg="#F7EFE5")
btn_frame.pack()

tk.Button(btn_frame, text="🐱 Show Cat", command=lambda: show_image(get_cat_image),
          bg="#E3A5C7", font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🐶 Show Dog", command=lambda: show_image(get_dog_image),
          bg="#A8D5BA", font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)

image_label = tk.Label(root, bg="#F7EFE5")
image_label.pack(pady=20)

tk.Button(root, text="💾 Save Image", command=save_image,
          bg="#FFD700", font=("Arial", 12, "bold")).pack(pady=10)

info_label = tk.Label(root, text="", bg="#F7EFE5", font=("Arial", 9), wraplength=400, justify="center")
info_label.pack(pady=10)

root.mainloop()
