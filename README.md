# Ayoayo Game Implementation

This project is an implementation of the traditional Mancala-style board game, Ayoayo. The game logic is written in Python, and a simple web interface is provided using Streamlit.

This was created as part of the "Software Developer Attachment Take-Away Assignment".

## Game Overview

Ayoayo is a two-player strategy game involving a board with 12 pits (6 for each player) and two stores (one for each player). The game starts with an equal number of seeds (typically 4) in each of the 12 pits. The objective is to capture more seeds in your store than your opponent.

### Key Rules Implemented (as per `Ayoayo_rules.pdf`):
* **Setup**: 4 seeds in each of the 6 pits on each player's side.
* **Sowing**: Players take turns picking up all seeds from one of their pits and "sowing" them one by one in a counter-clockwise direction into subsequent pits and their own store. Opponent's stores are skipped.
* **Extra Turn**: If the last seed sown lands in the player's own store, they get an extra turn.
* **Capture**: If the last seed sown lands in an empty pit on the player's own side, they capture all seeds from the opponent's pit directly opposite, as well as the capturing seed itself. These are all placed in the player's store.
* **Game End**: The game ends when all 6 pits on one player's side are empty. The other player then collects all remaining seeds from their own pits into their store.
* **Winner**: The player with the most seeds in their store at the end of the game wins.

## Project Structure

ayoayo_game_project/ ├── ayoayo.py # Contains the core game logic (Player and Ayoayo classes) ├── app.py # Streamlit application for playing the game via a web interface ├── reflection.txt # Developer's reflections on the project development process └── README.md # This file

## Features

* Python-based game logic adhering to the provided rules.
* Implementation of `Ayoayo` and `Player` classes as specified.
* Private data members within classes.
* Simple interactive web interface using Streamlit for gameplay.
* Turn-based play with visual representation of the board.
* Clear indication of player scores and game status.
* Game log to track moves.

## Technologies Used

* **Python 3**: For the core game logic.
* **Streamlit**: For creating the simple web-based user interface.

## How to Run the Game

1.  **Prerequisites**:
    * Python 3.7 or higher installed.
    * pip (Python package installer) installed.

2.  **Clone the repository (or download the files)** into a local directory.

3.  **Navigate to the project directory**:
    ```bash
    cd path/to/ayoayo_game_project
    ```

4.  **Install dependencies**:
    The only external dependency is Streamlit.
    ```bash
    pip install streamlit
    ```

5.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
    This will typically open the game in your default web browser. If not, the terminal will display a local URL (e.g., `http://localhost:8501`) to open manually.

6.  **Play the game**:
    * Enter names for Player 1 and Player 2.
    * Click "Start Game!".
    * Players take turns selecting a pit from their side of the board to sow seeds.
    * Follow the on-screen prompts and enjoy the game!

## Deliverables from Assignment

* `ayoayo.py`: Implements the `Ayoayo` class with game logic and the `Player` class.
* `reflection.txt`: Contains the developer's thought process, challenges, and learning during the project.
* This `README.md` provides an overview and setup instructions.

## Notes

* The game rules implemented are based on the `Ayoayo_rules.pdf` document provided alongside the original assignment.
* The core game logic in `ayoayo.py` can also be tested or integrated into other Python environments. The `if __name__ == "__main__":` block in `ayoayo.py` contains example console-based test runs.

---
*Generated on: May 8, 2025*
*Location: Juja, Kiambu County, Kenya*