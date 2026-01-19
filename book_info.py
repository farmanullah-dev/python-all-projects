import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO

# --- Function to search books ---
def search_books():
    query = entry_search.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a book title or author!")
        return

    url = f"https://openlibrary.org/search.json?q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        docs = data.get("docs", [])

        if not docs:
            messagebox.showinfo("No Results", "No books found for your search.")
            return

        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)

        for book in docs[:10]:  # Show top 10 results
            title = book.get("title", "Unknown Title")
            author = ", ".join(book.get("author_name", ["Unknown Author"]))
            year = book.get("first_publish_year", "N/A")
            isbn = book.get("isbn", [""])[0] if book.get("isbn") else None
            cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg" if isbn else ""

            result_box.insert(tk.END, f"📘 {title}\n", "title")
            result_box.insert(tk.END, f"✍️ Author(s): {author}\n", "author")
            result_box.insert(tk.END, f"📅 Published: {year}\n", "year")

            if cover_url:
                try:
                    img_data = requests.get(cover_url).content
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((100, 150))
                    cover_photo = ImageTk.PhotoImage(img)
                    image_labels.append(cover_photo)  # Keep reference to avoid garbage collection
                    result_box.image_create(tk.END, image=cover_photo)
                    result_box.insert(tk.END, "\n")
                except:
                    result_box.insert(tk.END, "🖼️ Cover not available\n")

            result_box.insert(tk.END, "-" * 60 + "\n\n")

        result_box.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to fetch book data.")

# --- GUI Setup ---
root = tk.Tk()
root.title("📚 Open Library Book Finder")
root.geometry("800x600")
root.config(bg="#101820")

# Keep image references
image_labels = []

# --- Title ---
title = tk.Label(root, text="📖 Open Library Book Finder", font=("Segoe UI", 22, "bold"), fg="#FEE715", bg="#101820")
title.pack(pady=15)

# --- Input Frame ---
frame = tk.Frame(root, bg="#1E1E1E", bd=2, relief=tk.RIDGE)
frame.pack(pady=10)
entry_search = tk.Entry(frame, font=("Segoe UI", 16), width=35, bg="#2E2E2E", fg="white", relief=tk.FLAT, insertbackground="white")
entry_search.pack(side=tk.LEFT, padx=10, pady=10)
btn_search = tk.Button(frame, text="🔍 Search", font=("Segoe UI", 13, "bold"), bg="#FEE715", fg="#101820", activebackground="#FFD700", command=search_books)
btn_search.pack(side=tk.RIGHT, padx=10, pady=10)

# --- Result Box ---
result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12), width=90, height=20, bg="#1E1E1E", fg="white", relief=tk.FLAT)
result_box.pack(padx=20, pady=10)
result_box.tag_config("title", foreground="#FEE715", font=("Segoe UI", 13, "bold"))
result_box.tag_config("author", foreground="#00E5FF")
result_box.tag_config("year", foreground="#81C784")
result_box.config(state=tk.DISABLED)

root.mainloop()
