import tkinter as tk
from tkinter import messagebox

# List of riddles: (riddle, answer, hint)
riddles = [
    ("What has keys but can't open locks?", "piano", "It's a musical instrument"),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", "m", "It's a letter"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "echo", "You hear me in mountains"),
    ("The more you take, the more you leave behind. What am I?", "footsteps", "You make them when you walk"),
    ("What can travel around the world while staying in a corner?", "stamp", "It's on an envelope"),
    ("I have cities but no houses, forests but no trees, and rivers but no water. What am I?", "map", "You look at it to find places"),
    ("What gets wet while drying?", "towel", "You use it after a shower"),
    ("I'm light as a feather, but the strongest person can't hold me for much longer than a minute. What am I?", "breath", "You do it all the time"),
    ("What has a head, a tail, is brown, and has no legs?", "penny", "It's a coin"),
    ("You see a boat filled with people. It has not sunk, but when you look again you don’t see a single person on the boat. Why?", "married", "All the people on the boat are married"),
    ("What can you break, even if you never pick it up or touch it?", "promise", "It's something you give"),
    ("I am always hungry, I must always be fed. The finger I touch will soon turn red. What am I?", "fire", "It needs fuel")
]

class RiddleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Riddle Master Challenge")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)

        self.score = 0
        self.current_riddle = 0

        # Title
        title = tk.Label(root, text="Riddle Master Challenge", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#2c3e50")
        title.pack(pady=20)

        # Score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14), bg="#f0f8ff", fg="#27ae60")
        self.score_label.pack(pady=10)

        # Riddle number
        self.riddle_num_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f8ff")
        self.riddle_num_label.pack(pady=5)

        # Riddle text
        self.riddle_label = tk.Label(root, text="", font=("Arial", 16), bg="#f0f8ff", wraplength=550, justify="center")
        self.riddle_label.pack(pady=30)

        # Answer entry
        self.answer_entry = tk.Entry(root, font=("Arial", 14), width=30, justify="center")
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#f0f8ff")
        btn_frame.pack(pady=20)

        self.submit_btn = tk.Button(btn_frame, text="Submit Answer", font=("Arial", 12), bg="#3498db", fg="white", width=15, command=self.check_answer)
        self.submit_btn.grid(row=0, column=0, padx=20)

        self.hint_btn = tk.Button(btn_frame, text="Show Hint (-3 pts)", font=("Arial", 12), bg="#e67e22", fg="white", width=15, command=self.show_hint)
        self.hint_btn.grid(row=0, column=1, padx=20)

        # Hint label (initially hidden)
        self.hint_label = tk.Label(root, text="", font=("Arial", 12, "italic"), fg="#8e44ad", bg="#f0f8ff")
        self.hint_label.pack(pady=10)

        self.load_riddle()

        # Press Enter to submit
        self.root.bind('<Return>', lambda event: self.check_answer())

    def load_riddle(self):
        if self.current_riddle < len(riddles):
            riddle_text, _, _ = riddles[self.current_riddle]
            self.riddle_num_label.config(text=f"Riddle {self.current_riddle + 1} of {len(riddles)}")
            self.riddle_label.config(text=riddle_text)
            self.answer_entry.delete(0, tk.END)
            self.hint_label.config(text="")
            self.hint_btn.config(state="normal")
        else:
            self.game_over()

    def check_answer(self):
        if self.current_riddle >= len(riddles):
            return

        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = riddles[self.current_riddle][1].lower()

        if user_answer == correct_answer:
            self.score += 10
            messagebox.showinfo("Correct!", "Great job! +10 points")
        else:
            self.score -= 5
            messagebox.showwarning("Wrong!", f"Incorrect! -5 points\nThe answer was: {riddles[self.current_riddle][1].capitalize()}")

        self.score_label.config(text=f"Score: {self.score}")
        self.current_riddle += 1
        self.load_riddle()

    def show_hint(self):
        hint = riddles[self.current_riddle][2]
        self.hint_label.config(text=f"Hint: {hint}")
        self.score -= 3
        self.score_label.config(text=f"Score: {self.score}")
        self.hint_btn.config(state="disabled")  # One hint per riddle

    def game_over(self):
        self.riddle_label.config(text="Congratulations! You've completed all riddles!")
        self.answer_entry.pack_forget()
        btn_frame = self.submit_btn.master
        btn_frame.pack_forget()
        final_msg = f"Final Score: {self.score}\n\nWell done!" 
        messagebox.showinfo("Game Over", final_msg)


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = RiddleGame(root)
    root.mainloop()