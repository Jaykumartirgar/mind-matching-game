# 🧠 AI Mind Matching Game

A feature-rich memory card matching game built with Python and Tkinter — play against an AI opponent or challenge a friend in multiplayer mode!

---

## 📌 Overview

Test your memory with this classic card-flip matching game. Choose your difficulty, theme, and mode — then race against the clock to find all pairs before time runs out. An AI opponent makes single-player mode challenging and fun.

---

## ✨ Features

- 🤖 **AI opponent** — Play against a smart AI in Single Player mode
- 👥 **Multiplayer** — Two-player mode on the same keyboard
- 🎯 **3 difficulty levels** — Easy (2×2), Medium (4×4), Hard (6×6)
- 🎨 **3 themes** — Numbers, Letters, or Emojis
- ⏱️ **Countdown timer** — Customizable time limit per game
- 💡 **One-time hint** — Briefly reveals all cards to help when you're stuck
- 🔊 **Sound effects** — Audio feedback for card flips and matches
- 🔄 **Restart & Quit** — Controls built into the game window
- 📐 **Responsive board** — Card sizes adjust dynamically when you resize the window
- 🏆 **Score tracking** — Live score display per player/AI throughout the game

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.x | Core language |
| Tkinter | Desktop GUI and game board |
| random module | Card shuffling and AI picks |
| winsound (Windows) | Sound effects |

---

## 📁 Project Structure

```
Mind_Matching_Game/
│
├── mind_game.py     # Complete game logic, UI, AI, and settings menu
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Jaykumartirgar/mind-matching-game.git
cd mind-matching-game
```

**2. Run the game**
```bash
python mind_game.py
```

> No external libraries required — uses Python's built-in `tkinter` only!

---

## 🎮 How to Play

1. Launch the game — a **Settings Menu** appears first
2. Choose your **difficulty**, **theme**, **mode**, and **timer**
3. Click **Start Game**
4. Click any card to flip it, then click another to find its match
5. Matched pairs stay revealed (highlighted green)
6. Unmatched pairs flip back after a short delay
7. Player with most matches when time runs out (or all pairs found) **wins!**

### AI Mode
- After each Player 1 turn (whether matched or not), the AI takes its turn
- AI randomly picks from unflipped, unmatched cards

---

## 🧩 Game Modes

| Mode | Description |
|---|---|
| Single Player | Play against AI — takes turns after each of your moves |
| Multiplayer | Two humans take turns on the same screen |

---

## 📸 Screenshots

> *(Add screenshots of the game here after running it)*

---

## 🙋 Author

**Jaykumar Tirgar**
- GitHub: [@Jaykumartirgar](https://github.com/Jaykumartirgar)
- LinkedIn: [jay-tirgar](https://www.linkedin.com/in/jay-tirgar-05b359349/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
