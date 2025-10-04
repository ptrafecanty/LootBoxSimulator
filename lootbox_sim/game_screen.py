import pygame
import random
import json
import os
import math
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

        # Mimic surprise system
        self.mimic_chance = 0.15  # 15% chance of mimic
        self.is_mimic = False
        self.mimic_revealed = False
        self.mimic_timer = 0
        self.mimic_duration = 3.0  # 3 seconds mimic display
        
        # Hilarious mimic roast lines (shorter for better screen fit)
        self.mimic_roasts = [
            "Git gud! 🤡",
            "Skill issue! 💀",
            "Got em! �",
            "L + ratio! 🌱",
            "Pranked! 📺",
            "Greedy much? 🤑",
            "MIMIC'D! �",
            "No loot 4 u! 🏆",
            "Rookie! 👑",
            "Gnomed! 🧙‍♂️",
            "Played urself! 🎉",
            "Ez clap! ⚡",
            "Trap card! 🃏",
            "Flawless! 🎯"
        ]

        # Inventory grid settings
        self.inventory_grid_cols = 6
        self.inventory_grid_rows = 4
        self.inventory_slot_size = 60
        self.inventory_start_x = 50
        self.inventory_start_y = 200

    def get_item_category(self, item_name):
        """Categorize items based on their name"""
        item_lower = item_name.lower()
        
        # Check legendary first (highest priority)
        if any(legendary in item_lower for legendary in ['dragon', 'legendary', 'epic', 'universe', 'cosmic', 'infinity', 'god']):
            return 'legendary'
        
        # Weapons
        elif any(weapon in item_lower for weapon in ['sword', 'blade', 'dagger', 'bow', 'crossbow', 'staff', 'excalibur']):
            return 'weapon'
        
        # Armor & Protection
        elif any(armor in item_lower for armor in ['shield', 'armor', 'mail', 'helmet', 'boots', 'gauntlets', 'cloak']):
            return 'armor'
        
        # Accessories
        elif any(accessory in item_lower for accessory in ['ring', 'amulet', 'crown', 'crystal', 'orb', 'gauntlet']):
            return 'accessory'
        
        # Consumables
        elif any(consumable in item_lower for consumable in ['potion', 'scroll', 'feather']):
            return 'consumable'
        
        # Default to misc
        return 'misc'

    def draw_item_icon(self, surface, item_name, x, y, size=40):
        """Draw an icon for the given item based on its category"""
        category = self.get_item_category(item_name)
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Background circle for all items
        pygame.draw.circle(surface, (50, 50, 50), (center_x, center_y), size // 2)
        pygame.draw.circle(surface, (100, 100, 100), (center_x, center_y), size // 2, 2)
        
        if category == 'weapon':
            # Draw a sword icon
            if 'bow' in item_name.lower() or 'crossbow' in item_name.lower():
                # Bow shape
                pygame.draw.arc(surface, (139, 90, 43), 
                               (x + 8, y + 8, size - 16, size - 16), 0.5, 2.6, 3)
                pygame.draw.line(surface, (139, 90, 43), 
                               (center_x, y + 12), (center_x, y + size - 12), 2)
            elif 'staff' in item_name.lower():
                # Staff shape
                pygame.draw.line(surface, (139, 90, 43), 
                               (center_x, y + 8), (center_x, y + size - 8), 4)
                pygame.draw.circle(surface, (255, 215, 0), (center_x, y + 12), 6)
            else:
                # Sword shape
                pygame.draw.line(surface, (192, 192, 192), 
                               (center_x, y + 8), (center_x, y + size - 12), 3)
                pygame.draw.rect(surface, (139, 90, 43), 
                               (center_x - 4, y + size - 12, 8, 6))
                
        elif category == 'armor':
            if 'shield' in item_name.lower():
                # Shield shape
                pygame.draw.ellipse(surface, (100, 100, 100), 
                                  (x + 10, y + 10, size - 20, size - 20))
                pygame.draw.ellipse(surface, (150, 150, 150), 
                                  (x + 10, y + 10, size - 20, size - 20), 2)
            elif 'boots' in item_name.lower():
                # Boot shape
                pygame.draw.ellipse(surface, (139, 90, 43), 
                                  (x + 12, y + 18, size - 24, size - 30))
                pygame.draw.rect(surface, (139, 90, 43), 
                               (x + 12, y + 25, size - 24, 8))
            else:
                # Generic armor (chest piece)
                pygame.draw.rect(surface, (100, 100, 100), 
                               (x + 12, y + 12, size - 24, size - 24))
                pygame.draw.rect(surface, (150, 150, 150), 
                               (x + 12, y + 12, size - 24, size - 24), 2)
                
        elif category == 'accessory':
            if 'ring' in item_name.lower():
                # Ring shape
                pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), 8, 3)
                pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y - 4), 3)
            elif 'crown' in item_name.lower():
                # Crown shape
                points = [(x + 10, y + 25), (x + 15, y + 15), (x + 20, y + 20), 
                         (x + 25, y + 10), (x + 30, y + 20), (x + 35, y + 15), (x + 40, y + 25)]
                pygame.draw.polygon(surface, (255, 215, 0), points)
            else:
                # Generic accessory (crystal/orb)
                pygame.draw.polygon(surface, (100, 200, 255), 
                                  [(center_x, y + 10), (x + 12, center_y), 
                                   (center_x, y + size - 10), (x + size - 12, center_y)])
                
        elif category == 'consumable':
            if 'potion' in item_name.lower():
                # Potion bottle
                pygame.draw.rect(surface, (100, 255, 100), 
                               (x + 15, y + 15, size - 30, size - 25))
                pygame.draw.rect(surface, (50, 150, 50), 
                               (x + 17, y + 12, size - 34, 6))
            else:
                # Scroll
                pygame.draw.rect(surface, (245, 245, 220), 
                               (x + 10, y + 12, size - 20, size - 24))
                pygame.draw.line(surface, (139, 90, 43), 
                               (x + 15, y + 18), (x + size - 15, y + 18), 1)
                pygame.draw.line(surface, (139, 90, 43), 
                               (x + 15, y + 22), (x + size - 15, y + 22), 1)
                
        elif category == 'legendary':
            # Special glowing effect for legendary items
            pygame.draw.circle(surface, (255, 100, 255), (center_x, center_y), size // 2 - 2, 3)
            pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), size // 2 - 8)
            # Add sparkle effect
            for i in range(4):
                angle = i * 3.14159 / 2
                spark_x = center_x + int((size // 3) * (0.7 if i % 2 else 1) * 
                                       (1 if i < 2 else -1) * (1 if i % 2 == 0 else 0))
                spark_y = center_y + int((size // 3) * (0.7 if i % 2 else 1) * 
                                       (1 if i >= 2 else -1) * (0 if i % 2 == 0 else 1))
                pygame.draw.circle(surface, (255, 255, 255), (spark_x, spark_y), 2)
        else:
            # Misc item - simple box
            pygame.draw.rect(surface, (150, 150, 150), 
                           (x + 12, y + 12, size - 24, size - 24))
            pygame.draw.rect(surface, (200, 200, 200), 
                           (x + 12, y + 12, size - 24, size - 24), 2)

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
        # Don't open if already opening or mimic is active
        if self.chest_is_opening or self.is_mimic:
            return
            
        # Check for mimic first!
        if random.random() < self.mimic_chance:
            # It's a mimic! 
            self.is_mimic = True
            self.mimic_revealed = False
            self.mimic_timer = 0
            self.chest_is_opening = True  # Start opening animation first
            self.chest_open_timer = 0
            return
            
        # Normal chest opening
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

    def draw_mimic(self, surface):
        """Draw a scary mimic that has revealed itself"""
        x, y = self.loot_box_rect.x, self.loot_box_rect.y
        w, h = self.loot_box_rect.width, self.loot_box_rect.height
        
        # Animate the reveal
        reveal_progress = min(self.mimic_timer / 1.0, 1.0)  # 1 second to fully reveal
        
        if not self.mimic_revealed and reveal_progress < 1.0:
            # Still looks like a chest but starting to change
            self.draw_treasure_chest(surface)
            
            # Add subtle warning signs
            if reveal_progress > 0.3:
                # Eyes starting to appear
                eye_alpha = int((reveal_progress - 0.3) * 255 / 0.7)
                if eye_alpha > 0:
                    # Left eye
                    pygame.draw.circle(surface, (255, 0, 0), 
                                     (x + w//3, y + h//3), 8)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                     (x + w//3, y + h//3), 4)
                    # Right eye  
                    pygame.draw.circle(surface, (255, 0, 0), 
                                     (x + 2*w//3, y + h//3), 8)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                     (x + 2*w//3, y + h//3), 4)
            
            if reveal_progress >= 1.0:
                self.mimic_revealed = True
        else:
            # Fully revealed mimic - scary!
            shake_x = int(random.random() * 6 - 3)  # Shake effect
            shake_y = int(random.random() * 6 - 3)
            
            mimic_x = x + shake_x
            mimic_y = y + shake_y
            
            # Main mimic body (darker, more menacing)
            body_rect = pygame.Rect(mimic_x, mimic_y + h//4, w, h*3//4)
            pygame.draw.rect(surface, (60, 40, 20), body_rect)  # Dark brown
            pygame.draw.rect(surface, (80, 40, 40), body_rect, 4)  # Red-brown outline
            
            # Gaping mouth with teeth
            mouth_rect = pygame.Rect(mimic_x + 10, mimic_y + h//2, w - 20, h//3)
            pygame.draw.rect(surface, (40, 0, 0), mouth_rect)  # Dark red mouth
            
            # Sharp teeth
            teeth_count = 8
            for i in range(teeth_count):
                tooth_x = mouth_rect.x + (i * mouth_rect.width // teeth_count)
                tooth_points = [
                    (tooth_x, mouth_rect.y),
                    (tooth_x + 8, mouth_rect.y + 15),
                    (tooth_x + 16, mouth_rect.y)
                ]
                pygame.draw.polygon(surface, (255, 255, 255), tooth_points)
            
            # Evil glowing eyes
            eye_glow = int(abs(math.sin(self.mimic_timer * 10)) * 100) + 155
            # Left eye
            pygame.draw.circle(surface, (eye_glow, 50, 50), 
                             (mimic_x + w//3, mimic_y + h//4), 12)
            pygame.draw.circle(surface, (255, 0, 0), 
                             (mimic_x + w//3, mimic_y + h//4), 8)
            pygame.draw.circle(surface, (0, 0, 0), 
                             (mimic_x + w//3, mimic_y + h//4), 4)
            
            # Right eye
            pygame.draw.circle(surface, (eye_glow, 50, 50), 
                             (mimic_x + 2*w//3, mimic_y + h//4), 12)
            pygame.draw.circle(surface, (255, 0, 0), 
                             (mimic_x + 2*w//3, mimic_y + h//4), 8)
            pygame.draw.circle(surface, (0, 0, 0), 
                             (mimic_x + 2*w//3, mimic_y + h//4), 4)
            
            # Spikes and claws coming out
            for i in range(4):
                angle = i * 1.57  # 90 degrees each
                spike_x = mimic_x + w//2 + int(30 * math.cos(angle))
                spike_y = mimic_y + h//2 + int(30 * math.sin(angle))
                spike_end_x = spike_x + int(20 * math.cos(angle))
                spike_end_y = spike_y + int(20 * math.sin(angle))
                pygame.draw.line(surface, (100, 100, 100), 
                               (spike_x, spike_y), (spike_end_x, spike_end_y), 5)

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

        # Update mimic encounter
        if self.is_mimic:
            self.mimic_timer += dt
            
            # Reveal mimic after chest opening animation (ONLY ONCE!)
            if self.chest_open_timer >= 0.5 and not self.mimic_revealed:
                # Mark as revealed to prevent spam
                self.mimic_revealed = True
                
                # Surprise! Show initial mimic reveal message
                initial_roast = random.choice(self.mimic_roasts)
                self.popup_text = f"MIMIC! {initial_roast}"
                self.popup_timer = 3.0
                print(f"MIMIC ENCOUNTER! {initial_roast}")
                
            if self.mimic_timer >= self.mimic_duration:
                # Mimic encounter ends
                self.mimic_consequence()
                self.reset_mimic()

    def mimic_consequence(self):
        """Handle what happens when you encounter a mimic"""
        # Additional savage roast lines for stealing items (shorter!)
        steal_roasts = [
            "Yoink! �", 
            "Mine now! 💸",
            "Finessed! 🎭",
            "Robbery! 🔫",
            "Pickpocketed! 🕵️",
            "Nom nom! 😋",
            "Stolen! 🤲"
        ]
        
        no_items_roasts = [
            "Broke! 📊",
            "Empty! �",
            "Nothing! �",
            "Poverty! 🚫",
            "Sad! 😢"
        ]
        
        if len(self.inventory.items) > 0:
            # Mimic steals a random item with savage commentary!
            items_list = list(self.inventory.items.keys())
            stolen_item = random.choice(items_list)
            steal_roast = random.choice(steal_roasts)
            
            if self.inventory.items[stolen_item] > 1:
                self.inventory.items[stolen_item] -= 1
            else:
                del self.inventory.items[stolen_item]
            
            self.popup_text = f"Ate {stolen_item}! {steal_roast}"
            self.popup_timer = 3.0
            print(f"Mimic stole: {stolen_item} - {steal_roast}")
        else:
            # No items to steal, extra savage roast
            no_items_roast = random.choice(no_items_roasts)
            self.popup_text = f"No items! {no_items_roast}"
            self.popup_timer = 2.5
            print(f"Mimic found no items - {no_items_roast}")

    def reset_mimic(self):
        """Reset mimic state back to normal chest"""
        self.is_mimic = False
        self.mimic_revealed = False
        self.mimic_timer = 0
        self.chest_is_opening = False
        self.chest_open_timer = 0

    def draw_inventory_grid(self, surface):
        """Draw the inventory as a grid with icons"""
        # Draw background panel
        panel_width = self.inventory_grid_cols * (self.inventory_slot_size + 5) + 15
        panel_height = self.inventory_grid_rows * (self.inventory_slot_size + 5) + 60
        panel_rect = pygame.Rect(self.inventory_start_x - 10, self.inventory_start_y - 40, 
                                panel_width, panel_height)
        
        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (20, 20, 40, 200), (0, 0, panel_width, panel_height))
        pygame.draw.rect(panel_surface, (100, 100, 100), (0, 0, panel_width, panel_height), 2)
        surface.blit(panel_surface, (panel_rect.x, panel_rect.y))
        
        # Draw header
        header_font = pygame.font.SysFont(None, 36)
        header = header_font.render("Inventory", True, (255, 255, 255))
        surface.blit(header, (self.inventory_start_x, self.inventory_start_y - 30))
        
        # Draw grid slots
        items_list = list(self.inventory.items.items())
        slot_index = 0
        
        for row in range(self.inventory_grid_rows):
            for col in range(self.inventory_grid_cols):
                # Calculate slot position
                slot_x = self.inventory_start_x + col * (self.inventory_slot_size + 5)
                slot_y = self.inventory_start_y + row * (self.inventory_slot_size + 5)
                
                # Draw slot background
                slot_rect = pygame.Rect(slot_x, slot_y, self.inventory_slot_size, self.inventory_slot_size)
                pygame.draw.rect(surface, (40, 40, 60), slot_rect)
                pygame.draw.rect(surface, (80, 80, 100), slot_rect, 2)
                
                # Draw item if it exists
                if slot_index < len(items_list):
                    item_name, item_count = items_list[slot_index]
                    
                    # Draw item icon
                    icon_size = self.inventory_slot_size - 10
                    icon_x = slot_x + 5
                    icon_y = slot_y + 5
                    self.draw_item_icon(surface, item_name, icon_x, icon_y, icon_size)
                    
                    # Draw item count
                    if item_count > 1:
                        count_font = pygame.font.SysFont(None, 24)
                        count_text = count_font.render(str(item_count), True, (255, 255, 255))
                        count_bg_rect = pygame.Rect(slot_x + self.inventory_slot_size - 20, 
                                                   slot_y + self.inventory_slot_size - 20, 18, 18)
                        pygame.draw.rect(surface, (0, 0, 0, 150), count_bg_rect)
                        surface.blit(count_text, (slot_x + self.inventory_slot_size - 18, 
                                                 slot_y + self.inventory_slot_size - 18))
                    
                    # Draw item name on hover (simplified - always show for now)
                    # You could add mouse hover detection here later
                    
                slot_index += 1

    def draw(self, surface):
        surface.fill((30, 30, 60))  # background
        
        # Draw mimic or treasure chest
        if self.is_mimic and self.mimic_timer > 0.5:
            # Draw the scary mimic
            self.draw_mimic(surface)
        else:
            # Draw normal treasure chest
            self.draw_treasure_chest(surface)

        # Add a glow effect around the chest (different color for mimic)
        if self.is_mimic and self.mimic_revealed:
            # Red menacing glow for mimic
            glow_rect = pygame.Rect(self.loot_box_rect.x - 10, self.loot_box_rect.y - 10,
                                   self.loot_box_rect.width + 20, self.loot_box_rect.height + 20)
            pygame.draw.rect(surface, (150, 20, 20), glow_rect, 5)  # Red glow
        else:
            # Normal golden glow
            glow_rect = pygame.Rect(self.loot_box_rect.x - 5, self.loot_box_rect.y - 5,
                                   self.loot_box_rect.width + 10, self.loot_box_rect.height + 10)
            pygame.draw.rect(surface, (100, 80, 20), glow_rect, 3)  # Golden glow

        # Popup text
        if self.popup_text:
            text_surf = self.font.render(self.popup_text, True, (255, 255, 255))
            surface.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 100))

        # Inventory display
        if self.show_inventory:
            self.draw_inventory_grid(surface)
