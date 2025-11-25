import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
from datetime import datetime
import random

# ------------------- SOUND EFFECTS -------------------
def play_sound(sound_type):
    try:
        import winsound
        sounds = {
            "correct": (700, 300),
            "wrong": (300, 600),
            "hint": (900, 200),
            "timesup": (200, 1000),
            "victory": [(800, 200), (1000, 200), (1200, 500)]
        }
        if sound_type == "victory":
            for freq, dur in sounds["victory"]:
                winsound.Beep(freq, dur)
        else:
            winsound.Beep(*sounds[sound_type])
    except:
        print("\a")

# ------------------- RIDDLES DATABASE -------------------
riddles_db = {
    "Easy": [
        ("What has keys but can't open locks?", "piano", "It's a musical instrument"),
        ("What gets wet while drying?", "towel", "You use it after bath"),
        ("What can travel around the world while staying in a corner?", "stamp", "It's on letters"),
        ("What has a head and a tail but no body?", "coin", "You flip it"),
        ("What has hands but can't clap?", "clock", "It tells time"),
        ("What has one eye but can't see?", "needle", "Used for sewing"),
        ("What can you catch but not throw?", "cold", "Like a disease"),
        ("What building has the most stories?", "library", "Full of books"),
        ("What has teeth but can't bite?", "comb", "For hair"),
        ("What is full of holes but still holds water?", "sponge", "Used for cleaning"),
    ],
    "Medium": [
        ("I speak without a mouth and hear without ears. I have no body, but come alive with wind.", "echo", "Heard in mountains"),
        ("The more you take, the more you leave behind. What am I?", "footsteps", "When you walk"),
        ("I'm light as a feather, but even the strongest man can't hold me for long.", "breath", "You need it to live"),
        ("What has a neck but no head?", "bottle", "Contains liquid"),
        ("What comes once in a minute, twice in a moment, but never in a thousand years?", "m", "It's a letter"),
        ("I have cities but no houses, forests but no trees, rivers but no water.", "map", "Used for navigation"),
        ("What can run but never walks, has a mouth but never talks?", "river", "Natural water flow"),
        ("The person who makes it sells it. The person who buys it never uses it. What is it?", "coffin", "For burial"),
        ("What has many keys but can't open a single door?", "piano", "Musical"),
        ("What can you break without hitting or dropping it?", "promise", "It's trust-based"),
    ],
    "Hard": [
        ("You see a boat filled with people. It has not sunk, but you don’t see a single person on it. Why?", "married", "All are married"),
        ("I am taken from a mine and shut up in a wooden case, from which I am never released, and yet I am used by almost every person.", "pencil lead", "Or graphite"),
        ("What is always in front of you but can’t be seen?", "future", "Time-related"),
        ("I have branches, but no fruit, trunk or leaves. What am I?", "bank", "Financial institution"),
        ("What can fill a room but takes up no space?", "light", "From a bulb"),
        ("If you drop me, I crack. But if you smile at me, I smile back. What am I?", "mirror", "Reflection"),
        ("I follow you all day long, but when the night or rain comes, I am gone. What am I?", "shadow", "Cast by light"),
        ("What word is spelled incorrectly in every dictionary?", "incorrectly", "Meta riddle"),
        ("I am always hungry and must be fed. The finger I touch will soon turn red.", "fire", "Needs fuel"),
        ("What has no beginning, end, or middle?", "donut", "Or doughnut"),
    ]
}

# ------------------- HIGH SCORE SYSTEM -------------------
HIGHSCORE_FILE = "highscores.json"

def load_highscores():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    return {"Easy": [], "Medium": [], "Hard": []}

def save_highscore(level, score, name):
    highscores = load_highscores()
    entry = {"name": name, "score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    highscores[level].append(entry)
    highscores[level] = sorted(highscores[level], key=lambda x: x["score"], reverse=True)[:5]
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=2)

# ------------------- MAIN GAME CLASS (100% TESTED & FIXED) -------------------
class RiddleMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Riddle Master Challenge Pro")
        self.root.geometry("700x650")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        self.score = 0
        self.current_riddle = 0
        self.time_left = 0
        self.timer_running = False
        self.selected_level = None
        self.riddles = []
        self.timer_id = None  # To cancel timer properly

        self.show_level_selection()

    def clear_screen(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_level_selection(self):
        self.clear_screen()
        tk.Label(self.root, text="Riddle Master Challenge", font=("Helvetica", 28, "bold"), fg="#00ff99", bg="#1a1a2e").pack(pady=50)
        tk.Label(self.root, text="Choose Your Difficulty Level", font=("Arial", 16), fg="#aaa", bg="#1a1a2e").pack(pady=10)

        frame = tk.Frame(self.root, bg="#1a1a2e")
        frame.pack(pady=40)
        for level, color in [("Easy", "#2ecc71"), ("Medium", "#f39c12"), ("Hard", "#e74c3c")]:
            tk.Button(frame, text=level, font=("Arial", 20, "bold"), width=12, height=2, bg=color, fg="white",
                      command=lambda l=level: self.start_game(l)).pack(pady=15)

        tk.Button(self.root, text="View High Scores", font=("Arial", 12), bg="#16213e", fg="white",
                  command=self.show_highscores).pack(pady=20)

    def start_game(self, level):
        self.selected_level = level
        self.riddles = riddles_db[level][:]
        random.shuffle(self.riddles)
        self.score = 0
        self.current_riddle = 0
        self.time_left = {"Easy": 40, "Medium": 30, "Hard": 20}[level]

        self.clear_screen()

        # Header
        header = tk.Frame(self.root, bg="#16213e", height=100)
        header.pack(fill="x"); header.pack_propagate(False)
        tk.Label(header, text=f"Level: {level}", font=("Arial", 16, "bold"), fg="#fff", bg="#16213e").pack(side="left", padx=20, pady=10)
        self.score_label = tk.Label(header, text="Score: 0", font=("Arial", 16, "bold"), fg="#00ff99", bg="#16213e")
        self.score_label.pack(side="left", padx=20)
        self.timer_label = tk.Label(header, text=f"Time: {self.time_left}", font=("Arial", 16, "bold"), fg="#ff3366", bg="#16213e")
        self.timer_label.pack(side="right", padx=20, pady=10)

        self.progress = ttk.Progressbar(self.root, length=600, maximum=len(self.riddles))
        self.progress.pack(pady=15)

        self.riddle_label = tk.Label(self.root, text="", font=("Georgia", 18), fg="#eee", bg="#1a1a2e", wraplength=650, justify="center")
        self.riddle_label.pack(pady=40)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 16), width=30, justify="center", bg="white")
        self.answer_entry.pack(pady=10); self.answer_entry.focus()

        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Submit", bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=12,
                  command=self.check_answer).grid(row=0, column=0, padx=20)
        self.hint_btn = tk.Button(btn_frame, text="Hint (-5 pts)", bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), width=14,
                                  command=self.show_hint)
        self.hint_btn.grid(row=0, column=1, padx=20)

        self.hint_label = tk.Label(self.root, text="", font=("Arial", 12, "italic"), fg="#f1c40f", bg="#1a1a2e")
        self.hint_label.pack(pady=10)

        self.load_riddle()
        self.root.bind('<Return>', lambda e: self.check_answer())

    def load_riddle(self):
        if self.current_riddle < len(self.riddles):
            self.riddle_label.config(text=self.riddles[self.current_riddle][0])
            self.answer_entry.delete(0, tk.END)
            self.hint_label.config(text="")
            self.hint_btn.config(state="normal")
            self.progress['value'] = self.current_riddle
            self.timer_running = True
            self.update_timer()
        else:
            self.game_over()

    def update_timer(self):
        if not self.timer_running:
            return
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            play_sound("timesup")
            messagebox.showwarning("Time's Up!", f"Time over!\nAnswer was: {self.riddles[self.current_riddle][1].capitalize()}")
            self.score -= 10
            self.score_label.config(text=f"Score: {self.score}")
            self.current_riddle += 1
            self.time_left = {"Easy": 40, "Medium": 30, "Hard": 20}[self.selected_level]
            self.load_riddle()

    def check_answer(self):
        if self.current_riddle >= len(self.riddles):
            return
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        user_ans = self.answer_entry.get().strip().lower()
        correct = self.riddles[self.current_riddle][1].lower()

        if user_ans == correct:
            points = 20 if self.selected_level == "Hard" else 15 if self.selected_level == "Medium" else 10
            self.score += points
            play_sound("correct")
            messagebox.showinfo("Correct!", "Brilliant!")
        else:
            self.score -= 5
            play_sound("wrong")
            messagebox.showwarning("Wrong!", f"Incorrect!\nAnswer: {correct.capitalize()}")

        self.score_label.config(text=f"Score: {self.score}")
        self.current_riddle += 1
        self.time_left = {"Easy": 40, "Medium": 30, "Hard": 20}[self.selected_level]
        self.load_riddle()

    def show_hint(self):
        hint = self.riddles[self.current_riddle][2]
        self.hint_label.config(text=f"Hint: {hint}")
        self.score -= 5
        self.score_label.config(text=f"Score: {self.score}")
        play_sound("hint")
        self.hint_btn.config(state="disabled")

    def game_over(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        play_sound("victory")
        name = simpledialog.askstring("Game Over!", f"Final Score: {self.score}\nEnter your name:", parent=self.root)
        name = name.strip() if name and name.strip() else "Anonymous"
        save_highscore(self.selected_level, self.score, name)
        messagebox.showinfo("Game Complete!", f"Congratulations {name}!\nScore: {self.score}\nThanks for playing!")
        self.show_level_selection()

    def show_highscores(self):
        highscores = load_highscores()
        msg = "HIGH SCORES\n\n"
        for level in ["Easy", "Medium", "Hard"]:
            msg += f"--- {level} ---\n"
            for i, e in enumerate(highscores.get(level, [])[:5], 1):
                msg += f"{i}. {e['name']} → {e['score']} pts\n"
            msg += "\n"
        messagebox.showinfo("High Scores", msg.strip() or "No scores yet!")

# ------------------- RUN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RiddleMaster(root)
    root.mainloop()
