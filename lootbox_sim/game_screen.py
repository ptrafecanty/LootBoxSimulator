import pygame
import random
from lootbox_sim.inventory import Inventory

class GameScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 48)

        # Loot box rectangle
        self.loot_box_rect = pygame.Rect(width//2 - 50, height//2 - 50, 100, 100)

        # Inventory
        self.inventory = Inventory()

        # Loot table
        self.loot_table = [
            {"name": "Common Sword", "chance": 0.6},
            {"name": "Rare Shield", "chance": 0.25},
            {"name": "Epic Staff", "chance": 0.1},
            {"name": "Legendary Dragon", "chance": 0.05}
        ]

        # Popup text
        self.popup_text = ""
        self.popup_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.loot_box_rect.collidepoint(event.pos):
                self.open_loot_box()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"  # go back to menu / exit
        return None

    def open_loot_box(self):
        r = random.random()
        cumulative = 0
        for item in self.loot_table:
            cumulative += item["chance"]
            if r < cumulative:
                self.inventory.add_item(item["name"])
                self.popup_text = f"You got: {item['name']}"
                self.popup_timer = 2.0  # seconds
                print(self.popup_text)  # for debugging
                break

    def update(self, dt):
        if self.popup_timer > 0:
            self.popup_timer -= dt
            if self.popup_timer <= 0:
                self.popup_text = ""

    def draw(self, surface):
        surface.fill((30, 30, 60))  # background
        pygame.draw.rect(surface, (200, 200, 50), self.loot_box_rect)  # loot box

        if self.popup_text:
            text_surf = self.font.render(self.popup_text, True, (255, 255, 255))
            surface.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 100))
