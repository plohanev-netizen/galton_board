# Deterministic Galton Board Simulator

A Python-based visualization of a Galton Board (bean machine) using a deterministic algorithm with toggle switches. Unlike a traditional Galton board that relies on random chance, this simulator uses mechanical "switches" that flip their state every time a ball passes through them.

## 🚀 Features

The repository contains two distinct simulation modes:

### 1. Automated Simulation (`animated_board.py`)
This script runs a continuous animation of balls falling through the board.
- **Visuals:** Watch the board state evolve and see the distribution grow in real-time.
- **Configurable Parameters:**
  - `LEVELS`: Number of rows of switches (tested optimally between 8 and 10).
  - `BALLS`: Total number of balls to be processed.
  - `INITIAL_MODE`: Sets the starting position of all switches:
    - `LEFT`: All switches point left.
    - `RIGHT`: All switches point right.
    - `RANDOM`: Switches are set to random initial positions.
  - `SPEED`: Animation delay (lower values result in faster animation).

### 2. Interactive Manual Mode (`animated_jamming.py`)
This script allows for a step-by-step analysis of the board's logic, including a "jamming" probability feature where switches might fail to toggle.
- **Controls:**
  - `SPACE`: Move the current ball down one level (or spawn a new ball if the previous one reached a bin).
  - `R`: Reset the board, clear all bins, and return switches to the initial state.
- **Jamming Logic:** Includes a `JAM_CHANCE` parameter (default 3%) representing the probability that a switch directs the ball but fails to flip its state for the next ball.

## 🛠 Prerequisites

To run these simulations, you need **Python 3.x** installed. The project relies on the `matplotlib` library for all graphics and animations.



## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME
