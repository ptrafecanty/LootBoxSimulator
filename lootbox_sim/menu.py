import pygame

class MenuScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.start_button = pygame.Rect(width//2 - 100, height//2 - 50, 200, 60)
        self.exit_button = pygame.Rect(width//2 - 100, height//2 + 50, 200, 60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.start_button.collidepoint(mouse_pos):
                return "start_game"
            elif self.exit_button.collidepoint(mouse_pos):
                return "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
        return None

    def update(self, dt):
        pass

    def draw(self, surface):
        title_surface = self.font.render("Loot Box Simulator", True, (255, 215, 0))
        surface.blit(title_surface, (self.width//2 - title_surface.get_width()//2, 100))

        pygame.draw.rect(surface, (100, 200, 100), self.start_button)
        pygame.draw.rect(surface, (200, 100, 100), self.exit_button)

        start_text = self.button_font.render("Start", True, (0, 0, 0))
        exit_text = self.button_font.render("Exit", True, (0, 0, 0))
        surface.blit(start_text, (self.start_button.centerx - start_text.get_width()//2,
                                  self.start_button.centery - start_text.get_height()//2))
        surface.blit(exit_text, (self.exit_button.centerx - exit_text.get_width()//2,
                                 self.exit_button.centery - exit_text.get_height()//2))
