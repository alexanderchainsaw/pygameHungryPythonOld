""" Built upon (https://github.com/guliang21)'s (https://github.com/guliang21/pygame/tree/master/GluttonousSnake)"""

import random
import sys
import pygame
from collections import deque

import assets

WIDTH, HEIGHT = 1000, 720
SQUARE_SIZE = 40
SQUARES_X = (WIDTH//SQUARE_SIZE) - 1  # = 24
SQUARES_Y = (HEIGHT//SQUARE_SIZE) - 1  # = 17
FOOD_FOR_PYTHON = assets.FOOD_FOR_PYTHON
game_time = pygame.time.Clock()
speed = 10  # difficulty (higher = faster)


def print_text(screen, font, x, y, text, font_color=(80, 80, 80)):
    imgtext = font.render(text, True, font_color)
    screen.blit(imgtext, (x, y))


def init_snake():
    snake = deque()
    snake.append((7, 8))
    snake.append((6, 8))
    snake.append((5, 8))
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
    pygame.display.set_caption('Hungry Python')
    head_position = assets.HEAD_RIGHT
    main_font = pygame.font.Font('Assets/AtariClassic-gry3.ttf', 24)
    snake = init_snake()
    food = create_food(snake)
    rand_food = random.choice(FOOD_FOR_PYTHON)
    pos = (1, 0)
    running, start = False, False
    score = 0
    flag = True  # preventing a bug ( simultaneous key presses causing game over )
    while True:
        screen.blit(assets.BACKGROUND, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN and not running:
                    flag, start, running = True, True, True
                    snake = init_snake()
                    food = create_food(snake)
                    pos = (1, 0)
                    head_position = assets.HEAD_RIGHT
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
        if running:
            flag = True
            next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
            if next_s == food:
                score += 10
                snake.appendleft(next_s)
                food = create_food(snake)
                rand_food = random.choice(FOOD_FOR_PYTHON)
            else:
                if 0 <= next_s[0] <= SQUARES_X and 0 <= next_s[1] <= SQUARES_Y \
                        and next_s not in snake:
                    snake.appendleft(next_s), snake.pop()
                elif next_s[0] > SQUARES_X and next_s not in snake:
                    if (foo := (snake[0][0] + pos[0] - SQUARES_X - 1, snake[0][1] + pos[1])) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif 0 > next_s[0] < SQUARES_X and next_s not in snake:
                    if (foo := (snake[0][0] + pos[0] + SQUARES_X + 1, snake[0][1] + pos[1])) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif next_s[1] > SQUARES_Y and next_s not in snake:
                    if (foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] - SQUARES_Y - 1)) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif 0 > next_s[1] < SQUARES_Y and next_s not in snake:
                    if (foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] + SQUARES_Y + 1)) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif next_s in snake:
                    running = False
        if running:
            screen.blit(rand_food,
                        (food[0] * SQUARE_SIZE, food[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for s in snake:
            screen.blit(assets.BODY, (s[0] * SQUARE_SIZE, s[1] * SQUARE_SIZE,
                        SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        screen.blit(head_position, (snake[0][0] * SQUARE_SIZE, snake[0][1] * SQUARE_SIZE,
                    SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        if running:
            print_text(screen, main_font, 0, 0, f'SCORE : {score}')
        if not running:
            if start:
                print_text(screen, main_font, WIDTH // 2 - 100,
                           HEIGHT // 2, 'GAME OVER')
                print_text(screen, main_font, WIDTH // 2 - 150,
                           HEIGHT // 2 + 75, f'SCORE : {score}')
        if not running:
            print_text(screen, main_font, WIDTH // 2 - 250,
                       HEIGHT // 2 + 150, "Press 'Enter' to start")

        pygame.display.update()
        game_time.tick(speed)


if __name__ == '__main__':
    main()
