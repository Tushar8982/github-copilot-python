# Refactoring Legacy Code with GitHub Copilot – Sudoku Game

A modernized Sudoku web application built with Python Flask and developed with the assistance of GitHub Copilot.

This project started from a simple legacy Sudoku implementation and was refactored into a more modular, maintainable, tested, and feature-rich application. The project also demonstrates responsible use of GitHub Copilot for code refactoring, documentation, testing, error handling, and UI improvements.

---

## Project Overview

The original application provided a basic Sudoku game with limited functionality.

The goal of this project was to refactor the legacy codebase while adding modern game functionality and improving the overall user experience.

The final application includes:

- Difficulty selection
- Valid Sudoku puzzle generation
- Unique-solution validation
- Real-time input feedback
- Puzzle checking
- Hint functionality
- Game timer
- Top 10 leaderboard
- Player name tracking
- Local storage persistence
- Dark mode
- Responsive UI
- Alternating 3×3 Sudoku grid styling
- Automated testing
- Modular Sudoku logic
- Graceful error handling
- GitHub Copilot-assisted development

---

# Features

## 1. Sudoku Board

The application provides a standard 9×9 Sudoku board.

Each puzzle follows the standard Sudoku rules:

- Each row contains numbers 1–9 without repetition.
- Each column contains numbers 1–9 without repetition.
- Each 3×3 sub-grid contains numbers 1–9 without repetition.

Prefilled cells are locked so that the player cannot accidentally modify the original puzzle.

---

## 2. Difficulty Levels

Players can choose between:

- Easy
- Medium
- Hard

The selected difficulty controls the number of prefilled clues in the generated puzzle.

Fewer prefilled cells result in a more challenging puzzle.

The application also validates the requested clue count to ensure it remains within a valid Sudoku range.

---

## 3. Unique Solution Validation

One of the main improvements over the legacy implementation is the Sudoku puzzle generator.

The application generates a completed valid Sudoku board and removes cells while checking whether the resulting puzzle still has exactly one solution.

The Sudoku logic includes:

- Backtracking-based solving
- Solution counting
- Board validation
- Unique-solution detection

This prevents the application from generating puzzles that have multiple possible solutions.

---

## 4. Immediate Input Feedback

The application provides visual feedback while the player interacts with the board.

Invalid entries can be identified visually, allowing players to correct mistakes while solving rather than waiting until the entire puzzle is completed.

This improves the interactive experience and makes the game easier to understand.

---

## 5. Check Solution

The **Check Solution** button compares the player's current board against the generated solution.

Incorrect cells are identified and highlighted so the player can determine which entries need correction.

The Flask backend validates the submitted board before processing it.

Invalid requests are handled with appropriate error messages and HTTP status codes instead of allowing malformed input to cause unexpected application behavior.

---

## 6. Hint System

The **Hint** button provides assistance when the player is stuck.

A hint:

- Fills one correct cell.
- Uses the puzzle's valid solution.
- Locks the revealed cell.
- Is visually distinguished from normal player entries.
- Contributes to the hint count used by the leaderboard.

---

## 7. Timer

A timer starts when a new puzzle is created and tracks the player's solving time.

The final solving time is displayed when the puzzle is completed and is used when recording leaderboard results.

This allows players to compete for faster solving times.

---

## 8. Top 10 Leaderboard

The application maintains a Top 10 leaderboard containing completed games.

Leaderboard information includes:

- Player name
- Difficulty
- Completion time
- Hints used

Leaderboard data is stored using browser `localStorage`, allowing the scores to persist when the page is refreshed or reopened.

The leaderboard can also be cleared using the provided control.

---

## 9. Player Name

Players can enter their name before completing a puzzle.

When a puzzle is successfully completed, the player's name and game information can be added to the leaderboard.

This makes the leaderboard personalized and allows multiple players to use the same application.

---

## 10. Dark Mode

The application includes a Dark Mode toggle.

The theme changes across the application interface, including:

- Page background
- Sudoku board
- Text
- Controls
- Leaderboard
- Buttons

The selected theme is persisted using browser local storage so the preference can remain available across sessions.

---

## 11. Responsive Design

The interface is designed to work across different screen sizes.

The layout adapts between:

- Desktop
- Tablet
- Mobile

The Sudoku board and controls scale appropriately while maintaining readability and usability.

---

## 12. Sudoku Grid Styling

The 9×9 board is visually divided into the standard 3×3 Sudoku regions.

Alternating background styling helps players distinguish the different 3×3 sections without changing the structure or position of the board.

The interface also provides separate visual states for:

- Original puzzle cells
- Player entries
- Hints
- Incorrect entries
- Completed cells

---

# Project Architecture

The project was refactored from a simple legacy implementation into separate modules with clear responsibilities.

```text
github-copilot-python/
│
├── Screenshots/
│   ├── Dark_mode.png
│   ├── final_app.png
│   ├── initial_tests.png
│   ├── copilot_unique_solution.png
│   ├── copilot_top10_localstorage.png
│   ├── copilot_grid_styling.png
│   └── ...
│
├── starter/
│   │
│   ├── app.py
│   ├── sudoku_logic.py
│   ├── requirements.txt
│   │
│   ├── sudoku/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   ├── solver.py
│   │   └── validator.py
│   │
│   ├── tests/
│   │   └── test_sudoku_logic.py
│   │
│   ├── static/
│   │   ├── main.js
│   │   └── styles.css
│   │
│   └── templates/
│       └── index.html
│
├── instruction.md
├── pytest.ini
├── .gitignore
└── README.md