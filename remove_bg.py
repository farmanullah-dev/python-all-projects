import requests
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io

API_KEY = "5F8puy3gyS3G5aMHJ8pF9gCs"

def remove_bg():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    if not file_path:
        return

    with open(file_path, "rb") as img_file:
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": img_file},
            data={"size": "auto"},
            headers={"X-Api-Key": API_KEY},
        )

    if response.status_code == 200:
        output_path = file_path.rsplit(".", 1)[0] + "_no_bg.png"
        with open(output_path, "wb") as out:
            out.write(response.content)

        img_data = Image.open(io.BytesIO(response.content))
        img_data.thumbnail((300, 300))
        img_preview = ImageTk.PhotoImage(img_data)

        preview_label.config(image=img_preview)
        preview_label.image = img_preview

        messagebox.showinfo("Success ✅", f"Background removed!\nSaved as: {output_path}")
    else:
        messagebox.showerror("Error ❌", response.text)

# --- GUI ---
root = Tk()
root.title("🪄 Background Remover")
root.geometry("400x500")
root.config(bg="#1C1C2E")

Label(root, text="🪄 Remove Background API", font=("Arial", 16, "bold"), bg="#1C1C2E", fg="#FFD700").pack(pady=20)
Button(root, text="🖼️ Choose Image & Remove BG", command=remove_bg,
       font=("Arial", 13, "bold"), bg="#FFD700", fg="black", relief=FLAT, padx=10, pady=5).pack(pady=20)

preview_label = Label(root, bg="#1C1C2E")
preview_label.pack(pady=20)

Label(root, text="Powered by remove.bg API", bg="#1C1C2E", fg="gray").pack(side="bottom", pady=10)

root.mainloop()
