import pygame
from pygame import Vector2
from random import randrange
import config
import pygame.freetype  # For text rendering

pygame.init()
pygame.mixer.init()

# Load and play music
try:
    extend_sound = pygame.mixer.Sound("audio/ext.mp3")
    pygame.mixer.music.load("audio/bg_sound.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except pygame.error:
    print("Warning: Audio files not found. Running without sound.")
    extend_sound = None


screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score and game over message
font = pygame.freetype.SysFont(None, 46)

running = True
begin = True
bait = True
game_over = False

time = None
snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None
food_rect = None
score = 0

while running:
    if begin:
        begin = False
        game_over = False
        time = 0
        snake_rect = pygame.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             config.SNAKE_PART_SIZE,
             config.SNAKE_PART_SIZE])
        snake_length = 1
        snake_parts = []
        snake_direction = Vector2(0, 0)
        score = 0

    if bait:
        bait = False
        food_rect = pygame.Rect(randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                config.FOOD_SIZE,
                                config.FOOD_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN and game_over:
            begin = False  # Restart the game if game over and key pressed
        # Movement Direction Constraints (only if game is not over)
        elif not game_over:
            if event.type == pygame.KEYDOWN:
                # ... (keep your existing key handling code here)
                if event.key == pygame.K_UP and snake_direction != Vector2(0, config.SNAKE_MOVE_LENGTH):
                    snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
                if event.key == pygame.K_DOWN and snake_direction != Vector2(0, -config.SNAKE_MOVE_LENGTH):
                    snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
                if event.key == pygame.K_RIGHT and snake_direction != Vector2(-config.SNAKE_MOVE_LENGTH, 0):
                    snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)
                if event.key == pygame.K_LEFT and snake_direction != Vector2(config.SNAKE_MOVE_LENGTH, 0):
                    snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)

    if not game_over:
        time_now = pygame.time.get_ticks()

        screen.fill(config.BG_COLOR)
        for n in range(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE):
            pygame.draw.line(screen, config.GRID_COLOR, (n, 0), (n, config.SCREEN_SIZE))
            pygame.draw.line(screen, config.GRID_COLOR, (0, n), (config.SCREEN_SIZE, n))

        if time_now - time > config.DELAY:
            time = time_now
            snake_rect.move_ip(snake_direction)
            snake_parts.append(snake_rect.copy())
            snake_parts = snake_parts[-snake_length:]

            # Check for collision with walls or itself
            if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
                snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE) or snake_parts.count(snake_rect) > 1:
                game_over = True

        pygame.draw.rect(screen, config.FOOD_COLOR, food_rect)
        [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part) for snake_part in snake_parts]

        if snake_rect.colliderect(food_rect):
            snake_length += 1
            if extend_sound:
                extend_sound.set_volume(1.0)
                extend_sound.play()
            bait = True
            score += 1  # Increment score

        # Draw current score
        score_text = f"** Score {score} **"
        rect = font.get_rect(score_text)
        rect.center = (config.SCREEN_SIZE/2, config.SCREEN_SIZE/10)  # Position score text
        font.render_to(screen, rect, score_text, config.SCORE_COLOR)

    else:
        # Game Over Screen
        screen.fill(config.BG_COLOR)
        game_over_text = f"Game Over! Final Score: {score}"
        rect = font.get_rect(game_over_text)
        rect.center = (config.SCREEN_SIZE / 2, config.SCREEN_SIZE / 2 - 32)
        font.render_to(screen, rect, game_over_text, config.SCORE_COLOR)
        restart_text = "Press any key to restart"
        rect = font.get_rect(restart_text)
        rect.center = (config.SCREEN_SIZE / 2, config.SCREEN_SIZE / 2 + 32)
        font.render_to(screen, rect, restart_text, config.SCORE_COLOR)

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()