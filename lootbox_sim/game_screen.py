import pygame
import random
import json
import os
from lootbox_sim.inventory import Inventory

class GameScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 48)

        # Loot box rectangle (make it bigger for the chest)
        self.loot_box_rect = pygame.Rect(width//2 - 75, height//2 - 60, 150, 120)

        # Inventory
        self.inventory = Inventory()
        self.show_inventory = False  # toggle display

        # Load loot table from JSON
        self.loot_table = self.load_loot_table()

        # Popup
        self.popup_text = ""
        self.popup_timer = 0

        # Chest opening animation
        self.chest_is_opening = False
        self.chest_open_timer = 0
        self.chest_open_duration = 1.0  # 1 second animation
        self.chest_lid_angle = 0  # 0 = closed, 90 = fully open

    def load_loot_table(self):
        """Load loot table from JSON file"""
        try:
            # Get the directory of this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            loot_table_path = os.path.join(current_dir, 'loot_table.json')
            
            with open(loot_table_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback to hardcoded table if file not found
            return [
                {"name": "Common Sword", "chance": 0.6},
                {"name": "Rare Shield", "chance": 0.25},
                {"name": "Epic Staff", "chance": 0.1},
                {"name": "Legendary Dragon", "chance": 0.05}
            ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.loot_box_rect.collidepoint(event.pos):
                self.open_loot_box()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_menu"  # back to menu
            elif event.key == pygame.K_i:
                self.show_inventory = not self.show_inventory  # toggle
        return None

    def open_loot_box(self):
        # Don't open if already opening
        if self.chest_is_opening:
            return
            
        # Start opening animation
        self.chest_is_opening = True
        self.chest_open_timer = 0
        
        r = random.random()
        cumulative = 0
        for item in self.loot_table:
            cumulative += item["chance"]
            if r < cumulative:
                self.inventory.add_item(item["name"])
                self.popup_text = f"You got: {item['name']}"
                self.popup_timer = 2.0  # seconds
                print(self.popup_text)
                break

    def draw_treasure_chest(self, surface):
        """Draw a detailed treasure chest with opening animation"""
        x, y = self.loot_box_rect.x, self.loot_box_rect.y
        w, h = self.loot_box_rect.width, self.loot_box_rect.height
        
        # Main chest body (brown wood)
        chest_body = pygame.Rect(x, y + h//4, w, h*3//4)
        pygame.draw.rect(surface, (101, 67, 33), chest_body)  # Dark brown
        pygame.draw.rect(surface, (139, 90, 43), chest_body, 3)  # Brown outline
        
        # Add some wood grain lines to the body
        for i in range(3):
            line_y = chest_body.y + (i + 1) * chest_body.height // 4
            pygame.draw.line(surface, (80, 53, 25), 
                           (chest_body.x + 5, line_y), 
                           (chest_body.x + chest_body.width - 5, line_y), 2)
        
        # Calculate lid position based on opening animation
        lid_offset_y = 0
        lid_height = h//2
        
        if self.chest_is_opening:
            # Animate the lid opening (moving up and rotating)
            progress = min(self.chest_open_timer / self.chest_open_duration, 1.0)
            # Smooth easing function for animation
            eased_progress = 1 - (1 - progress) ** 3  # Ease-out cubic
            lid_offset_y = -int(eased_progress * 20)  # Move lid up by 20 pixels
            self.chest_lid_angle = eased_progress * 45  # Rotate up to 45 degrees
        
        # Draw the chest lid
        lid_rect = pygame.Rect(x, y + lid_offset_y, w, lid_height)
        pygame.draw.rect(surface, (101, 67, 33), lid_rect)  # Dark brown
        pygame.draw.rect(surface, (139, 90, 43), lid_rect, 3)  # Brown outline
        
        # If chest is opening, show magical glow inside
        if self.chest_is_opening and self.chest_open_timer > 0.2:
            progress = min((self.chest_open_timer - 0.2) / (self.chest_open_duration - 0.2), 1.0)
            glow_alpha = int(progress * 150)
            
            # Create a glowing effect inside the chest
            glow_surf = pygame.Surface((w - 20, 30), pygame.SRCALPHA)
            glow_color = (255, 215, 0, glow_alpha)  # Golden glow with alpha
            pygame.draw.ellipse(glow_surf, glow_color, (0, 0, w - 20, 30))
            
            # Add magical sparkles
            import math
            for i in range(5):
                sparkle_x = x + 20 + (i * (w - 40) // 5) + int(math.sin(self.chest_open_timer * 10 + i) * 5)
                sparkle_y = y + h//2 + int(math.cos(self.chest_open_timer * 8 + i) * 8)
                sparkle_size = 3 + int(math.sin(self.chest_open_timer * 15 + i) * 2)
                pygame.draw.circle(surface, (255, 255, 150), (sparkle_x, sparkle_y), sparkle_size)
            
            surface.blit(glow_surf, (x + 10, y + h//3))
        
        # Metal bands (iron straps) - only on body, not on lid
        band_color = (64, 64, 64)  # Dark gray
        # Horizontal bands on body
        for i in range(2):
            band_y = chest_body.y + (i + 1) * chest_body.height // 3
            band_rect = pygame.Rect(x, band_y - 3, w, 6)
            pygame.draw.rect(surface, band_color, band_rect)
        
        # Vertical bands on body
        left_band = pygame.Rect(x + w//4 - 3, y + h//4, 6, h*3//4)
        right_band = pygame.Rect(x + 3*w//4 - 3, y + h//4, 6, h*3//4)
        pygame.draw.rect(surface, band_color, left_band)
        pygame.draw.rect(surface, band_color, right_band)
        
        # Lock mechanism (only show when closed)
        if not self.chest_is_opening or self.chest_open_timer < 0.3:
            lock_center_x = x + w//2
            lock_center_y = y + h*2//3
            lock_size = 12
            
            # Lock body (brass/gold)
            lock_rect = pygame.Rect(lock_center_x - lock_size//2, lock_center_y - lock_size//2, 
                                   lock_size, lock_size)
            pygame.draw.rect(surface, (218, 165, 32), lock_rect)  # Golden rod
            pygame.draw.rect(surface, (184, 134, 11), lock_rect, 2)  # Darker gold outline
            
            # Keyhole
            keyhole_rect = pygame.Rect(lock_center_x - 2, lock_center_y - 2, 4, 4)
            pygame.draw.rect(surface, (0, 0, 0), keyhole_rect)
            
            # Lock shackle (U-shaped)
            shackle_rect = pygame.Rect(lock_center_x - 6, lock_center_y - 12, 12, 8)
            pygame.draw.arc(surface, (184, 134, 11), shackle_rect, 0, 3.14159, 3)
        
        # Corner reinforcements on body
        corner_size = 8
        corners = [
            (x + 5, y + h//4 + 5),  # Top left
            (x + w - corner_size - 5, y + h//4 + 5),  # Top right
            (x + 5, y + h - corner_size - 5),  # Bottom left
            (x + w - corner_size - 5, y + h - corner_size - 5)  # Bottom right
        ]
        
        for corner_x, corner_y in corners:
            corner_rect = pygame.Rect(corner_x, corner_y, corner_size, corner_size)
            pygame.draw.rect(surface, band_color, corner_rect)
            # Add a small highlight
            pygame.draw.rect(surface, (96, 96, 96), corner_rect, 1)

    def update(self, dt):
        # Update popup timer
        if self.popup_timer > 0:
            self.popup_timer -= dt
            if self.popup_timer <= 0:
                self.popup_text = ""
        
        # Update chest opening animation
        if self.chest_is_opening:
            self.chest_open_timer += dt
            if self.chest_open_timer >= self.chest_open_duration:
                # Animation finished, reset to closed state
                self.chest_is_opening = False
                self.chest_open_timer = 0
                self.chest_lid_angle = 0

    def draw(self, surface):
        surface.fill((30, 30, 60))  # background
        
        # Draw the treasure chest instead of a simple rectangle
        self.draw_treasure_chest(surface)

        # Add a glow effect around the chest to make it more attractive
        glow_rect = pygame.Rect(self.loot_box_rect.x - 5, self.loot_box_rect.y - 5,
                               self.loot_box_rect.width + 10, self.loot_box_rect.height + 10)
        pygame.draw.rect(surface, (100, 80, 20), glow_rect, 3)  # Golden glow

        # Popup text
        if self.popup_text:
            text_surf = self.font.render(self.popup_text, True, (255, 255, 255))
            surface.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 100))

        # Inventory display
        if self.show_inventory:
            y_offset = 200
            header = self.font.render("Inventory:", True, (255, 255, 255))
            surface.blit(header, (50, y_offset))
            y_offset += 50
            for name, count in self.inventory.items.items():
                item_text = self.font.render(f"{name}: {count}", True, (255, 255, 255))
                surface.blit(item_text, (50, y_offset))
                y_offset += 40
