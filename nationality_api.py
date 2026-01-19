import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# --- Function to predict nationality ---
def predict_nationality():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name!")
        return

    url = f"https://api.nationalize.io/?name={name}"

    try:
        response = requests.get(url)
        data = response.json()

        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)

        countries = data.get("country", [])
        if not countries:
            result_box.insert(tk.END, "❌ No nationality data found.\n", "error")
            result_box.config(state=tk.DISABLED)
            return

        result_box.insert(tk.END, f"🌍 Predictions for '{name}':\n\n", "title")

        for c in countries[:3]:  # Top 3 predictions
            code = c.get("country_id")
            prob = round(c.get("probability", 0) * 100, 2)
            flag_url = f"https://flagsapi.com/{code}/flat/64.png"

            # Insert text info
            result_box.insert(tk.END, f"🏳️ Country Code: {code}\n", "country")
            result_box.insert(tk.END, f"📊 Probability: {prob}%\n", "prob")

            # Insert flag image
            try:
                flag_img_data = requests.get(flag_url).content
                flag_img = Image.open(BytesIO(flag_img_data))
                flag_img = flag_img.resize((80, 50))
                flag_photo = ImageTk.PhotoImage(flag_img)
                flag_images.append(flag_photo)
                result_box.image_create(tk.END, image=flag_photo)
                result_box.insert(tk.END, "\n\n")
            except:
                result_box.insert(tk.END, "🚫 Flag not available\n\n")

        result_box.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# --- GUI Setup ---
root = tk.Tk()
root.title("🌎 Nationality Predictor (Nationalize.io)")
root.geometry("650x600")
root.config(bg="#0F172A")

flag_images = []

# --- Title ---
lbl_title = tk.Label(root, text="🌍 Nationality Predictor", font=("Segoe UI", 22, "bold"), fg="#38BDF8", bg="#0F172A")
lbl_title.pack(pady=25)

# --- Input Frame ---
frame = tk.Frame(root, bg="#1E293B", bd=2, relief=tk.RIDGE)
frame.pack(pady=10)

entry_name = tk.Entry(frame, font=("Segoe UI", 16), width=25, bg="#334155", fg="white", relief=tk.FLAT, insertbackground="white")
entry_name.pack(side=tk.LEFT, padx=10, pady=10)

btn_predict = tk.Button(frame, text="Predict", font=("Segoe UI", 13, "bold"), bg="#38BDF8", fg="white", relief=tk.FLAT, command=predict_nationality)
btn_predict.pack(side=tk.RIGHT, padx=10, pady=10)

# --- Result Box ---
result_box = tk.Text(root, wrap=tk.WORD, font=("Segoe UI", 13), width=70, height=20, bg="#1E293B", fg="white", relief=tk.FLAT)
result_box.pack(padx=20, pady=20)
result_box.tag_config("title", foreground="#FACC15", font=("Segoe UI", 14, "bold"))
result_box.tag_config("country", foreground="#93C5FD", font=("Segoe UI", 12, "bold"))
result_box.tag_config("prob", foreground="#86EFAC", font=("Segoe UI", 12))
result_box.tag_config("error", foreground="#F87171", font=("Segoe UI", 13))
result_box.config(state=tk.DISABLED)

# --- Footer ---
lbl_footer = tk.Label(root, text="🔗 Powered by Nationalize.io API", font=("Segoe UI", 10), fg="#94A3B8", bg="#0F172A")
lbl_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
