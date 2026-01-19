import requests
import tkinter as tk
from tkinter import messagebox

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    try:
        response = requests.get(url)
        data = response.json()

        if data["type"] == "single":
            joke_text = data["joke"]
        elif data["type"] == "twopart":
            joke_text = f"{data['setup']}\n\n{data['delivery']}"
        else:
            joke_text = "Couldn't fetch a joke right now!"
        
        joke_label.config(text=joke_text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load joke: {e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("😂 Random Joke Generator")
root.geometry("500x300")
root.config(bg="#FFFACD")

tk.Label(root, text="Click to Get a Joke!", font=("Arial", 16, "bold"), bg="#FFFACD").pack(pady=10)
tk.Button(root, text="🎭 Get Joke", command=get_joke, bg="#FFD700", fg="black", font=("Arial", 14)).pack(pady=10)

joke_label = tk.Label(root, text="", wraplength=450, justify="center", bg="#FFFACD", font=("Arial", 12))
joke_label.pack(pady=20)

root.mainloop()
