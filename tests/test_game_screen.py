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

pygame.quit()
