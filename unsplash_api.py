import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from io import BytesIO

# --- Your Unsplash API Key ---
ACCESS_KEY = "z7WXqdYAbQl4w0X_YxX_z8fMdlNcuB7CGENpqkMs7-s"

# --- Download & Save Image ---
def save_image(img_url, author):
    try:
        img_data = requests.get(img_url).content
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
            initialfile=f"{author}_unsplash.jpg",
            title="Save Image As"
        )
        if file_path:
            with open(file_path, "wb") as f:
                f.write(img_data)
            messagebox.showinfo("Success", f"Image saved successfully:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image.\n{e}")


# --- Fetch images from Unsplash ---
def fetch_images():
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a topic to search!")
        return

    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=15&client_id={ACCESS_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Error", "Unable to fetch images. Please try again later.")
        return

    data = response.json()
    photos = data.get("results", [])

    if not photos:
        messagebox.showinfo("No Results", "No images found for that topic.")
        return

    # Clear previous images
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for photo in photos:
        img_url = photo["urls"]["regular"]
        author = photo["user"]["name"]
        likes = photo["likes"]

        try:
            img_data = requests.get(photo["urls"]["small"]).content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((300, 200))
            photo_img = ImageTk.PhotoImage(img)

            # --- Stylish Card ---
            card = tk.Frame(scrollable_frame, bg="#25273D", bd=0, relief="flat",
                            highlightbackground="#3B3F5C", highlightthickness=1)
            card.pack(padx=15, pady=12, fill="x")

            img_label = tk.Label(card, image=photo_img, bg="#25273D")
            img_label.image = photo_img
            img_label.pack(padx=10, pady=10)

            info_text = f"📸 {author}\n❤️ {likes} Likes"
            tk.Label(card, text=info_text, font=("Segoe UI", 10), fg="#DADADA", bg="#25273D").pack(pady=(0, 6))

            # --- Save Button ---
            save_btn = tk.Button(
                card,
                text="💾 Save Image",
                command=lambda url=img_url, a=author: save_image(url, a),
                font=("Segoe UI", 10, "bold"),
                bg="#00BFA6",
                fg="white",
                activebackground="#00E6B8",
                relief="flat",
                padx=8,
                pady=4
            )
            save_btn.pack(pady=(0, 10))

        except Exception:
            continue


# --- GUI Setup ---
root = tk.Tk()
root.title("📷 Unsplash Image Explorer")
root.geometry("780x680")
root.config(bg="#1A1B26")

# --- Gradient Header ---
header = tk.Canvas(root, width=780, height=100, bg="#1A1B26", highlightthickness=0)
header.pack()
for i in range(100):
    color = f'#{30+i:02x}{10+i//2:02x}{80+i:02x}'
    header.create_rectangle(0, i, 780, i+1, outline="", fill=color)
header.create_text(390, 50, text="Unsplash Image Explorer 🌅", fill="white", font=("Segoe UI", 22, "bold"))

# --- Search Frame ---
search_frame = tk.Frame(root, bg="#1A1B26")
search_frame.pack(pady=15)

search_entry = tk.Entry(search_frame, width=35, font=("Segoe UI", 14), bg="#2C2F48", fg="white",
                        relief="flat", insertbackground="white")
search_entry.grid(row=0, column=0, padx=10, ipady=6)

search_btn = tk.Button(
    search_frame,
    text="🔍 Search",
    command=fetch_images,
    font=("Segoe UI", 12, "bold"),
    bg="#7C3AED",
    fg="white",
    activebackground="#9F7AEA",
    relief="flat",
    padx=12,
    pady=5
)
search_btn.grid(row=0, column=1, padx=8)

# --- Scrollable Frame ---
canvas = tk.Canvas(root, bg="#1A1B26", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1A1B26")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=10)
scrollbar.pack(side="right", fill="y")

footer = tk.Label(root, text="Made with ❤️ using Unsplash API", bg="#1A1B26", fg="#777", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=10)

root.mainloop()
