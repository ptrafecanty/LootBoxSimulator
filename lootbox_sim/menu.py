import pygame

class MenuScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 64)

        # Buttons
        self.buttons = {
            "Start": pygame.Rect(width//2 - 100, height//2 - 50, 200, 60),
            "Exit": pygame.Rect(width//2 - 100, height//2 + 50, 200, 60)
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.buttons["Start"].collidepoint(pos):
                return "start_game"
            elif self.buttons["Exit"].collidepoint(pos):
                return "quit"
        return None

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((20, 20, 40))
        title_surf = self.font.render("Loot Box Simulator", True, (255, 255, 255))
        surface.blit(title_surf, (self.width//2 - title_surf.get_width()//2, 100))

        for text, rect in self.buttons.items():
            pygame.draw.rect(surface, (200, 200, 50), rect)
            text_surf = self.font.render(text, True, (0, 0, 0))
            surface.blit(text_surf, (rect.x + rect.width//2 - text_surf.get_width()//2,
                                     rect.y + rect.height//2 - text_surf.get_height()//2))
