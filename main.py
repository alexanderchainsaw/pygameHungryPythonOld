""" Built upon (https://github.com/guliang21)'s (https://github.com/guliang21/pygame/tree/master/GluttonousSnake)"""

import random
import sys
import pygame
from collections import deque

import assets
import levels
import text_display

WIDTH, HEIGHT = 1000, 720
SQUARE_SIZE = 40
SQUARES_X = (WIDTH//SQUARE_SIZE) - 1  # = 24
SQUARES_Y = (HEIGHT//SQUARE_SIZE) - 1  # = 17
FOOD_FOR_PYTHON = assets.FOOD_FOR_PYTHON
GAME_TIME = pygame.time.Clock()
LEVELS = (levels.zero, levels.one, levels.two, levels.three, levels.four)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def init_snake():
    snake = deque()
    snake.append((3, 7))
    snake.append((2, 7))
    snake.append((1, 7))
    return snake


def create_food(snake, obstacle):
    food_x = random.randint(0, SQUARES_X)
    food_y = random.randint(0, SQUARES_Y)
    while (food_x, food_y) in snake or (food_x, food_y) in obstacle:
        food_x = random.randint(0, SQUARES_X)
        food_y = random.randint(0, SQUARES_Y)
    return food_x, food_y


def main():
    pygame.init()
    pygame.display.set_caption('Hungry Python')
    visual_status = random.getrandbits(1)  # for switching color schemes during the game
    head_position = (assets.HEAD_RIGHT, assets.HEAD_RIGHT_Alt)[visual_status]
    snake = init_snake()
    lvl = 0
    obstacles = LEVELS[lvl]
    food = create_food(snake, obstacles)
    rand_food = random.choice(FOOD_FOR_PYTHON)
    pos = (1, 0)
    running, won = False, False
    lost = False
    score = 0
    flag = True  # preventing a bug ( simultaneous key presses causing game over )
    lvlup_points = 100  # points for level up
    base_speed = 10  # base speed (increases with each win)
    speed_increment = 2  # adds to the base speed with each consecutive win
    streak = 0
    while True:
        obstacles = LEVELS[lvl]
        SCREEN.blit((assets.BACKGROUND, assets.BACKGROUND_Alt)[visual_status], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN and not running:
                    if won:
                        flag, running = True, True
                        snake = init_snake()
                        food = create_food(snake, obstacles)
                        pos = (1, 0)
                        head_position = (assets.HEAD_RIGHT, assets.HEAD_RIGHT_Alt)[visual_status]
                        base_speed += speed_increment
                        streak += 1
                        won = False
                    elif lost:
                        flag, running = True, True
                        snake = init_snake()
                        food = create_food(snake, obstacles)
                        pos = (1, 0)
                        head_position = (assets.HEAD_RIGHT, assets.HEAD_RIGHT_Alt)[visual_status]
                        score = 0
                        lvl = 0
                        base_speed = 10
                        streak = 0
                    else:
                        flag, running = True, True
                        snake = init_snake()
                        food = create_food(snake, obstacles)
                        pos = (1, 0)
                        head_position = (assets.HEAD_RIGHT, assets.HEAD_RIGHT_Alt)[visual_status]
                elif event.key in (pygame.K_w, pygame.K_UP):
                    if flag and not pos[1]:
                        pos = (0, -1)
                        flag = False
                        head_position = (assets.HEAD_UP, assets.HEAD_UP_Alt)[visual_status]
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if flag and not pos[1]:
                        pos = (0, 1)
                        flag = False
                        head_position = (assets.HEAD_DOWN, assets.HEAD_DOWN_Alt)[visual_status]
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if flag and not pos[0]:
                        pos = (-1, 0)
                        flag = False
                        head_position = (assets.HEAD_LEFT, assets.HEAD_LEFT_Alt)[visual_status]
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if flag and not pos[0]:
                        pos = (1, 0)
                        flag = False
                        head_position = (assets.HEAD_RIGHT, assets.HEAD_RIGHT_Alt)[visual_status]
        if running:
            flag = True
            next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
            if next_s == food:
                score += 10
                snake.appendleft(next_s)
                food = create_food(snake, obstacles)
                rand_food = random.choice(FOOD_FOR_PYTHON)
            else:
                if 0 <= next_s[0] <= SQUARES_X and 0 <= next_s[1] <= SQUARES_Y \
                        and next_s not in snake and next_s not in obstacles:
                    snake.appendleft(next_s), snake.pop()
                elif next_s[0] > SQUARES_X and next_s not in snake and next_s not in obstacles:
                    if (foo := (snake[0][0] + pos[0] - SQUARES_X - 1, snake[0][1] + pos[1])) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake, obstacles)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif 0 > next_s[0] < SQUARES_X and next_s not in snake and next_s not in obstacles:
                    if (foo := (snake[0][0] + pos[0] + SQUARES_X + 1, snake[0][1] + pos[1])) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake, obstacles)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif next_s[1] > SQUARES_Y and next_s not in snake and next_s not in obstacles:
                    if (foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] - SQUARES_Y - 1)) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake, obstacles)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif 0 > next_s[1] < SQUARES_Y and next_s not in snake and next_s not in obstacles:
                    if (foo := (snake[0][0] + pos[0], snake[0][1] + pos[1] + SQUARES_Y + 1)) in snake:
                        running = False
                    else:
                        snake.appendleft(foo), snake.pop()
                    if foo == food:
                        score += 10
                        snake.appendleft(foo)
                        food = create_food(snake, obstacles)
                        rand_food = random.choice(FOOD_FOR_PYTHON)
                elif next_s in snake or next_s in obstacles:
                    running = False
                    lost = True
        if score == lvlup_points:
            lvl += 1
            if lvl > len(LEVELS)-1:
                won = True
                lvl = 0
            running = False
            lost = False
            score = 0
            visual_status = int(not visual_status)
        if running:
            SCREEN.blit(rand_food,
                        (food[0] * SQUARE_SIZE, food[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for s in snake:
            SCREEN.blit((assets.BODY, assets.BODY_Alt)[visual_status], (s[0] * SQUARE_SIZE, s[1] * SQUARE_SIZE,
                                                                        SQUARE_SIZE * 2, SQUARE_SIZE * 2))
        SCREEN.blit(head_position, (snake[0][0] * SQUARE_SIZE, snake[0][1] * SQUARE_SIZE,
                                    SQUARE_SIZE * 2, SQUARE_SIZE * 2))

        for obstacle in obstacles:
            pygame.draw.rect(SCREEN, (100, 100, 100),
                             (obstacle[0] * SQUARE_SIZE, obstacle[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        text_display.display_text(running, won, lost, lvl, score, streak)

        pygame.display.update()
        GAME_TIME.tick(base_speed)


if __name__ == '__main__':
    main()
