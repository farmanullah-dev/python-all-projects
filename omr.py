import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Entry, Frame

answer_key = {}

def process_omr(image_path, num_questions=10):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    answers = {}
    q_num = 1

    for cnt in sorted(contours, key=lambda c: cv2.boundingRect(c)[1]):
        x, y, w, h = cv2.boundingRect(cnt)
        roi = thresh[y:y + h, x:x + w]

        filled = cv2.countNonZero(roi) > (w * h) // 2

        if filled:
            answers[q_num] = "A"  # placeholder for now
            q_num += 1
        if q_num > num_questions:
            break

    return answers

def upload_teacher():
    global answer_key
    if not q_entry.get().isdigit():
        result_label.config(text="⚠️ Enter number of questions first!", fg="red")
        return
    file_path = filedialog.askopenfilename()
    if file_path:
        answer_key = process_omr(file_path, int(q_entry.get()))
        result_label.config(text="✅ Teacher OMR Uploaded!", fg="green")

def upload_student():
    if not q_entry.get().isdigit():
        result_label.config(text="⚠️ Enter number of questions first!", fg="red")
        return
    if not answer_key:
        result_label.config(text="⚠️ Upload teacher OMR first!", fg="red")
        return
    file_path = filedialog.askopenfilename()
    if file_path:
        student_answers = process_omr(file_path, int(q_entry.get()))
        score = sum(1 for q in student_answers if student_answers[q] == answer_key.get(q))
        result_label.config(
            text=f"📊 Student Score: {score}/{q_entry.get()}",
            fg="blue", font=("Arial", 14, "bold")
        )

# ---------------- GUI ----------------
root = Tk()
root.title("OMR Checker System")

# Set window size & center it
root.geometry("500x300")
root.configure(bg="#f4f6f7")  # light gray background

# Title label
Label(root, text="📘 OMR Checker System", font=("Arial", 18, "bold"), bg="#f4f6f7", fg="#2c3e50").pack(pady=10)

frame = Frame(root, bg="#f4f6f7")
frame.pack(pady=10)

Label(frame, text="Number of Questions:", font=("Arial", 12), bg="#f4f6f7").grid(row=0, column=0, padx=5, pady=5)
q_entry = Entry(frame, font=("Arial", 12), width=10)
q_entry.grid(row=0, column=1, padx=5, pady=5)

Button(root, text="Upload Teacher OMR", font=("Arial", 12), bg="#3498db", fg="white", width=20, command=upload_teacher).pack(pady=8)
Button(root, text="Upload Student OMR", font=("Arial", 12), bg="#2ecc71", fg="white", width=20, command=upload_student).pack(pady=8)

result_label = Label(root, text="", font=("Arial", 12, "bold"), bg="#f4f6f7")
result_label.pack(pady=15)

root.mainloop()
