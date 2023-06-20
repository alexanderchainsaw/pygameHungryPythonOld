import random
import sys
import time
import pygame
from collections import deque

WIDTH = 1000
HEIGHT = 720
SQUARE_SIZE = 40
SQUARES_X = 24
SQUARES_Y = 17

BACKGROUND = pygame.image.load('Assets/Background.png')
BODY = pygame.image.load('Assets/PythonBody.png')
HEAD_UP = pygame.image.load('Assets/PythonHeadUp.png')
HEAD_DOWN = pygame.image.load('Assets/PythonHeadDown.png')
HEAD_RIGHT = pygame.image.load('Assets/PythonHeadRight.png')
HEAD_LEFT = pygame.image.load('Assets/PythonHeadLeft.png')
CPLUS = pygame.image.load('Assets/cplusplus.png')
CSHARP = pygame.image.load('Assets/csharp.png')
JS = pygame.image.load('Assets/js.png')
JAVA = pygame.image.load('Assets/java.png')
RUBY = pygame.image.load('Assets/ruby.png')
GOLANG = pygame.image.load('Assets/golang.png')
PHP = pygame.image.load('Assets/php.png')
RUST = pygame.image.load('Assets/rust.png')
SWIFT = pygame.image.load('Assets/swift.png')
FOOD_FOR_PYTHON = [CPLUS, CSHARP, JS, JAVA, RUST, RUBY, GOLANG, PHP, SWIFT]


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgtext = font.render(text, True, fcolor)
    screen.blit(imgtext, (x, y))


def init_snake():
    snake = deque()
    snake.append((2, 0))
    snake.append((1, 0))
    snake.append((0, 0))
    return snake


def create_food(snake):
    food_x = random.randint(0, SQUARES_X)
    food_y = random.randint(0, SQUARES_Y)
    while (food_x, food_y) in snake:
        food_x = random.randint(0, SQUARES_X)
        food_y = random.randint(0, SQUARES_Y)
    return food_x, food_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Python Snake')

    head_position = HEAD_RIGHT

    flag = True  # preventing a bug ( simultaneous key presses causing game over )

    font2 = pygame.font.Font(None, 72)
    fwidth, fheight = font2.size('GAME OVER')
    score = 0
    snake = init_snake()
    food = create_food(snake)
    rand_food = random.choice(FOOD_FOR_PYTHON)
    pos = (1, 0)
    running = False
    start = False
    speed = 0.15
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
                    flag = True
                    start = True
                    running = True
                    snake = init_snake()
                    food = create_food(snake)
                    pos = (1, 0)
                    score += 1
                    last_move_time = time.time()
                elif event.key == pygame.K_SPACE:
                    if running:
                        pause = not pause
                elif event.key in (pygame.K_w, pygame.K_UP):
                    if flag and not pos[1]:
                        pos = (0, -1)
                        flag = False
                        head_position = HEAD_UP
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if flag and not pos[1]:
                        pos = (0, 1)
                        flag = False
                        head_position = HEAD_DOWN
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if flag and not pos[0]:
                        pos = (-1, 0)
                        flag = False
                        head_position = HEAD_LEFT
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if flag and not pos[0]:
                        pos = (1, 0)
                        flag = False
                        head_position = HEAD_RIGHT
        screen.blit(BACKGROUND, (0, 0))

        if running:
            cur_time = time.time()
            if cur_time - last_move_time > speed:
                if not pause:
                    flag = True
                    last_move_time = cur_time
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:  # brute force = 'if food in snake'
                        snake.appendleft(next_s)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                    else:
                        if 0 <= next_s[0] <= SQUARES_X and 0 <= next_s[1] <= SQUARES_Y \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        # early ver of passthrough (not working properly)
                        elif next_s[0] > SQUARES_X and next_s not in snake:
                            snake.appendleft(next_s := (snake[0][0] + pos[0] - SQUARES_X - 1, snake[0][1] + pos[1]))
                            snake.pop()
                            if next_s == food:  # brute force = 'if food in snake'
                                snake.appendleft(next_s)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif 0 > next_s[0] < SQUARES_X and next_s not in snake:
                            snake.appendleft(next_s := (snake[0][0] + pos[0] + SQUARES_X + 1, snake[0][1] + pos[1]))
                            snake.pop()
                            if next_s == food:  # brute force = 'if food in snake'
                                snake.appendleft(next_s)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif next_s[1] > SQUARES_Y and next_s not in snake:
                            snake.appendleft(next_s := (snake[0][0] + pos[0], snake[0][1] + pos[1] - SQUARES_Y - 1))
                            snake.pop()
                            if next_s == food:  # brute force = 'if food in snake'
                                snake.appendleft(next_s)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif 0 > next_s[1] < SQUARES_Y and next_s not in snake:
                            snake.appendleft(next_s := (snake[0][0] + pos[0], snake[0][1] + pos[1] + SQUARES_Y + 1))
                            snake.pop()
                            if next_s == food:  # brute force = 'if food in snake'
                                snake.appendleft(next_s)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        # early ver of passthrough (not working properly)
                        elif next_s in snake:
                            running = False
        if running:
            screen.blit(rand_food,
                        (food[0] * SQUARE_SIZE, food[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for s in snake:
            screen.blit(BODY,
                        (s[0] * SQUARE_SIZE, s[1] * SQUARE_SIZE,
                         SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        screen.blit(head_position,
                    (snake[0][0] * SQUARE_SIZE, snake[0][1] * SQUARE_SIZE,
                        SQUARE_SIZE * 2, SQUARE_SIZE * 2))
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
