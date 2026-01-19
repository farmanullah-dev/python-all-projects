import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# --- Replace with your OMDb API key ---
API_KEY = "6981d9d7"

def get_movie_info():
    movie_name = movie_entry.get()
    if not movie_name:
        messagebox.showwarning("Warning", "Please enter a movie name!")
        return

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        title_label.config(text=f"🎬 {data['Title']} ({data['Year']})", fg="#FFD700")
        genre_label.config(text=f"🎭 Genre: {data['Genre']}")
        rating_label.config(text=f"⭐ IMDb Rating: {data['imdbRating']}")
        plot_label.config(text=f"📝 Plot: {data['Plot']}", wraplength=400, justify=LEFT)

        # Load poster image
        if data["Poster"] != "N/A":
            img_data = requests.get(data["Poster"]).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((200, 300))
            poster_img = ImageTk.PhotoImage(img)
            poster_label.config(image=poster_img)
            poster_label.image = poster_img
        else:
            poster_label.config(image="", text="No Poster Available")
    else:
        messagebox.showerror("Error", "Movie not found!")

# --- GUI Setup ---
root = Tk()
root.title("🎥 Movie Info App")
root.geometry("700x500")
root.config(bg="#1C1C1C")

Label(root, text="🎞 Enter Movie Name:", font=("Arial", 14, "bold"), bg="#1C1C1C", fg="#FFFFFF").pack(pady=10)
movie_entry = Entry(root, font=("Arial", 14), width=30)
movie_entry.pack(pady=5)

Button(root, text="🔍 Search Movie", command=get_movie_info, bg="#FFD700", fg="black",
       font=("Arial", 12, "bold"), relief=FLAT, padx=10, pady=5).pack(pady=10)

# Movie Info Labels
title_label = Label(root, text="", font=("Arial", 16, "bold"), bg="#1C1C1C", fg="#FFD700")
title_label.pack(pady=5)

genre_label = Label(root, text="", font=("Arial", 12), bg="#1C1C1C", fg="white")
genre_label.pack(pady=5)

rating_label = Label(root, text="", font=("Arial", 12), bg="#1C1C1C", fg="white")
rating_label.pack(pady=5)

plot_label = Label(root, text="", font=("Arial", 11), bg="#1C1C1C", fg="white", wraplength=400, justify=LEFT)
plot_label.pack(pady=10)

poster_label = Label(root, bg="#1C1C1C")
poster_label.pack(pady=10)

root.mainloop()
