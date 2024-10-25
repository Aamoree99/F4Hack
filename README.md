
# Fallout Hacking Terminal

A Fallout-inspired hacking terminal emulator where users can input words, find matches, and interact with an interface complete with sound and visual effects.

## Description

This project emulates a Fallout-style terminal interface with animated text, typing sound effects, and color effects. Users can input commands like `EXIT` to end the session or `N` to reset the interface. Enter words to check for matches, and the system will provide suggestions and feedback.

## Requirements

- **Python 3.6+**
- **PyQt5** (for graphical interface and sound management)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/username/FalloutTerminal.git
    cd FalloutTerminal
    ```

2. Install the required package:

    ```bash
    pip install PyQt5
    ```

   If `pip` doesn’t work on macOS or Linux, try `pip3`:

   ```bash
   pip3 install PyQt5
   ```

3. Run the application:

    ```bash
    python main.py
    ```

   If `python` doesn’t work on macOS or Linux, try `python3`:

   ```bash
   python3 main.py
   ```

## Usage

Once launched, the terminal will display a sequence simulating a system breach. Use the following commands:

- `N` - Reset the terminal and start a new session.
- `EXIT` - Shut down the terminal.
- Enter a list of words to start a word match game, then follow the prompts to guess matches.

## Principle of Operation

The terminal starts with an animated text display, setting up a hacking scenario. When users input a list of words, the terminal initiates a "word match" sequence, displaying words with random bit sequences and suggesting potential matches. Typing sounds enhance the experience. The interface includes custom styling, with a blinking cursor and green color scheme that resemble the classic terminal.
