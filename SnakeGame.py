import pygame
from random import randrange

WINDOW = 900
TILE_SIZE = 18
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

pygame.init()

snake = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

food = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food.center = get_random_position()

score = 0
font = pygame.font.SysFont(None, 48)

screen = pygame.display.set_mode([WINDOW] * 2)
clock = pygame.time.Clock()

def display_score():
    score_text = font.render(f'Score: {score}', True, pygame.Color('white'))
    screen.blit(score_text, (10, 10))

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake_dir != (0, TILE_SIZE):
                snake_dir = (0, -TILE_SIZE)
            if event.key == pygame.K_s and snake_dir != (0, -TILE_SIZE):
                snake_dir = (0, TILE_SIZE)
            if event.key == pygame.K_a and snake_dir != (TILE_SIZE, 0):
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pygame.K_d and snake_dir != (-TILE_SIZE, 0):
                snake_dir = (TILE_SIZE, 0)

    snake.move_ip(snake_dir)
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW:
        exit()

    segments.append(snake.copy())
    segments = segments[-length:]

    if snake.colliderect(food):
        food.center = get_random_position()
        length += 1
        score += 1

    if len(segments) != len(set((seg.left, seg.top) for seg in segments)):
        exit()

    screen.fill('black')

    pygame.draw.rect(screen, 'red', food)

    [pygame.draw.rect(screen, 'green', segment) for segment in segments]

    display_score()

    pygame.display.flip()

    if score < 10:
        speed = 10
    elif score < 30:
        speed = 15
    elif score < 150:
        speed = 20
    else:
        speed = 25

    clock.tick(speed)
