# Tic Tac Toe AI

A compact Python and Pygame project where you play Tic Tac Toe against an AI powered by the Minimax algorithm.

I originally built this as a small school project and later refactored it to make the code easier to read, the game flow more reliable, and the README easier to share as a portfolio piece.

## Highlights

- Human vs AI gameplay
- Minimax-based decision making for the AI
- Clean win detection with highlighted winning lines
- Draw detection and restart support
- Simple single-file project that is easy to run and extend

## Refactor Notes

- Removed the unnecessary NumPy dependency and simplified the board representation
- Separated board logic, AI logic, and the game loop into focused classes
- Added proper draw handling so the game ends cleanly when the board is full
- Kept the project import-safe with a standard `if __name__ == "__main__"` entry point

## Tech Stack

- Python 3.8+
- Pygame

## Run Locally

1. Install the dependency:

   ```bash
   pip install pygame
   ```

2. Launch the game:

   ```bash
   python mini_project.py
   ```

## Controls

- Click a square to place your mark
- Press `R` to restart the match
- Close the window to quit

## AI Modes

The script defaults to the Minimax AI. If you want a more relaxed opponent, set `AI_LEVEL = 0` in the script to switch to random moves.

## Project Structure

- `mini_project.py` contains the board, AI, and game loop

## Shareable Summary

A Tic Tac Toe game built with Python and Pygame, featuring a Minimax AI and a cleaned-up codebase focused on readability and maintainability.

## What I Learned

- How to structure a small game loop cleanly
- How Minimax evaluates game states
- Why handling draw states matters in turn-based games

---

Enjoy playing Tic Tac Toe.



