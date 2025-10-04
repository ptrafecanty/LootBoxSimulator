import pygame
from lootbox_sim.menu import MenuScreen
from lootbox_sim.game_screen import GameScreen  # Phase 2 screen

def run_game():
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Loot Box Simulator")
    clock = pygame.time.Clock()
    FPS = 60

    current_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                action = current_screen.handle_event(event)

                if action == "start_game":
                    current_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
                elif action == "quit":
                    running = False

        current_screen.update(dt)

        screen.fill((50, 50, 50))
        current_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()
