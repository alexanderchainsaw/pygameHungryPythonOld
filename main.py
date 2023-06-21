import random
import sys
import time
import pygame
from collections import deque

import assets

WIDTH = 1000
HEIGHT = 720
SQUARE_SIZE = 40
SQUARES_X = 24
SQUARES_Y = 17
FOOD_FOR_PYTHON = assets.FOOD_FOR_PYTHON


def print_text(screen, font, x, y, text, fcolor=(100, 100, 100)):
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

    head_position = assets.HEAD_RIGHT

    flag = True  # preventing a bug ( simultaneous key presses causing game over )

    main_font = pygame.font.Font('Assets/AtariClassic-gry3.ttf', 24)
    fwidth, fheight = main_font.size('GAME OVER')
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
                    last_move_time = time.time()
                    head_position = assets.HEAD_RIGHT
                elif event.key == pygame.K_SPACE:
                    if running:
                        pause = not pause
                elif event.key in (pygame.K_w, pygame.K_UP):
                    if flag and not pos[1]:
                        pos = (0, -1)
                        flag = False
                        head_position = assets.HEAD_UP
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if flag and not pos[1]:
                        pos = (0, 1)
                        flag = False
                        head_position = assets.HEAD_DOWN
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if flag and not pos[0]:
                        pos = (-1, 0)
                        flag = False
                        head_position = assets.HEAD_LEFT
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if flag and not pos[0]:
                        pos = (1, 0)
                        flag = False
                        head_position = assets.HEAD_RIGHT
        screen.blit(assets.BACKGROUND, (0, 0))

        if running:
            cur_time = time.time()
            if cur_time - last_move_time > speed:
                if not pause:
                    flag = True
                    last_move_time = cur_time
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        snake.appendleft(next_s)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                    else:
                        # BUG - Game not over when passing through wall and there is snake on the other side
                        if 0 <= next_s[0] <= SQUARES_X and 0 <= next_s[1] <= SQUARES_Y \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        elif next_s[0] > SQUARES_X and next_s not in snake:
                            snake.appendleft(foo := (snake[0][0] + pos[0] - SQUARES_X - 1, snake[0][1] + pos[1]))
                            snake.pop()
                            if foo == food:
                                snake.appendleft(foo)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif 0 > next_s[0] < SQUARES_X and next_s not in snake:
                            snake.appendleft(foo := (snake[0][0] + pos[0] + SQUARES_X + 1, snake[0][1] + pos[1]))
                            snake.pop()
                            if foo == food:
                                snake.appendleft(foo)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif next_s[1] > SQUARES_Y and next_s not in snake:
                            snake.appendleft(foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] - SQUARES_Y - 1))
                            snake.pop()
                            if foo == food:
                                snake.appendleft(foo)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif 0 > next_s[1] < SQUARES_Y and next_s not in snake:
                            snake.appendleft(foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] + SQUARES_Y + 1))
                            snake.pop()
                            if foo == food:
                                snake.appendleft(foo)
                                food = create_food(snake)
                                rand_food = random.choice(FOOD_FOR_PYTHON)
                        elif next_s in snake:
                            running = False
        if running:
            screen.blit(rand_food,
                        (food[0] * SQUARE_SIZE, food[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for s in snake:
            screen.blit(assets.BODY,
                        (s[0] * SQUARE_SIZE, s[1] * SQUARE_SIZE,
                         SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        screen.blit(head_position,
                    (snake[0][0] * SQUARE_SIZE, snake[0][1] * SQUARE_SIZE,
                        SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        if not running:
            if start:
                print_text(screen, main_font, (WIDTH - fwidth) // 2,
                           (HEIGHT - fheight) // 2, 'GAME OVER')
        if not running:
            print_text(screen, main_font, (WIDTH - fwidth) // 2 - 150,
                       (HEIGHT - fheight) // 2 + 150, "Press 'Enter' to start")
        pygame.display.update()


if __name__ == '__main__':
    main()
