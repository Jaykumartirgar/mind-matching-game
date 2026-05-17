import tkinter as tk
from tkinter import messagebox
import random

try:
    import winsound
except Exception:
    winsound = None


class AIMindMatchingGame:
    def __init__(self, root, size=4, difficulty="Easy", theme="Numbers", mode="Single", time_limit=120):
        self.root = root
        self.size = size
        self.difficulty = difficulty
        self.theme = theme
        self.mode = mode
        self.total_pairs = (size * size) // 2
        self.values = []
        self.buttons = []
        self.flipped = []
        self.matched = set()
        self.hint_used = False
        self.player1_score = 0
        self.player2_or_ai_score = 0
        self.current_player = "Player 1"
        self.time_limit = time_limit
        self.time_left = time_limit
        self.timer_job = None

        self.root.title("AI Mind Matching Game")
        self.root.geometry("800x800")
        self.root.configure(bg="#1e1e2e")
        self.root.bind("<Configure>", self.on_resize)

        self.build_ui()
        self.start_new_game()

    def build_ui(self):
        top_frame = tk.Frame(self.root, bg="#1e1e2e")
        top_frame.pack(fill="x", pady=(8, 4))

        self.title_label = tk.Label(top_frame, text="Memory Match Game", font=("Arial", 20, "bold"),
                                    bg="#1e1e2e", fg="#facc15")
        self.title_label.pack(side="left", padx=12)

        self.info_label = tk.Label(top_frame, text="", font=("Arial", 11), bg="#1e1e2e", fg="#ffffff")
        self.info_label.pack(side="left", padx=12)

        self.timer_label = tk.Label(top_frame, text="", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#ff6b6b")
        self.timer_label.pack(side="right", padx=12)

        score_frame = tk.Frame(self.root, bg="#1e1e2e")
        score_frame.pack(fill="x")
        self.score_label = tk.Label(score_frame, text="", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#ffffff")
        self.score_label.pack(pady=(2, 8))

        controls_frame = tk.Frame(self.root, bg="#1e1e2e")
        controls_frame.pack(fill="x", pady=(0, 6))

        self.hint_button = tk.Button(controls_frame, text="💡 Hint (one-time)", command=self.use_hint,
                                     font=("Arial", 12), bg="#fde68a")
        self.hint_button.pack(side="left", padx=8)

        self.restart_button = tk.Button(controls_frame, text="🔁 Restart", command=self.restart_game,
                                        font=("Arial", 12), bg="#4ade80")
        self.restart_button.pack(side="left", padx=8)

        self.quit_button = tk.Button(controls_frame, text="✖ Quit", command=self.quit_game,
                                     font=("Arial", 12), bg="#f87171")
        self.quit_button.pack(side="right", padx=8)

        self.board_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.board_frame.pack(expand=True, fill="both", padx=8, pady=8)

    def start_new_game(self):
        self.values = self.generate_values()
        random.shuffle(self.values)
        self.flipped = []
        self.matched = set()
        self.hint_used = False
        self.player1_score = 0
        self.player2_or_ai_score = 0
        self.current_player = "Player 1"
        self.time_left = self.time_limit

        self.info_label.config(text=f"Mode: {self.mode} | Difficulty: {self.difficulty} | Theme: {self.theme}")
        self.update_score_label()
        self.update_timer_label()

        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.buttons = []

        for i in range(self.size * self.size):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 16, "bold"),
                            bg="#374151", fg="#ffffff", relief="raised",
                            command=lambda idx=i: self.on_card_click(idx))
            btn.grid(row=i // self.size, column=i % self.size, sticky="nsew", padx=6, pady=6)
            self.buttons.append(btn)

        for r in range(self.size):
            self.board_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.size):
            self.board_frame.grid_columnconfigure(c, weight=1)

        self.hint_button.config(state="normal")

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_job = self.root.after(1000, self.timer_tick)

    def restart_game(self):
        if messagebox.askyesno("Restart", "Are you sure you want to restart the game?"):
            self.start_new_game()

    def quit_game(self):
        if messagebox.askyesno("Quit", "Exit the game?"):
            self.root.quit()

    def generate_values(self):
        total_pairs = (self.size * self.size) // 2
        if self.theme == "Numbers":
            vals = [str(i) for i in range(1, total_pairs + 1)]
        elif self.theme == "Letters":
            vals = [chr(65 + i) for i in range(total_pairs)]
        else:
            emojis = ["😀", "😂", "😍", "😎", "😜", "🤖", "🐱", "🐶",
                      "🍕", "🎮", "⚽", "🎵", "🚗", "🌟", "🔥", "💎",
                      "🍀", "🌈", "🧩", "🕹️", "📚", "🔔", "🧠", "🪄"]
            vals = emojis[:total_pairs]
        return vals * 2

    def on_card_click(self, idx):
        if idx in self.matched or idx in self.flipped:
            return
        self.reveal_idx(idx)
        self.flipped.append(idx)
        if len(self.flipped) == 2:
            self.root.after(350, self.evaluate_flipped)

    def reveal_idx(self, idx):
        self.buttons[idx].config(text=self.values[idx], bg="#60a5fa", state="disabled")
        self.play_sound("click")

    def hide_idx(self, idx):
        self.buttons[idx].config(text="", bg="#374151", state="normal")

    def evaluate_flipped(self):
        if len(self.flipped) != 2:
            return
        a, b = self.flipped
        if self.values[a] == self.values[b]:
            self.matched.update([a, b])
            self.buttons[a].config(bg="#22c55e")
            self.buttons[b].config(bg="#22c55e")
            self.play_sound("match")
            if self.current_player == "Player 1":
                self.player1_score += 1
            else:
                self.player2_or_ai_score += 1
            self.update_score_label()
            self.flipped = []
            if len(self.matched) == len(self.values):
                self.root.after(200, self.end_game)
            elif self.mode == "Single" and self.current_player == "AI":
                self.root.after(600, self.ai_take_turn)
        else:
            self.root.after(600, self.hide_non_matches_and_switch)

    def hide_non_matches_and_switch(self):
        for idx in self.flipped:
            if idx not in self.matched:
                self.hide_idx(idx)
        self.flipped = []
        if self.mode == "Single":
            self.current_player = "AI" if self.current_player == "Player 1" else "Player 1"
            self.update_score_label()
            if self.current_player == "AI":
                self.root.after(700, self.ai_take_turn)
        else:
            self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"
            self.update_score_label()

    def ai_take_turn(self):
        available = [i for i in range(len(self.values)) if i not in self.matched and i not in self.flipped]
        if len(available) < 2:
            self.current_player = "Player 1"
            self.update_score_label()
            return
        picks = random.sample(available, 2)
        self.reveal_idx(picks[0])
        self.flipped.append(picks[0])

        def second_pick():
            if picks[1] not in self.matched and picks[1] not in self.flipped:
                self.reveal_idx(picks[1])
                self.flipped.append(picks[1])
                self.root.after(400, self.evaluate_flipped)

        self.root.after(500, second_pick)

    def use_hint(self):
        if self.hint_used:
            messagebox.showinfo("Hint", "Hint already used.")
            return
        self.hint_used = True
        self.hint_button.config(state="disabled")
        to_reveal = [i for i in range(len(self.values)) if i not in self.matched]
        for idx in to_reveal:
            self.buttons[idx].config(text=self.values[idx], state="disabled", bg="#60a5fa")
        self.root.after(1000, lambda: self._hide_hint(to_reveal))

    def _hide_hint(self, indices):
        for idx in indices:
            if idx not in self.matched:
                self.buttons[idx].config(text="", state="normal", bg="#374151")

    def timer_tick(self):
        if self.time_left <= 0:
            self.update_timer_label()
            self.end_game(time_up=True)
            return
        self.time_left -= 1
        self.update_timer_label()
        self.timer_job = self.root.after(1000, self.timer_tick)

    def update_timer_label(self):
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.timer_label.config(text=f"Time Left: {mins:02d}:{secs:02d}")

    def update_score_label(self):
        if self.mode == "Single":
            self.score_label.config(
                text=f"Player: {self.player1_score} | AI: {self.player2_or_ai_score} (Turn: {self.current_player})")
        else:
            self.score_label.config(
                text=f"Player 1: {self.player1_score} | Player 2: {self.player2_or_ai_score} (Turn: {self.current_player})")

    def end_game(self, time_up=False):
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        if time_up:
            msg = "⏱ Time's up!\n\n"
            if self.player1_score > self.player2_or_ai_score:
                msg += "Player 1 wins!"
            elif self.player1_score < self.player2_or_ai_score:
                msg += "AI/Player 2 wins!"
            else:
                msg += "It's a tie!"
            messagebox.showinfo("Time Up", msg)
        else:
            if self.player1_score > self.player2_or_ai_score:
                messagebox.showinfo("Game Over", "🎉 Player 1 wins!")
            elif self.player1_score < self.player2_or_ai_score:
                winner = "AI" if self.mode == "Single" else "Player 2"
                messagebox.showinfo("Game Over", f"🎉 {winner} wins!")
            else:
                messagebox.showinfo("Game Over", "🤝 It's a tie!")

        if messagebox.askyesno("Play again?", "Do you want to play again with same settings?"):
            self.start_new_game()
        else:
            self.root.quit()

    def on_resize(self, event):
        if self.size <= 0:
            return
        try:
            total_w = max(200, self.board_frame.winfo_width())
            total_h = max(200, self.board_frame.winfo_height())
            cell_w = total_w // self.size
            cell_h = total_h // self.size
            new_font = max(10, min(cell_w, cell_h) // 3)
            for btn in self.buttons:
                btn.config(font=("Arial", new_font, "bold"))
        except Exception:
            pass

    def play_sound(self, sound_type):
        if winsound is None:
            return
        try:
            if sound_type == "click":
                winsound.Beep(800, 80)
            elif sound_type == "match":
                winsound.Beep(1200, 160)
        except Exception:
            pass


def start_menu():
    menu = tk.Tk()
    menu.title("Memory Match - Settings")
    menu.geometry("420x380")
    menu.configure(bg="#0b1220")

    tk.Label(menu, text="AI Mind Matching - Settings",
             font=("Arial", 18, "bold"), fg="#facc15", bg="#0b1220").pack(pady=12)

    tk.Label(menu, text="Select Difficulty (board size):", font=("Arial", 12), fg="white", bg="#0b1220").pack(pady=(10, 4))
    difficulty_var = tk.StringVar(menu)
    difficulty_var.set("Easy")
    diff_menu = tk.OptionMenu(menu, difficulty_var, "Easy", "Medium", "Hard")
    diff_menu.config(width=12)
    diff_menu.pack()

    tk.Label(menu, text="Select Theme:", font=("Arial", 12), fg="white", bg="#0b1220").pack(pady=(12, 4))
    theme_var = tk.StringVar(menu)
    theme_var.set("Numbers")
    theme_menu = tk.OptionMenu(menu, theme_var, "Numbers", "Letters", "Emojis")
    theme_menu.config(width=12)
    theme_menu.pack()

    tk.Label(menu, text="Select Mode:", font=("Arial", 12), fg="white", bg="#0b1220").pack(pady=(12, 4))
    mode_var = tk.StringVar(menu)
    mode_var.set("Single")
    mode_menu = tk.OptionMenu(menu, mode_var, "Single", "Multi")
    mode_menu.config(width=12)
    mode_menu.pack()

    tk.Label(menu, text="Timer (seconds):", font=("Arial", 12), fg="white", bg="#0b1220").pack(pady=(12, 4))
    timer_var = tk.IntVar(menu)
    timer_var.set(120)
    timer_entry = tk.Entry(menu, textvariable=timer_var, width=10, justify="center")
    timer_entry.pack()

    def launch_game():
        diff = difficulty_var.get()
        theme = theme_var.get()
        mode = mode_var.get()
        time_limit = max(10, int(timer_var.get()))
        size_map = {"Easy": 2, "Medium": 4, "Hard": 6}
        size = size_map.get(diff, 2)
        menu.destroy()
        root = tk.Tk()
        AIMindMatchingGame(root, size=size, difficulty=diff, theme=theme,
                           mode=("Single" if mode == "Single" else "Multi"), time_limit=time_limit)
        root.mainloop()

    tk.Button(menu, text="Start Game", command=launch_game, font=("Arial", 14), bg="#10b981", fg="white").pack(pady=18)

    menu.mainloop()


if __name__ == "__main__":
    start_menu()
