# Loot Box Simulator

## Overview

**Loot Box Simulator** is a Python project built with **Pygame** that simulates the experience of opening loot boxes in a game. Players can interact with a graphical interface to open loot boxes, collect items, and view their inventory. This project is intended as a personal project to practice Python, Pygame, and basic game design concepts.

---

## Features

1. **Interactive Menu**
   - Start the game or quit.
   - Buttons respond to mouse clicks.

2. **Loot Box Mechanics**
   - Clickable loot box generates random items.
   - Items have different rarity probabilities based on JSON configuration.
   - Adds items automatically to inventory.

3. **Inventory System**
   - Tracks items and quantities.
   - Toggle inventory display with the `I` key.
   - Inventory updates in real time as items are collected.

4. **Popup Messages**
   - Shows what item was obtained after opening a loot box.
   - Popup disappears automatically after a few seconds.

5. **Event Handling**
   - Mouse clicks for loot box and menu buttons.
   - Keyboard input for inventory toggle and returning to menu.

6. **Configurable Loot Table**
   - Items and their probabilities are defined in `loot_table.json`.
   - Easy to modify item names and drop rates.

---

## Installation

### Requirements

- Python 3.12+
- Pygame
- Pytest (for testing, optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ptrafecanty/LootBoxSimulator.git
cd LootBoxSimulator
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies

```bash
pip install pygame
pip install pytest      # optional, for running tests
```

---

## How to Run the Game

```bash
python main.py
```

---

## Controls

- **Mouse**: Click on menu buttons and loot box
- **I Key**: Toggle inventory display on/off
- **ESC Key**: Return to main menu from game screen
- **Close Window**: Quit the game

---

## File Structure

```
LootBoxSimulator/
├── main.py                    # Entry point: runs the game
├── lootbox_sim/
│   ├── __init__.py
│   ├── game.py                # Main game loop logic
│   ├── game_screen.py         # GameScreen class with loot box, inventory, popups
│   ├── inventory.py           # Inventory class for item management
│   ├── menu.py                # MenuScreen class for main menu
│   └── loot_table.json        # Item definitions and drop probabilities
├── tests/
│   ├── test_game_screen.py    # Tests for game screen functionality
│   ├── test_inventory.py      # Tests for inventory system
│   └── test_menu.py           # Tests for menu interactions
└── README.md
```

---

## Loot Table Configuration

The game uses a JSON file (`loot_table.json`) to define available items and their drop probabilities:

```json
[
  { "name": "Common Sword", "chance": 0.6 },
  { "name": "Rare Shield", "chance": 0.25 },
  { "name": "Epic Staff", "chance": 0.1 },
  { "name": "Legendary Dragon", "chance": 0.05 }
]
```

**Note**: Chances should add up to 1.0 (100%) for proper probability distribution.

---

## Running Tests

```bash
pytest
```

**Note**: Some tests may require headless mode setup for Pygame in CI environments.

---

## Troubleshooting

### Font Initialization Issues
If you encounter "font not initialized" errors during testing:
- Ensure pygame is properly installed
- The tests include pygame.font.init() calls for headless testing
- Make sure you have a display available (or use headless mode)

### Import Errors
- Ensure you're running from the project root directory
- Activate your virtual environment before running
- Verify all dependencies are installed

---

## Future Enhancements

- Sound effects for loot box opening
- Visual animations for item drops
- Save/load game state
- Statistics tracking
- Multiple loot box types
- Item rarity visual indicators