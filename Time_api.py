import requests
import tkinter as tk
from tkinter import ttk, messagebox

def get_time():
    region = region_box.get()
    if not region:
        messagebox.showwarning("Input Error", "Please select a region!")
        return

    url = f"https://worldtimeapi.org/api/timezone/{region}"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            date = data["datetime"][:10]
            time = data["datetime"][11:19]
            utc_offset = data["utc_offset"]

            result_label.config(
                text=f"📍 Region: {region}\n📅 Date: {date}\n⏰ Time: {time}\nUTC Offset: {utc_offset}"
            )
        else:
            messagebox.showerror("Error", data.get("error", "Something went wrong!"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load time data: {e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("🕒 Time & Date App")
root.geometry("400x300")
root.config(bg="#E8F1F2")

tk.Label(root, text="Select a Region", font=("Arial", 13, "bold"), bg="#E8F1F2").pack(pady=10)

# Dropdown list of some popular time zones
regions = [
    "Asia/Karachi", "Asia/Tokyo", "Asia/Dubai", "Asia/Kolkata",
    "Europe/London", "Europe/Paris", "America/New_York", "America/Los_Angeles",
    "Australia/Sydney", "Africa/Cairo"
]

region_box = ttk.Combobox(root, values=regions, font=("Arial", 11))
region_box.set("Asia/Karachi")
region_box.pack(pady=5)

tk.Button(root, text="Get Time", command=get_time, bg="#0077B6", fg="white",
          font=("Arial", 12)).pack(pady=10)

result_label = tk.Label(root, text="", bg="#E8F1F2", font=("Arial", 12), justify="left")
result_label.pack(pady=20)

root.mainloop()
