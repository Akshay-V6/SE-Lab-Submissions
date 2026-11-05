"""Launch the Space Invaders game."""

import pygame
from game.game_engine import GameEngine

WIDTH, HEIGHT = 600, 700
FPS = 60
BLACK = (0, 0, 0)


def main():
    """Initialize Pygame and run until the player exits."""
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        # Gameplay remains available on machines without an audio device.
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            running = engine.handle_event(event) and running
        engine.handle_input()
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
