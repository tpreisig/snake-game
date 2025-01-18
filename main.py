import pygame
from pygame import Vector2
from random import randrange
import config
import pygame.freetype

pygame.init()

# pygame.mixer.init()
# pygame.mixer.music.load("audio/game_music.wav")
# pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))
clock = pygame.time.Clock()


# flagto start (flag begin, flag bait)
running = True
begin = True
bait = True

time = None
snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None

food_rect = None

score = 0
font = pygame.freetype.SysFont(None, 24)

# begin and bait flags to manage initialization
while running:
    if begin:
        begin = False
        time = 0
        snake_rect = pygame.rect.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
             config.SNAKE_PART_SIZE,
             config.SNAKE_PART_SIZE])
        snake_length = 1
        snake_parts = []
        snake_direction = Vector2(0, 0)

    if bait:
        bait = False
        food_rect = pygame.rect.Rect(randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                     randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE),
                                     config.FOOD_SIZE,
                                     config.FOOD_SIZE)

    for event in pygame.event.get():
        # quit event or escape key press
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
        # Movement Direction Constraints
        if event.type == pygame.KEYDOWN:
            # no immediate reversing of the snake's movement
            if event.key == pygame.K_UP and snake_direction != Vector2(0, config.SNAKE_MOVE_LENGTH):
                snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_DOWN and snake_direction != Vector2(0, -config.SNAKE_MOVE_LENGTH):
                snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_RIGHT and snake_direction != Vector2(-config.SNAKE_MOVE_LENGTH, 0):
                snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)
            if event.key == pygame.K_LEFT and snake_direction != Vector2(config.SNAKE_MOVE_LENGTH, 0):
                snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)

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

        # Check for collision with walls
        if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
                snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE):
            running = False

        # Check for collision with itself
        if snake_parts.count(snake_rect) > 1:
            running = False

    pygame.draw.rect(screen, config.FOOD_COLOR, food_rect)

    [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part) for snake_part in snake_parts]

    # Python method to detect if two rectangles have collided: colliderect()
    # when snake collides with food, the snake grows...
    if snake_rect.colliderect(food_rect):
        snake_length += 1
        score += 1
        # ...and a new food piece is placed.
        bait = True
    
    # draw score on screen
    score_text = f"Score: {score}"
    rect = font.get_rect(score_text)
    rect.topleft = (24, 21)
    font.render_to(screen, rect, score_text, config.SCORE_COLOR )

    # update the full display window
    pygame.display.flip()

    # run game at a consistent frame rate
    clock.tick(config.FPS)

pygame.quit()