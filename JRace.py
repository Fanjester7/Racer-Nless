import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
RED        = (220, 50, 50)
BLUE       = (50, 100, 220)
YELLOW     = (255, 220, 0)
GRAY       = (100, 100, 100)
DARK_GRAY  = (50, 50, 50)
GREEN      = (50, 200, 50)
ORANGE     = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)
ASPHALT    = (60, 60, 70)
LINE_WHITE = (240, 240, 240)

# Road settings
ROAD_LEFT  = 100
ROAD_RIGHT = 500
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Lane centers
LANES = [160, 250, 340, 430]

# ─── Player Car ──────────────────────────────────────────────────────────────
class PlayerCar:
    WIDTH  = 50
    HEIGHT = 90

    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - self.WIDTH // 2
        self.y = SCREEN_HEIGHT - 150
        self.speed = 6
        self.lane_index = 1
        self.x = LANES[self.lane_index] - self.WIDTH // 2
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def move_left(self):
        if self.lane_index > 0:
            self.lane_index -= 1

    def move_right(self):
        if self.lane_index < len(LANES) - 1:
            self.lane_index += 1

    def update(self):
        target_x = LANES[self.lane_index] - self.WIDTH // 2
        if self.x < target_x:
            self.x = min(self.x + 10, target_x)
        elif self.x > target_x:
            self.x = max(self.x - 10, target_x)
        self.rect.x = int(self.x)
        self.rect.y = self.y

    def draw(self, screen):
        x, y = int(self.x), self.y
        w, h = self.WIDTH, self.HEIGHT

        # Car body
        pygame.draw.rect(screen, BLUE, (x + 5, y + 10, w - 10, h - 20), border_radius=8)
        # Roof
        pygame.draw.rect(screen, (30, 70, 180), (x + 10, y + 20, w - 20, 35), border_radius=6)
        # Windshield front
        pygame.draw.rect(screen, LIGHT_BLUE, (x + 12, y + 22, w - 24, 16), border_radius=4)
        # Windshield back
        pygame.draw.rect(screen, LIGHT_BLUE, (x + 12, y + 40, w - 24, 12), border_radius=4)
        # Headlights
        pygame.draw.rect(screen, YELLOW, (x + 6,  y + 12, 12, 8), border_radius=3)
        pygame.draw.rect(screen, YELLOW, (x + w - 18, y + 12, 12, 8), border_radius=3)
        # Taillights
        pygame.draw.rect(screen, RED, (x + 6,  y + h - 18, 12, 8), border_radius=3)
        pygame.draw.rect(screen, RED, (x + w - 18, y + h - 18, 12, 8), border_radius=3)
        # Wheels
        wheel_color = BLACK
        pygame.draw.rect(screen, wheel_color, (x - 6,  y + 15, 12, 22), border_radius=4)
        pygame.draw.rect(screen, wheel_color, (x + w - 6, y + 15, 12, 22), border_radius=4)
        pygame.draw.rect(screen, wheel_color, (x - 6,  y + h - 35, 12, 22), border_radius=4)
        pygame.draw.rect(screen, wheel_color, (x + w - 6, y + h - 35, 12, 22), border_radius=4)


# ─── Enemy Car ───────────────────────────────────────────────────────────────
ENEMY_COLORS = [RED, GREEN, ORANGE, (180, 0, 180), (0, 180, 180)]

class EnemyCar:
    WIDTH  = 50
    HEIGHT = 90

    def __init__(self, speed):
        self.lane_index = random.randint(0, len(LANES) - 1)
        self.x = LANES[self.lane_index] - self.WIDTH // 2
        self.y = -self.HEIGHT - random.randint(0, 200)
        self.speed = speed
        self.color = random.choice(ENEMY_COLORS)
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self, game_speed):
        self.y += self.speed + game_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 20

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        w, h = self.WIDTH, self.HEIGHT
        c = self.color

        # Car body
        pygame.draw.rect(screen, c, (x + 5, y + 10, w - 10, h - 20), border_radius=8)
        # Roof
        dark_c = tuple(max(0, v - 50) for v in c)
        pygame.draw.rect(screen, dark_c, (x + 10, y + 20, w - 20, 35), border_radius=6)
        # Windshields
        pygame.draw.rect(screen, LIGHT_BLUE, (x + 12, y + 22, w - 24, 16), border_radius=4)
        pygame.draw.rect(screen, LIGHT_BLUE, (x + 12, y + 40, w - 24, 12), border_radius=4)
        # Headlights
        pygame.draw.rect(screen, YELLOW, (x + 6,      y + 12, 12, 8), border_radius=3)
        pygame.draw.rect(screen, YELLOW, (x + w - 18, y + 12, 12, 8), border_radius=3)
        # Taillights
        pygame.draw.rect(screen, RED, (x + 6,      y + h - 18, 12, 8), border_radius=3)
        pygame.draw.rect(screen, RED, (x + w - 18, y + h - 18, 12, 8), border_radius=3)
        # Wheels
        pygame.draw.rect(screen, BLACK, (x - 6,      y + 15,     12, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (x + w - 6,  y + 15,     12, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (x - 6,      y + h - 35, 12, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (x + w - 6,  y + h - 35, 12, 22), border_radius=4)


# ─── Road Marking ────────────────────────────────────────────────────────────
class RoadMark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, speed):
        self.y += speed

    def draw(self, screen):
        pygame.draw.rect(screen, LINE_WHITE, (self.x - 3, int(self.y), 6, 40), border_radius=2)


# ─── Game ────────────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏎  JRace")
        self.clock  = pygame.time.Clock()

        self.font_big   = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 22)

        self.reset()

    # ── helpers ─────────────────────────────────────────────────────────────
    def reset(self):
        self.player      = PlayerCar()
        self.enemies     = []
        self.road_marks  = []
        self.score       = 0
        self.high_score  = getattr(self, "high_score", 0)
        self.game_speed  = 4
        self.enemy_speed = 3
        self.spawn_timer = 0
        self.spawn_interval = 80   # frames
        self.state       = "menu"  # menu | playing | dead

        # Seed road markings
        lane_dividers = [210, 295, 380]
        for xd in lane_dividers:
            for row in range(10):
                self.road_marks.append(RoadMark(xd, row * 120 - 60))

    # ── road drawing ─────────────────────────────────────────────────────────
    def draw_road(self):
        # Sky / background
        self.screen.fill((30, 30, 40))

        # Grass left & right
        pygame.draw.rect(self.screen, (30, 90, 30), (0, 0, ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (30, 90, 30), (ROAD_RIGHT, 0, SCREEN_WIDTH - ROAD_RIGHT, SCREEN_HEIGHT))

        # Asphalt
        pygame.draw.rect(self.screen, ASPHALT, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # Road edges
        pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT - 5, 0, 8, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (ROAD_RIGHT - 3, 0, 8, SCREEN_HEIGHT))

        # Lane dividers (dashed lines)
        for mark in self.road_marks:
            mark.draw(self.screen)

    # ── UI ───────────────────────────────────────────────────────────────────
    def draw_hud(self):
        # Score
        score_surf = self.font_med.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (12, 12))
        # Speed
        speed_surf = self.font_small.render(f"Speed: {int(self.game_speed * 20)} km/h", True, YELLOW)
        self.screen.blit(speed_surf, (12, 52))
        # High score
        hs_surf = self.font_small.render(f"Best: {self.high_score}", True, (200, 200, 200))
        self.screen.blit(hs_surf, (SCREEN_WIDTH - 130, 12))

    def draw_menu(self):
        self.draw_road()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title = self.font_big.render("🏎  JRace", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        sub = self.font_med.render("RACING GAME", True, WHITE)
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 280))

        info = self.font_small.render("← → Arrow Keys  |  SPACE to start", True, (200, 200, 200))
        self.screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 380))

        btn = self.font_med.render("[ PRESS SPACE ]", True, GREEN)
        self.screen.blit(btn, (SCREEN_WIDTH // 2 - btn.get_width() // 2, 460))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        go = self.font_big.render("GAME OVER", True, RED)
        self.screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, 220))

        sc = self.font_med.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(sc, (SCREEN_WIDTH // 2 - sc.get_width() // 2, 310))

        hs = self.font_med.render(f"Best:  {self.high_score}", True, YELLOW)
        self.screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 360))

        restart = self.font_small.render("SPACE = Restart  |  ESC = Quit", True, (200, 200, 200))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 440))

    # ── main loop ────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS)

            # ── Events ──────────────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if self.state == "menu":
                        if event.key == pygame.K_SPACE:
                            self.state = "playing"

                    elif self.state == "playing":
                        if event.key == pygame.K_LEFT:
                            self.player.move_left()
                        if event.key == pygame.K_RIGHT:
                            self.player.move_right()

                    elif self.state == "dead":
                        if event.key == pygame.K_SPACE:
                            self.reset()
                            self.state = "playing"

            # ── Menu ────────────────────────────────────────────────────────
            if self.state == "menu":
                self.draw_menu()
                pygame.display.flip()
                continue

            # ── Playing ─────────────────────────────────────────────────────
            if self.state == "playing":
                # Update road marks
                for mark in self.road_marks:
                    mark.update(self.game_speed)
                    if mark.y > SCREEN_HEIGHT + 10:
                        mark.y -= 1200

                # Spawn enemies
                self.spawn_timer += 1
                if self.spawn_timer >= self.spawn_interval:
                    self.spawn_timer = 0
                    new_enemy = EnemyCar(self.enemy_speed)
                    # avoid stacking in same lane right away
                    occupied = {e.lane_index for e in self.enemies if e.y < 200}
                    attempts = 0
                    while new_enemy.lane_index in occupied and attempts < 10:
                        new_enemy.lane_index = random.randint(0, len(LANES) - 1)
                        new_enemy.x = LANES[new_enemy.lane_index] - new_enemy.WIDTH // 2
                        attempts += 1
                    self.enemies.append(new_enemy)

                # Update enemies
                for e in self.enemies:
                    e.update(self.game_speed)

                self.enemies = [e for e in self.enemies if not e.is_off_screen()]

                # Update player
                self.player.update()

                # Collision detection
                for e in self.enemies:
                    if self.player.rect.inflate(-10, -10).colliderect(e.rect.inflate(-10, -10)):
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.state = "dead"

                # Score & difficulty ramp
                self.score += 1
                if self.score % 300 == 0:
                    self.game_speed  = min(self.game_speed  + 0.5, 15)
                    self.enemy_speed = min(self.enemy_speed + 0.3, 8)
                    self.spawn_interval = max(35, self.spawn_interval - 5)

            # ── Draw ────────────────────────────────────────────────────────
            self.draw_road()

            for e in self.enemies:
                e.draw(self.screen)

            self.player.draw(self.screen)
            self.draw_hud()

            if self.state == "dead":
                self.draw_game_over()

            pygame.display.flip()


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    game = Game()
    game.run()
