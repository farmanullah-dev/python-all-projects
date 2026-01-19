import requests
import tkinter as tk
from tkinter import messagebox

# --- Function to predict age ---
def predict_age():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name!")
        return

    url = f"https://api.agify.io/?name={name}"

    try:
        response = requests.get(url)
        data = response.json()

        if "age" in data and data["age"] is not None:
            age = data["age"]
            count = data.get("count", 0)

            result_label.config(
                text=f"👤 Name: {name}\n🎂 Predicted Age: {age}\n📊 Based on {count} records",
                fg="#FACC15",
            )
        else:
            result_label.config(text="❌ Age data not found for this name.", fg="#F87171")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# --- GUI Setup ---
root = tk.Tk()
root.title("🎂 Age Predictor (Agify.io)")
root.geometry("500x450")
root.config(bg="#0F172A")

# --- Title ---
lbl_title = tk.Label(
    root, text="🎂 Age Predictor", font=("Segoe UI", 22, "bold"), fg="#38BDF8", bg="#0F172A"
)
lbl_title.pack(pady=25)

# --- Input Frame ---
frame = tk.Frame(root, bg="#1E293B", bd=2, relief=tk.RIDGE)
frame.pack(pady=10)

entry_name = tk.Entry(
    frame, font=("Segoe UI", 16), width=25, bg="#334155", fg="white", relief=tk.FLAT, insertbackground="white"
)
entry_name.pack(side=tk.LEFT, padx=10, pady=10)

btn_predict = tk.Button(
    frame, text="Predict", font=("Segoe UI", 13, "bold"), bg="#38BDF8", fg="white", relief=tk.FLAT, command=predict_age
)
btn_predict.pack(side=tk.RIGHT, padx=10, pady=10)

# --- Result Label ---
result_label = tk.Label(root, text="", font=("Segoe UI", 16, "bold"), bg="#0F172A", fg="white", justify=tk.CENTER)
result_label.pack(pady=40)

# --- Footer ---
lbl_footer = tk.Label(
    root, text="🔗 Powered by Agify.io API", font=("Segoe UI", 10), fg="#94A3B8", bg="#0F172A"
)
lbl_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
