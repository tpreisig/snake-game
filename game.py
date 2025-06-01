import pygame
from pygame import Vector2
from random import randrange
import config
import pygame.freetype

pygame.init()
pygame.mixer.init()

try:
    extend_sound = pygame.mixer.Sound("audio/pop.mp3")
    pygame.mixer.music.load("audio/bg_sound.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except FileNotFoundError:
    print("Warning: Audio files not found. Running without sound.")
    extend_sound = None


screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

gradient_surface = pygame.Surface((config.SCREEN_SIZE, config.SCREEN_SIZE))
# Function to create a gradient
def create_linear_gradient(surface, start_color, end_color):
    width, height = surface.get_size()
    # interpolation
    for y in range(height):
        t = y / (height -1)
        r = int(start_color[0] + t * (end_color[0] - start_color[0]))
        b = int(start_color[1] + t * (end_color[1] - start_color[1]))
        g = int(start_color[2] + t * (end_color[2] - start_color[2]))
        pygame.draw.line(surface, (r, g, b), (0, y), (width - 1, y))

# Generate the gradient once (since it doesn't change)
create_linear_gradient(gradient_surface, config.COLOR_START, config.COLOR_END)



font = pygame.freetype.SysFont(None, 54)


running = True
begin = True
bait = True
game_over = False
game_over_time = None

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
        snake_rect = pygame.rect.Rect(
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
        food_rect = pygame.rect.Rect(randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                     randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                     config.FOOD_SIZE,
                                     config.FOOD_SIZE)

    for event in pygame.event.get():
        # Quit event or escape key press
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if pygame.time.get_ticks() - game_over_time > 600:
                    begin = True  # Restart game
            else:
                # Movement Direction Constraints
                if event.key == pygame.K_UP and snake_direction != Vector2(0, config.SNAKE_MOVE_LENGTH):
                    snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
                elif event.key == pygame.K_DOWN and snake_direction != Vector2(0, -config.SNAKE_MOVE_LENGTH):
                    snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
                elif event.key == pygame.K_RIGHT and snake_direction != Vector2(-config.SNAKE_MOVE_LENGTH, 0):
                    snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)
                elif event.key == pygame.K_LEFT and snake_direction != Vector2(config.SNAKE_MOVE_LENGTH, 0):
                    snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)

    if not game_over:
        time_now = pygame.time.get_ticks()
        screen.blit(gradient_surface, (0, 0))
        
        for n in range(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE):
            pygame.draw.line(screen, config.GRID_COLOR, (n, 0), (n, config.SCREEN_SIZE))
            pygame.draw.line(screen, config.GRID_COLOR, (0, n), (config.SCREEN_SIZE, n))

        if time_now - time > config.DELAY:
            time = time_now
            snake_rect.move_ip(snake_direction)
            snake_parts.append(snake_rect.copy())
            snake_parts = snake_parts[-snake_length:]

            # Check for collision with walls or iteself
            if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
                    snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE) or snake_parts.count(snake_rect) > 1:
                game_over = True
                game_over_time = pygame.time.get_ticks()  # record when game over occurred

        pygame.draw.rect(screen, config.FOOD_COLOR, food_rect)
        [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part) for snake_part in snake_parts]

        # Python method to detect if two rectangles have collided: colliderect()
        # when snake collides with food, the snake grows...
        if snake_rect.colliderect(food_rect):
            snake_length += 1
            score += 1
            if extend_sound:
                extend_sound.play()
            # ...and a new food piece is placed to a new random location
            bait = True

        # draw score on screen
        score_text = f"Score: {score}"
        rect = font.get_rect(score_text)
        rect.topleft = (31, 21)
        font.render_to(screen, rect, score_text, config.SCORE_COLOR )

    else:
        # Game Over Screen
        screen.fill(config.BG_COLOR)
        game_over_text = f"Game Over! Final Score: {score}"
        rect = font.get_rect(game_over_text)
        rect.center = (config.SCREEN_SIZE // 2, config.SCREEN_SIZE // 2)
        font.render_to(screen, rect, game_over_text, config.SCORE_COLOR)
        restart_text = "Press any key to restart"
        rect = font.get_rect(restart_text)
        rect.center = (config.SCREEN_SIZE // 2, config.SCREEN_SIZE // 2 + 69)
        font.render_to(screen, rect, restart_text, config.SCORE_COLOR)

    # update the full display window
    pygame.display.flip()

    # run game at a consistent frame rate
    clock.tick(config.FPS)

pygame.quit()
