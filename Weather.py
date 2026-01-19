import requests
import tkinter as tk
from tkinter import messagebox

# --- Your OpenWeatherMap API key ---
API_KEY = "0d1a32d338b6582ca943387893b7f865"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        result = (
            f"🌍 City: {data['name']}, {data['sys']['country']}\n\n"
            f"🌡 Temperature: {data['main']['temp']}°C\n"
            f"🤗 Feels Like: {data['main']['feels_like']}°C\n"
            f"💧 Humidity: {data['main']['humidity']}%\n"
            f"🌤 Weather: {data['weather'][0]['description'].title()}"
        )
        result_label.config(text=result, fg="#1A237E")
    else:
        messagebox.showerror("Error", data.get("message", "Something went wrong!"))

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App")
root.geometry("460x360")
root.config(bg="#D6EAF8")

# --- Heading ---
heading = tk.Label(
    root,
    text="🌞 Welcome! Check Your City Weather 🌧️",
    bg="#5DADE2",
    fg="white",
    font=("Helvetica", 16, "bold"),
    pady=15
)
heading.pack(fill="x")

# --- Input section ---
tk.Label(
    root,
    text="Enter your city name below 👇",
    bg="#D6EAF8",
    fg="#154360",
    font=("Arial", 12, "bold")
).pack(pady=(20, 5))

city_entry = tk.Entry(root, width=30, font=("Arial", 13), justify="center", relief="solid", bd=1)
city_entry.pack(pady=5)

tk.Button(
    root,
    text="Get Weather ☁️",
    command=get_weather,
    bg="#2E86C1",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    padx=10,
    pady=5,
    cursor="hand2"
).pack(pady=10)

# --- Result section ---
result_label = tk.Label(
    root,
    text="",
    bg="#D6EAF8",
    fg="#1A237E",
    font=("Calibri", 12),
    justify="left",
    padx=10,
    pady=10
)
result_label.pack(pady=10)

# --- Footer ---
footer = tk.Label(
    root,
    text="Powered by OpenWeatherMap API",
    bg="#D6EAF8",
    fg="#424949",
    font=("Arial", 9, "italic")
)
footer.pack(side="bottom", pady=10)

root.mainloop()
