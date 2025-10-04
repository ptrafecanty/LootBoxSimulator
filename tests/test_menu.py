import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Headless Pygame setup
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.font.init()  # Initialize font module for testing
pygame.display.set_mode((1, 1))  # minimal dummy display

from unittest.mock import Mock
from lootbox_sim.menu import MenuScreen

# Mock font for testing
def mock_sysfont(name, size):
    mock_font = Mock()
    mock_font.render.return_value = Mock()
    mock_font.render.return_value.get_width.return_value = 100
    mock_font.render.return_value.get_height.return_value = 30
    return mock_font

# Apply the mock
pygame.font.SysFont = mock_sysfont

def test_start_button_click():
    menu = MenuScreen(800, 600)
    x = menu.buttons["Start"].x + 10
    y = menu.buttons["Start"].y + 10
    class Event:
        type = pygame.MOUSEBUTTONDOWN
        button = 1
        pos = (x, y)
    action = menu.handle_event(Event())
    assert action == "start_game"

def test_exit_button_click():
    menu = MenuScreen(800, 600)
    x = menu.buttons["Exit"].x + 10
    y = menu.buttons["Exit"].y + 10
    class Event:
        type = pygame.MOUSEBUTTONDOWN
        button = 1
        pos = (x, y)
    action = menu.handle_event(Event())
    assert action == "quit"

def test_click_outside_buttons():
    menu = MenuScreen(800, 600)
    class Event:
        type = pygame.MOUSEBUTTONDOWN
        button = 1
        pos = (0, 0)
    action = menu.handle_event(Event())
    assert action is None

pygame.quit()
