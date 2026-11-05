import pygame
import random
from pathlib import Path
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
NAVY = (8, 14, 35)
CYAN = (90, 220, 255)
DIFFICULTIES = {
    pygame.K_1: ("Easy", 1.0, 0.004),
    pygame.K_2: ("Medium", 1.5, 0.01),
    pygame.K_3: ("Hard", 2.5, 0.02),
}


class GameEngine:
    """Own the Space Invaders game state, rules, and rendering."""

    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self._load_sounds()
        self.reset(difficulty)

    def _load_sounds(self):
        """Load packaged effects when an audio device is available."""
        self.sounds = {}
        if pygame.mixer.get_init() is None:
            return
        asset_dir = Path(__file__).parent / "assets"
        for name in ("shoot", "hit", "game_over"):
            try:
                self.sounds[name] = pygame.mixer.Sound(asset_dir / f"{name}.wav")
            except (pygame.error, OSError):
                continue

    def _play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def reset(self, difficulty="Medium"):
        """Start a new run with the selected enemy speed and fire rate."""
        profiles = {
            "Easy": (1.0, 0.004),
            "Medium": (1.5, 0.01),
            "Hard": (2.5, 0.02),
        }
        if difficulty not in profiles:
            difficulty = "Medium"
        enemy_speed, self.enemy_fire_chance = profiles[difficulty]
        self.difficulty = difficulty
        self.player = Player(self.width // 2 - 20, self.height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(self.width, speed=enemy_speed)
        self.player_bullets = []
        self.enemy_bullets = []
        self._shoot_cooldown = 0
        self.score = 0
        self.game_over = False
        self.won = False

    def handle_event(self, event):
        """Handle shooting, replay selection, and window-close events."""
        if event.type == pygame.QUIT:
            return False
        if event.type != pygame.KEYDOWN:
            return True

        if self.game_over:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r:
                self.reset(self.difficulty)
            elif event.key in DIFFICULTIES:
                self.reset(DIFFICULTIES[event.key][0])
            return True

        if event.key == pygame.K_SPACE and self._shoot_cooldown <= 0:
            bullet_x = self.player.center_x() - 2
            self.player_bullets.append(
                Bullet(bullet_x, self.player.y, direction=-1)
            )
            self._shoot_cooldown = 15
            self._play_sound("shoot")
        return True

    def handle_input(self):
        """Move the ship with the arrow keys or A and D."""
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-self.player.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(self.player.speed, self.width)

    def _finish(self, won=False):
        self.game_over = True
        self.won = won
        self._play_sound("game_over")

    def update(self):
        """Advance entities and resolve collisions without skipping bullets."""
        if self.game_over:
            return
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        self.enemy_grid.move()
        for enemy in self.enemy_grid.alive_enemies():
            if random.random() < self.enemy_fire_chance:
                bullet_x = enemy.x + enemy.width // 2
                self.enemy_bullets.append(
                    Bullet(bullet_x, enemy.y + enemy.height, direction=1)
                )

        for bullet in self.player_bullets:
            bullet.move()
        for bullet in self.enemy_bullets:
            bullet.move()
        self.player_bullets = [
            bullet for bullet in self.player_bullets
            if not bullet.off_screen(self.height)
        ]
        self.enemy_bullets = [
            bullet for bullet in self.enemy_bullets
            if not bullet.off_screen(self.height)
        ]

        consumed_bullets = set()
        for bullet in tuple(self.player_bullets):
            for enemy in self.enemy_grid.alive_enemies():
                if bullet.rect().colliderect(enemy.rect()):
                    enemy.alive = False
                    consumed_bullets.add(id(bullet))
                    self.score += 1
                    self._play_sound("hit")
                    break
        self.player_bullets = [
            bullet for bullet in self.player_bullets
            if id(bullet) not in consumed_bullets
        ]

        for bullet in self.enemy_bullets:
            if bullet.rect().colliderect(self.player.rect()):
                self._finish()
                break

        if not self.game_over:
            if not self.enemy_grid.alive_enemies():
                self._finish(won=True)
            elif self.enemy_grid.reached_bottom(self.player.y):
                self._finish()

    def _draw_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))
        headline = "YOU WIN" if self.won else "GAME OVER"
        title = self.title_font.render(headline, True, CYAN if self.won else RED)
        screen.blit(title, title.get_rect(center=(self.width // 2, 250)))
        final_score = self.font.render(
            f"Final score: {self.score}", True, WHITE
        )
        screen.blit(final_score, final_score.get_rect(center=(self.width // 2, 315)))
        prompt = self.small_font.render(
            "Play again? Choose difficulty:", True, WHITE
        )
        screen.blit(prompt, prompt.get_rect(center=(self.width // 2, 390)))
        options = self.small_font.render(
            "1  Easy       2  Medium       3  Hard", True, CYAN
        )
        screen.blit(options, options.get_rect(center=(self.width // 2, 430)))
        replay = self.small_font.render(
            "R  Replay same level       Esc  Exit", True, WHITE
        )
        screen.blit(replay, replay.get_rect(center=(self.width // 2, 470)))

    def render(self, screen):
        """Draw the game scene and an in-window final-score screen."""
        screen.fill(NAVY)
        pygame.draw.rect(screen, GREEN, self.player.rect())
        for enemy in self.enemy_grid.alive_enemies():
            pygame.draw.rect(screen, WHITE, enemy.rect())
        for bullet in self.player_bullets:
            pygame.draw.rect(screen, WHITE, bullet.rect())
        for bullet in self.enemy_bullets:
            pygame.draw.rect(screen, RED, bullet.rect())
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.small_font.render(
            f"Difficulty: {self.difficulty}", True, CYAN
        )
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 48))
        if self.game_over:
            self._draw_game_over(screen)
