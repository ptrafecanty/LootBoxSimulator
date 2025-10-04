# Loot Box Simulator

## Overview

**Loot Box Simulator** is an advanced Python project built with **Pygame** that delivers an immersive loot box opening experience. Features include a beautiful treasure chest that opens with magical animations, a comprehensive grid-based inventory system with custom icons, and a mischievous mimic system that will roast you with hilarious memes when you least expect it! This project showcases advanced game development concepts including animations, visual effects, and dynamic user interfaces.

---

## ✨ Features

### 🎮 Core Gameplay
1. **Interactive Menu**
   - Polished start screen with responsive buttons
   - Clean, user-friendly interface

2. **Realistic Treasure Chest**
   - Beautiful hand-drawn chest with wood grain, metal bands, and golden lock
   - Smooth opening animation with lid movement and magical glow effects
   - Sparkling particle effects when opening
   - Much more immersive than a simple rectangle!

3. **Advanced Loot System**
   - **32 unique items** across multiple categories (up from 4!)
   - **Rarity-based drops**: Common (50.5%), Uncommon (20.5%), Epic (10%), Legendary (1.9%)
   - **JSON-configurable** loot table for easy customization
   - Perfectly balanced probability distribution

### 🎒 Revolutionary Inventory System
4. **Grid-Based Inventory**
   - **6x4 visual grid** layout (24 slots total)
   - **Custom item icons** for every category:
     - ⚔️ **Weapons**: Swords, bows, staffs with unique shapes
     - 🛡️ **Armor**: Shields, boots, helmets with realistic designs
     - 💍 **Accessories**: Rings, amulets, crystals with magical effects
     - 🧪 **Consumables**: Potions, scrolls with detailed artwork
     - ✨ **Legendary**: Special glowing effects with animated sparkles
   - **Item stacking** with quantity counters
   - **Semi-transparent background** with professional styling

### 👹 Mimic Surprise System
5. **Hilarious Mimic Encounters** (15% chance)
   - **Visual transformation**: Chest reveals glowing red eyes, sharp teeth, and spikes
   - **Savage roasting**: 14+ meme-worthy insults like "Git gud! 🤡" and "Skill issue! 💀"
   - **Item theft**: Mimic steals random items with additional roasts
   - **Smooth animations**: 3-second encounter with shaking effects
   - **No spam**: Clean, single-message experience

### 🎯 Enhanced User Experience
6. **Smooth Animations**
   - Chest opening sequences with easing functions
   - Magical particle effects and glowing auras
   - Red menacing glow for mimic encounters

7. **Professional UI**
   - **ESC key** returns to main menu (preserves inventory)
   - **I key** toggles beautiful grid inventory
   - **Mouse controls** for all interactions
   - Responsive design with proper feedback

8. **Comprehensive Testing**
   - **17 unit tests** covering all functionality
   - **Test coverage** for animations, inventory, and mimic system
   - **Automated validation** of game mechanics

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

- **Mouse**: Click treasure chest to open (watch out for mimics!)
- **I Key**: Toggle beautiful grid inventory display
- **ESC Key**: Return to main menu (preserves your collected items)
- **Close Window**: Quit the game entirely

---

## 🎲 Loot Table Breakdown

The game features **32 unique items** across **5 rarity tiers**:

### **Common Items (50.5% total chance)**
- Rusty Dagger, Common Sword, Basic Shield, Wooden Bow
- Leather Boots, Health Potion, Iron Helmet, Chain Mail

### **Uncommon Items (20.5% total chance)**  
- Steel Sword, Rare Shield, Silver Ring, Enchanted Boots
- Magic Scroll, Crossbow, Mithril Chainmail, Crystal Amulet

### **Epic Items (10% total chance)**
- Epic Staff, Flaming Sword, Dragon Scale Armor, Elven Bow
- Frost Gauntlets, Shadow Cloak, Lightning Staff, Phoenix Feather

### **Legendary Items (1.9% total chance)**
- Legendary Dragon, Excalibur, Crown of Kings, God Slayer Blade
- Infinity Gauntlet, Time Manipulation Orb, Cosmic Shield, Universe Crystal

**Note**: All probabilities are perfectly balanced and add up to 100%

---

## 👹 Mimic System

**Beware!** 15% of treasure chests are actually **mimics** in disguise!

### **Mimic Features:**
- **Visual Transformation**: Eyes, teeth, spikes, and shaking effects
- **Savage Roasts**: "Git gud! 🤡", "Skill issue! 💀", "L + ratio! 🌱"
- **Item Theft**: Steals random items with additional insults
- **Meme References**: Modern gaming slang and internet culture

### **Sample Mimic Encounters:**
```
MIMIC! Pranked! 📺
Ate Lightning Staff! Yoink! 🥷

MIMIC! Ez clap! ⚡  
No items! Broke! 📊
```

---

## File Structure

```
LootBoxSimulator/
├── main.py                    # Entry point: runs the game
├── lootbox_sim/
│   ├── __init__.py
│   ├── game.py                # Main game loop and screen management
│   ├── game_screen.py         # Game logic, treasure chest, inventory, mimics
│   ├── inventory.py           # Item storage and management
│   ├── menu.py                # Main menu interface
│   └── loot_table.json        # 32 items with rarity probabilities
├── tests/
│   ├── test_game_screen.py    # Comprehensive game logic tests
│   ├── test_inventory.py      # Inventory system tests  
│   └── test_menu.py           # Menu interaction tests
├── assets/                    # Future: images and sounds
├── sounds/                    # Future: audio effects
└── README.md                  # This comprehensive guide
```
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

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest -v

# Run specific test categories  
python -m pytest tests/test_game_screen.py -v  # Game mechanics
python -m pytest tests/test_inventory.py -v   # Inventory system
python -m pytest tests/test_menu.py -v        # Menu interactions
```

**Test Coverage**: 17 comprehensive tests covering:
- Loot box mechanics and item generation
- Inventory grid system and icon categorization  
- Treasure chest opening animations
- Mimic encounter system and roasting mechanics
- Menu navigation and controls

---

## 🛠️ Technical Highlights

### **Advanced Game Development Concepts**
- **Custom Animation System**: Smooth easing functions for chest opening
- **Particle Effects**: Magical sparkles and glow effects
- **State Management**: Clean separation of game states and screens
- **Event-Driven Architecture**: Responsive user input handling
- **Visual Effects**: Alpha blending, color transitions, shaking effects

### **Object-Oriented Design**
- **Modular Architecture**: Separate classes for different game components
- **Inheritance Patterns**: Clean base classes for screens and objects
- **Encapsulation**: Private methods and proper data hiding
- **Polymorphism**: Unified interface for different item types

### **Data-Driven Development**
- **JSON Configuration**: Externalized loot table for easy modification
- **Automated Testing**: Comprehensive test suite with mocking
- **Error Handling**: Graceful fallbacks and exception management

---

## 🚀 Future Enhancements

### **Planned Features**
- 🔊 **Sound System**: Chest opening, mimic roars, item collection sounds
- 💾 **Save/Load**: Persistent inventory and statistics
- 📊 **Statistics Dashboard**: Track opening count, rarity percentages, mimic encounters
- 🎨 **Visual Upgrades**: Sprite-based graphics, particle systems, screen shake
- 🏆 **Achievement System**: Unlock rewards for milestones
- 🎪 **Multiple Chest Types**: Different loot tables and visual styles

### **Advanced Systems**
- 🌐 **Multiplayer Support**: Share loot with friends
- 📈 **Economy System**: Item values and trading mechanics  
- 🎮 **Gamepad Support**: Controller input handling
- 🎯 **Quest System**: Challenges and objectives
- 🎭 **Character Classes**: Different loot preferences per class

---

## 🤝 Contributing

This project showcases modern Python game development practices and is perfect for learning:
- **Pygame fundamentals** and advanced techniques
- **Game state management** and animation systems
- **Test-driven development** with comprehensive coverage
- **Object-oriented design** patterns in game development
- **User interface design** and user experience optimization

Feel free to fork, experiment, and contribute improvements!

---

## 📜 License

This project is open source and available for educational purposes. Perfect for learning game development, Python programming, and software engineering best practices.

---

## 🎯 Summary

**Loot Box Simulator** has evolved from a simple prototype into a **polished gaming experience** featuring:

✅ **Beautiful treasure chest** with realistic animations  
✅ **32 unique items** across 5 rarity tiers  
✅ **Professional grid inventory** with custom icons  
✅ **Hilarious mimic encounters** with meme-worthy roasts  
✅ **Smooth animations** and magical effects  
✅ **Comprehensive testing** with 17 unit tests  
✅ **Clean architecture** and maintainable code  

**Ready to get roasted by a treasure chest? Start collecting loot and see if you can avoid the savage mimics!** 🎮👹✨