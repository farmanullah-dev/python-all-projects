import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Function to fetch word meaning ---
def get_meaning():
    word = entry_word.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word!")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meanings = data[0]["meanings"]
        phonetic = data[0].get("phonetic", "")
        word_label.config(text=f"🔤 Word: {word.capitalize()}  |  🔈 {phonetic}")
        
        result_box.config(state=tk.NORMAL)
        result_box.delete(1.0, tk.END)
        for meaning in meanings:
            part_of_speech = meaning["partOfSpeech"]
            definitions = meaning["definitions"]
            result_box.insert(tk.END, f"🧩 {part_of_speech.capitalize()}\n", "pos")
            for d in definitions:
                definition = d["definition"]
                example = d.get("example", "")
                result_box.insert(tk.END, f"• {definition}\n", "def")
                if example:
                    result_box.insert(tk.END, f"  📘 Example: {example}\n\n", "ex")
        result_box.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Word not found! Please try another word.")

# --- GUI Setup ---
root = tk.Tk()
root.title("📚 Dictionary App")
root.geometry("700x500")
root.config(bg="#121212")

# --- Title ---
title = tk.Label(root, text="📖 Free Dictionary", font=("Segoe UI", 22, "bold"), fg="#00E676", bg="#121212")
title.pack(pady=15)

# --- Input Box ---
frame = tk.Frame(root, bg="#1E1E1E", bd=2, relief=tk.RIDGE)
frame.pack(pady=10)
entry_word = tk.Entry(frame, font=("Segoe UI", 16), width=25, bg="#2E2E2E", fg="white", relief=tk.FLAT, insertbackground="white")
entry_word.pack(side=tk.LEFT, padx=10, pady=10)
btn_search = tk.Button(frame, text="🔍 Search", font=("Segoe UI", 13, "bold"), bg="#00E676", fg="#121212", activebackground="#00C853", command=get_meaning)
btn_search.pack(side=tk.RIGHT, padx=10, pady=10)

# --- Word Info Label ---
word_label = tk.Label(root, text="", font=("Segoe UI", 14, "italic"), fg="#80CBC4", bg="#121212")
word_label.pack(pady=5)

# --- Result Box ---
result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 13), width=70, height=15, bg="#1E1E1E", fg="white", relief=tk.FLAT)
result_box.pack(padx=20, pady=10)
result_box.tag_config("pos", foreground="#00E5FF", font=("Segoe UI", 13, "bold"))
result_box.tag_config("def", foreground="#E0E0E0")
result_box.tag_config("ex", foreground="#81C784", font=("Segoe UI", 12, "italic"))
result_box.config(state=tk.DISABLED)

root.mainloop()
