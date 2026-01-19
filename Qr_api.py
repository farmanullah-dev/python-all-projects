import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# --- Function to generate QR code ---
def generate_qr():
    text = entry_text.get().strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter text or a link!")
        return

    # Free QR API endpoint
    url = f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=200x200"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            qr_img = ImageTk.PhotoImage(img)
            label_qr.config(image=qr_img)
            label_qr.image = qr_img  # keep reference
        else:
            messagebox.showerror("Error", "Failed to generate QR code!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Save QR image ---
def save_qr():
    text = entry_text.get().strip()
    if not text:
        messagebox.showwarning("Input Error", "Please generate a QR code first!")
        return

    try:
        response = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=500x500")
        if response.status_code == 200:
            with open("Generated_QR.png", "wb") as f:
                f.write(response.content)
            messagebox.showinfo("Saved", "✅ QR code saved as 'Generated_QR.png'")
        else:
            messagebox.showerror("Error", "Failed to save QR code!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("🔲 QR Code Generator")
root.geometry("600x500")
root.config(bg="#0F172A")

# --- Title ---
lbl_title = tk.Label(root, text="🔳 QR Code Generator", font=("Segoe UI", 22, "bold"), fg="#38BDF8", bg="#0F172A")
lbl_title.pack(pady=20)

# --- Input Frame ---
frame = tk.Frame(root, bg="#1E293B", bd=2, relief=tk.RIDGE)
frame.pack(pady=15)

entry_text = tk.Entry(frame, font=("Segoe UI", 16), width=30, bg="#334155", fg="white", insertbackground="white", relief=tk.FLAT)
entry_text.pack(side=tk.LEFT, padx=10, pady=10)

btn_generate = tk.Button(frame, text="Generate", font=("Segoe UI", 13, "bold"), bg="#38BDF8", fg="white", relief=tk.FLAT, command=generate_qr)
btn_generate.pack(side=tk.RIGHT, padx=10, pady=10)

# --- QR Display ---
label_qr = tk.Label(root, bg="#0F172A")
label_qr.pack(pady=30)

# --- Save Button ---
btn_save = tk.Button(root, text="💾 Save QR", font=("Segoe UI", 14, "bold"), bg="#22C55E", fg="white", relief=tk.FLAT, command=save_qr)
btn_save.pack(pady=10)

# --- Footer ---
lbl_footer = tk.Label(root, text="Made with 💙 using goQR API", font=("Segoe UI", 10), fg="#94A3B8", bg="#0F172A")
lbl_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
