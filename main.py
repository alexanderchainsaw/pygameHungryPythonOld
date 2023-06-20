import random
import sys
import time
import pygame
from collections import deque

WIDTH = 1000
HEIGHT = 720
PIXEL_SIZE = 40
LINE_WIDTH = 1

SCOPE_X = (0, 24)
SCOPE_Y = (0, 17)

BACKGROUND = pygame.image.load('Assets/Background.png')
BODY = pygame.image.load('Assets/PythonBody.png')
HEAD = pygame.image.load('Assets/PythonHead.png')
cplus = pygame.image.load('Assets/cplusplus.png')
csharp = pygame.image.load('Assets/csharp.png')
js = pygame.image.load('Assets/js.png')
java = pygame.image.load('Assets/java.png')
ruby = pygame.image.load('Assets/ruby.png')
golang = pygame.image.load('Assets/golang.png')
php = pygame.image.load('Assets/php.png')
rust = pygame.image.load('Assets/rust.png')
swift = pygame.image.load('Assets/swift.png')

FOOD_FOR_PYTHON = [cplus, csharp, js, java, rust, ruby, golang, php, swift]


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgtext = font.render(text, True, fcolor)
    screen.blit(imgtext, (x, y))


def init_snake():
    snake = deque()
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))
    return snake


def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Python Snake')

    font2 = pygame.font.Font(None, 72)
    fwidth, fheight = font2.size('GAME OVER')
    b = True
    score = 0
    snake = init_snake()
    food = create_food(snake)
    rand_food = random.choice(FOOD_FOR_PYTHON)
    pos = (1, 0)

    running = False
    start = False
    orispeed = 0.2
    speed = orispeed
    last_move_time = None
    pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN and not running:

                    start = True
                    running = True
                    b = True
                    snake = init_snake()
                    food = create_food(snake)
                    pos = (1, 0)
                    score += 1
                    last_move_time = time.time()
                elif event.key == pygame.K_SPACE:
                    if running:
                        pause = not pause
                elif event.key in (pygame.K_w, pygame.K_UP):
                    if b and not pos[1]:
                        pos = (0, -1)
                        b = False
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False
        screen.blit(BACKGROUND, (0, 0))

        if running:
            cur_time = time.time()
            if cur_time - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = cur_time
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        snake.appendleft(next_s)
                        speed = orispeed - 0.03 * (score // 100)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            running = False
        if running:
            screen.blit(rand_food,
                        (food[0] * PIXEL_SIZE, food[1] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        for s in snake:
            proper_size_body = pygame.transform.scale(BODY, (40, 40))
            screen.blit(proper_size_body,
                        (s[0] * PIXEL_SIZE + LINE_WIDTH, s[1] * PIXEL_SIZE + LINE_WIDTH,
                         PIXEL_SIZE - LINE_WIDTH * 2, PIXEL_SIZE - LINE_WIDTH * 2))
        if not running:
            if start:
                print_text(screen, font2, (WIDTH - fwidth) // 2,
                           (HEIGHT - fheight) // 2, 'GAME OVER', (100, 100, 100))
        if not running:
            print_text(screen, font2, (WIDTH - fwidth) // 2 - 85,
                       (HEIGHT - fheight) // 2 + 150, "Press 'Enter' to start", (100, 100, 100))
        pygame.display.update()


if __name__ == '__main__':
    main()
