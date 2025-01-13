import tkinter as tk
from tkinter import messagebox
import time

questions = {
    "What is the capital of France?": ["Paris", "London"],
    "What is 2 + 2?": ["4", "5"],
    "Is the earth round?": ["Yes", "No"],
    "Are you a human?": ["Yes", "No"],
}
current_question = None
timer_value = 0
timer_running = False
log_file = "game_log.txt"
after_id = None  

def log_event(event):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {event}\n")

def start_game():
    start_button.pack_forget()
    log_event("Game started")
    show_question_elements()
    timer_label.pack(pady=10)
    next_question()

def next_question():
    global current_question, questions, timer_value, timer_running
    if not questions:
        end_game()
        return

    stop_timer()

    current_question, options = questions.popitem()
    timer_value = 10
    question_label.config(text=current_question)
    option1_button.config(text=options[0], state=tk.NORMAL)
    option2_button.config(text=options[1], state=tk.NORMAL)
    skip_button.config(state=tk.NORMAL)
    start_timer()

def record_choice(choice):
    global current_question, timer_running
    log_event(f"Question: {current_question}, Choice: {choice}")
    stop_timer()
    next_question()

def start_timer():
    global timer_running
    timer_running = True
    update_timer()

def update_timer():
    global timer_value, timer_running, after_id
    if timer_value > 0 and timer_running:
        timer_label.config(text=f"Time Left: {timer_value}")
        timer_value -= 1
        after_id = root.after(1000, update_timer)
    elif timer_running:
        record_choice("Skipped")

def stop_timer():
    global timer_running, after_id
    timer_running = False
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

def end_game():
    log_event("Game ended")
    messagebox.showinfo("Game Over", "You have completed all questions!")
    root.quit()

root = tk.Tk()
root.title("Question Game")
root.geometry("800x600")

start_button = tk.Button(root, text="Start", command=start_game, font=("Arial", 14))
start_button.pack(pady=20)

question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=700, justify="center")
option1_button = tk.Button(root, text="", command=lambda: record_choice(1), font=("Arial", 12))
option2_button = tk.Button(root, text="", command=lambda: record_choice(2), font=("Arial", 12))
skip_button = tk.Button(root, text="Skip", command=lambda: record_choice("Skipped"), font=("Arial", 12))

question_label.pack_forget()
option1_button.pack_forget()
option2_button.pack_forget()
skip_button.pack_forget()

def show_question_elements():
    question_label.pack(pady=20)
    option1_button.pack(pady=10)
    option2_button.pack(pady=10)
    skip_button.pack(pady=10)

timer_label = tk.Label(root, text="Time Left: 10", font=("Arial", 14))
timer_label.pack_forget()

root.mainloop()
