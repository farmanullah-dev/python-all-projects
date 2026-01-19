import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# --- Function to get country info ---
def get_country_info():
    country_name = entry.get().strip()
    if not country_name:
        messagebox.showwarning("Input Error", "Please enter a country name!")
        return

    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Error", "Country not found. Please try again.")
        return

    data = response.json()[0]
    display_country_info(data)

# --- Function to display info ---
def display_country_info(data):
    for widget in info_frame.winfo_children():
        widget.destroy()

    # --- Flag Image ---
    flag_url = data.get("flags", {}).get("png")
    if flag_url:
        flag_response = requests.get(flag_url)
        img_data = flag_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 120))
        photo = ImageTk.PhotoImage(img)

        flag_label = tk.Label(info_frame, image=photo, bg="#1E1E2E")
        flag_label.image = photo
        flag_label.pack(pady=(10, 20))

    # --- Info Text ---
    name = data.get("name", {}).get("common", "Unknown")
    capital = data.get("capital", ["N/A"])[0]
    region = data.get("region", "N/A")
    subregion = data.get("subregion", "N/A")
    population = data.get("population", "N/A")
    currency = ", ".join([c["name"] for c in data.get("currencies", {}).values()]) if data.get("currencies") else "N/A"
    language = ", ".join(data.get("languages", {}).values()) if data.get("languages") else "N/A"

    text = (
        f"🏴 Country: {name}\n"
        f"🏙️ Capital: {capital}\n"
        f"🌍 Region: {region} ({subregion})\n"
        f"👥 Population: {population:,}\n"
        f"💰 Currency: {currency}\n"
        f"💬 Languages: {language}\n"
    )

    info_label = tk.Label(
        info_frame,
        text=text,
        justify="left",
        font=("Segoe UI", 12),
        fg="#FFFFFF",
        bg="#1E1E2E",
        wraplength=450
    )
    info_label.pack(pady=(5, 10))


# --- Main GUI Window ---
root = tk.Tk()
root.title("🌎 REST Countries Explorer")
root.geometry("550x650")
root.config(bg="#0F1021")

# --- Gradient Header ---
header = tk.Canvas(root, width=550, height=100, bg="#0F1021", highlightthickness=0)
header.pack()
for i in range(100):
    r = 15 + i
    g = 15
    b = 40 + i
    color = f'#{r:02x}{g:02x}{b:02x}'
    header.create_rectangle(0, i, 550, i+1, outline="", fill=color)

header.create_text(275, 50, text="🌍 Country Info App", fill="white", font=("Segoe UI", 20, "bold"))

# --- Search Frame ---
search_frame = tk.Frame(root, bg="#0F1021")
search_frame.pack(pady=20)

entry = tk.Entry(search_frame, width=28, font=("Segoe UI", 14), bg="#2E2F4F", fg="white", relief="flat", insertbackground="white")
entry.grid(row=0, column=0, padx=10, ipady=6)

search_btn = tk.Button(
    search_frame,
    text="🔍 Search",
    command=get_country_info,
    font=("Segoe UI", 12, "bold"),
    bg="#8A2BE2",
    fg="white",
    activebackground="#A569BD",
    relief="flat",
    padx=10,
    pady=5
)
search_btn.grid(row=0, column=1, padx=10)

# --- Info Display Frame ---
info_frame = tk.Frame(root, bg="#1E1E2E", bd=0, relief="groove")
info_frame.pack(padx=20, pady=20, fill="both", expand=True)

footer = tk.Label(root, text="Made with ❤️ using REST Countries API", bg="#0F1021", fg="#888", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=10)

root.mainloop()
