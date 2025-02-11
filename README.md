# Terminal Board Game

A simple, terminal-based two-player board game written in Python. In this game, two players (one using the "O" symbol and the other "X") take turns placing their pieces on a board whose size can be configured (between 5 and 10). The game automatically detects wins in horizontal, vertical, and diagonal directions, tracks scores (4 points per win), and resets the board when full. It also supports saving and loading the game state using CSV files.

## Features

- **Two-Player Gameplay:** Players alternate turns placing their symbols on the board.
- **Configurable Board:** Choose a board size from 5 to 10.
- **Win Detection:** Checks for wins horizontally, vertically, and diagonally.
- **Score Tracking:** Each win awards exactly 4 points.
- **Save/Load Functionality:** Game state (board and additional data) is saved to and loaded from CSV files.
- **Automatic Board Reset:** When the board is full, the round ends and the board resets.

### Game Flow

- **New Game / Load Game:**  
  At launch, you can start a new game or load a saved game (press **c** to load a saved game).

- **Making a Move:**  
  Players choose a column (or line) where they want to drop their piece. The board is printed with letters for rows and numbers for columns.

- **Win and Score:**  
  When a winning configuration is detected, the winning pieces are highlighted and then removed; points are awarded, and any cascading wins are handled.

- **Saving the Game:**  
  At the end of a round, you'll be prompted whether you want to save the current game state to CSV files.
