# Desenvolvido com apoio de IA (Claude, da Anthropic) para estruturacao do
# codigo, revisao de logica e escrita dos testes automatizados. A escolha do
# conceito do jogo, as decisoes de design e a revisao final sao de autoria
# propria.

import random
import sys
from pathlib import Path

import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SIZE = 40
PLAYER_SPEED = 6

OBSTACLE_MIN_RADIUS = 12
OBSTACLE_MAX_RADIUS = 28
OBSTACLE_BASE_SPEED = 3
OBSTACLE_SPAWN_MS = 700

POWERUP_SIZE = 24
POWERUP_SPEED = 4
POWERUP_SPAWN_MS = 6000
POWERUP_TYPES = ("shield", "life", "multiplier")

SHIELD_DURATION_MS = 4000
MULTIPLIER_DURATION_MS = 5000
STARTING_LIVES = 3

BG_COLOR = (10, 10, 30)
PLAYER_COLOR = (80, 200, 255)
SHIELD_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 90, 90)
TEXT_COLOR = (230, 230, 230)

POWERUP_COLORS = {
    "shield": (100, 220, 255),
    "life": (120, 255, 120),
    "multiplier": (255, 210, 80),
}

HIGHSCORE_PATH = Path(__file__).parent / "highscore.txt"


def load_highscore(path):
    if not path.exists():
        return 0
    try:
        return int(path.read_text().strip())
    except (ValueError, OSError):
        return 0


def save_highscore(path, score):
    current = load_highscore(path)
    if score > current:
        path.write_text(str(score))
        return score
    return current


def spawn_obstacle(obstacles, difficulty):
    radius = random.randint(OBSTACLE_MIN_RADIUS, OBSTACLE_MAX_RADIUS)
    x = random.randint(radius, WIDTH - radius)
    speed = OBSTACLE_BASE_SPEED + difficulty * 0.4 + random.uniform(0, 1.5)
    obstacles.append({"x": x, "y": -radius, "radius": radius, "speed": speed})


def spawn_powerup(powerups):
    kind = random.choice(POWERUP_TYPES)
    x = random.randint(POWERUP_SIZE, WIDTH - POWERUP_SIZE)
    powerups.append({"x": x, "y": -POWERUP_SIZE, "type": kind})


def update_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle["y"] += obstacle["speed"]
    return [o for o in obstacles if o["y"] - o["radius"] <= HEIGHT]


def update_powerups(powerups):
    for powerup in powerups:
        powerup["y"] += POWERUP_SPEED
    return [p for p in powerups if p["y"] - POWERUP_SIZE <= HEIGHT]


def check_collision(player_rect, obstacles):
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(
            obstacle["x"] - obstacle["radius"],
            obstacle["y"] - obstacle["radius"],
            obstacle["radius"] * 2,
            obstacle["radius"] * 2,
        )
        if player_rect.colliderect(obstacle_rect):
            return obstacle
    return None


def check_powerup_collision(player_rect, powerups):
    for powerup in powerups:
        powerup_rect = pygame.Rect(
            powerup["x"] - POWERUP_SIZE // 2,
            powerup["y"] - POWERUP_SIZE // 2,
            POWERUP_SIZE,
            POWERUP_SIZE,
        )
        if player_rect.colliderect(powerup_rect):
            return powerup
    return None


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_hud(screen, font, score, lives, highscore):
    score_surface = font.render(f"Pontos: {score}", True, TEXT_COLOR)
    lives_surface = font.render(f"Vidas: {lives}", True, TEXT_COLOR)
    highscore_surface = font.render(f"Recorde: {highscore}", True, TEXT_COLOR)
    screen.blit(score_surface, (16, 12))
    screen.blit(lives_surface, (16, 44))
    screen.blit(highscore_surface, (WIDTH - highscore_surface.get_width() - 16, 12))


def run_menu(screen, clock, font, big_font, highscore):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)
        title = big_font.render("STAR DODGE", True, PLAYER_COLOR)
        prompt = font.render("Pressione ESPACO para jogar", True, TEXT_COLOR)
        quit_hint = font.render("ESC para sair", True, TEXT_COLOR)
        record = font.render(f"Recorde atual: {highscore}", True, TEXT_COLOR)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(record, record.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        screen.blit(quit_hint, quit_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))

        pygame.display.flip()
        clock.tick(FPS)


def run_game_over(screen, clock, font, big_font, score, highscore):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)
        title = big_font.render("FIM DE JOGO", True, OBSTACLE_COLOR)
        score_line = font.render(f"Pontuacao: {score}", True, TEXT_COLOR)
        highscore_line = font.render(f"Recorde: {highscore}", True, TEXT_COLOR)
        restart_hint = font.render("R para jogar novamente | ESC para sair", True, TEXT_COLOR)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        screen.blit(score_line, score_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(highscore_line, highscore_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        screen.blit(restart_hint, restart_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))

        pygame.display.flip()
        clock.tick(FPS)


def run_game(screen, clock, font, highscore):
    player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 80, PLAYER_SIZE, PLAYER_SIZE)
    obstacles = []
    powerups = []

    score = 0
    lives = STARTING_LIVES
    difficulty = 0

    shield_until = 0
    multiplier_until = 0

    last_obstacle_spawn = pygame.time.get_ticks()
    last_powerup_spawn = pygame.time.get_ticks()
    start_ticks = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += PLAYER_SPEED

        player.x = clamp(player.x, 0, WIDTH - PLAYER_SIZE)
        player.y = clamp(player.y, 0, HEIGHT - PLAYER_SIZE)

        difficulty = (now - start_ticks) // 5000

        if now - last_obstacle_spawn >= max(250, OBSTACLE_SPAWN_MS - difficulty * 40):
            spawn_obstacle(obstacles, difficulty)
            last_obstacle_spawn = now

        if now - last_powerup_spawn >= POWERUP_SPAWN_MS:
            spawn_powerup(powerups)
            last_powerup_spawn = now

        obstacles = update_obstacles(obstacles)
        powerups = update_powerups(powerups)

        hit_powerup = check_powerup_collision(player, powerups)
        if hit_powerup:
            powerups.remove(hit_powerup)
            if hit_powerup["type"] == "shield":
                shield_until = now + SHIELD_DURATION_MS
            elif hit_powerup["type"] == "life":
                lives += 1
            elif hit_powerup["type"] == "multiplier":
                multiplier_until = now + MULTIPLIER_DURATION_MS

        shielded = now < shield_until
        hit_obstacle = check_collision(player, obstacles)
        if hit_obstacle and not shielded:
            obstacles.remove(hit_obstacle)
            lives -= 1
            if lives <= 0:
                return score

        points_this_frame = 2 if now < multiplier_until else 1
        score += points_this_frame

        screen.fill(BG_COLOR)

        player_color = SHIELD_COLOR if shielded else PLAYER_COLOR
        pygame.draw.rect(screen, player_color, player, border_radius=8)

        for obstacle in obstacles:
            pygame.draw.circle(
                screen, OBSTACLE_COLOR, (obstacle["x"], int(obstacle["y"])), obstacle["radius"]
            )

        for powerup in powerups:
            color = POWERUP_COLORS[powerup["type"]]
            rect = pygame.Rect(0, 0, POWERUP_SIZE, POWERUP_SIZE)
            rect.center = (powerup["x"], int(powerup["y"]))
            pygame.draw.rect(screen, color, rect, border_radius=6)

        draw_hud(screen, font, score, lives, highscore)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Star Dodge")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big_font = pygame.font.SysFont("arial", 48, bold=True)

    highscore = load_highscore(HIGHSCORE_PATH)

    while True:
        run_menu(screen, clock, font, big_font, highscore)
        score = run_game(screen, clock, font, highscore)
        highscore = save_highscore(HIGHSCORE_PATH, score)
        run_game_over(screen, clock, font, big_font, score, highscore)


if __name__ == "__main__":
    main()