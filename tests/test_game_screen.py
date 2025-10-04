import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Headless Pygame setup
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.font.init()  # Initialize font module for testing
pygame.display.set_mode((1, 1))  # minimal dummy display

import pytest
from unittest.mock import Mock
from lootbox_sim.game_screen import GameScreen

# Mock font for testing
def mock_sysfont(name, size):
    mock_font = Mock()
    mock_font.render.return_value = Mock()
    mock_font.render.return_value.get_width.return_value = 100
    mock_font.render.return_value.get_height.return_value = 30
    return mock_font

# Apply the mock
pygame.font.SysFont = mock_sysfont

def test_loot_box_adds_item(monkeypatch):
    gs = GameScreen(800, 600)

    # Patch random.random to control loot drop
    monkeypatch.setattr("random.random", lambda: 0.7)  # should pick "Steel Sword" with new loot table

    gs.open_loot_box()
    assert "Steel Sword" in gs.inventory.items
    assert gs.popup_text.startswith("You got:")

def test_inventory_toggle():
    gs = GameScreen(800, 600)
    assert gs.show_inventory == False
    # Simulate pressing 'I' key
    class Event:
        type = pygame.KEYDOWN
        key = pygame.K_i
    gs.handle_event(Event())
    assert gs.show_inventory == True

def test_escape_key_returns_to_menu():
    gs = GameScreen(800, 600)
    # Simulate pressing 'ESC' key
    class Event:
        type = pygame.KEYDOWN
        key = pygame.K_ESCAPE
    action = gs.handle_event(Event())
    assert action == "back_to_menu"

def test_chest_opening_animation():
    gs = GameScreen(800, 600)
    # Initially chest should be closed
    assert gs.chest_is_opening == False
    assert gs.chest_open_timer == 0
    
    # Open the chest
    gs.open_loot_box()
    
    # Should start opening animation
    assert gs.chest_is_opening == True
    assert gs.chest_open_timer == 0
    
    # Update animation
    gs.update(0.5)  # 0.5 seconds
    assert gs.chest_is_opening == True
    assert gs.chest_open_timer == 0.5
    
    # Complete animation
    gs.update(0.6)  # Total 1.1 seconds (more than duration)
    assert gs.chest_is_opening == False
    assert gs.chest_open_timer == 0

def test_item_categorization():
    gs = GameScreen(800, 600)
    
    # Test weapon categorization
    assert gs.get_item_category("Steel Sword") == "weapon"
    assert gs.get_item_category("Elven Bow") == "weapon"
    assert gs.get_item_category("Lightning Staff") == "weapon"
    
    # Test armor categorization
    assert gs.get_item_category("Rare Shield") == "armor"
    assert gs.get_item_category("Leather Boots") == "armor"
    assert gs.get_item_category("Iron Helmet") == "armor"
    
    # Test accessory categorization
    assert gs.get_item_category("Silver Ring") == "accessory"
    assert gs.get_item_category("Crystal Amulet") == "accessory"
    assert gs.get_item_category("Crown of Kings") == "accessory"
    
    # Test consumable categorization
    assert gs.get_item_category("Health Potion") == "consumable"
    assert gs.get_item_category("Magic Scroll") == "consumable"
    
    # Test legendary categorization
    assert gs.get_item_category("Legendary Dragon") == "legendary"
    assert gs.get_item_category("Universe Crystal") == "legendary"

def test_inventory_grid_settings():
    gs = GameScreen(800, 600)
    
    # Check grid settings are properly initialized
    assert gs.inventory_grid_cols == 6
    assert gs.inventory_grid_rows == 4
    assert gs.inventory_slot_size == 60
    assert gs.inventory_start_x == 50
    assert gs.inventory_start_y == 200

def test_mimic_initialization():
    gs = GameScreen(800, 600)
    
    # Check mimic properties are properly initialized
    assert gs.mimic_chance == 0.15
    assert gs.is_mimic == False
    assert gs.mimic_revealed == False
    assert gs.mimic_timer == 0
    assert gs.mimic_duration == 3.0

def test_mimic_encounter(monkeypatch):
    gs = GameScreen(800, 600)
    
    # Force mimic encounter
    monkeypatch.setattr("random.random", lambda: 0.1)  # Less than mimic_chance (0.15)
    
    # Add some items to inventory first
    gs.inventory.add_item("Test Sword")
    gs.inventory.add_item("Test Shield")
    
    # Open loot box
    gs.open_loot_box()
    
    # Should trigger mimic
    assert gs.is_mimic == True
    assert gs.chest_is_opening == True

def test_mimic_reset():
    gs = GameScreen(800, 600)
    
    # Set mimic state
    gs.is_mimic = True
    gs.mimic_revealed = True
    gs.mimic_timer = 2.0
    gs.chest_is_opening = True
    
    # Reset mimic
    gs.reset_mimic()
    
    # Check everything is reset
    assert gs.is_mimic == False
    assert gs.mimic_revealed == False
    assert gs.mimic_timer == 0
    assert gs.chest_is_opening == False

def test_mimic_roasts_initialization():
    gs = GameScreen(800, 600)
    
    # Check that roast lines are loaded
    assert len(gs.mimic_roasts) > 0
    assert "Git gud! 🤡" in gs.mimic_roasts
    assert "Skill issue! 💀" in gs.mimic_roasts
    
    # All roasts should be strings and reasonably short
    for roast in gs.mimic_roasts:
        assert isinstance(roast, str)
        assert len(roast) < 20  # Keep roasts short for screen fit

def test_mimic_consequence_with_items(monkeypatch):
    gs = GameScreen(800, 600)
    
    # Add items to inventory
    gs.inventory.add_item("Test Sword")
    gs.inventory.add_item("Test Shield")
    initial_count = len(gs.inventory.items)
    
    # Mock random.choice to be predictable
    def mock_choice(seq):
        return seq[0]  # Always return first item
    monkeypatch.setattr("random.choice", mock_choice)
    
    # Execute mimic consequence
    gs.mimic_consequence()
    
    # Should have lost an item and gotten a roast message
    assert len(gs.inventory.items) <= initial_count
    assert "Ate " in gs.popup_text  # New shorter format
    assert gs.popup_timer > 0

pygame.quit()
