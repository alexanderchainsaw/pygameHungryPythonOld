import pygame


def print_text(screen, font, x, y, text, font_color=(255, 255, 255)):
    imgtext = font.render(text, True, font_color)
    screen.blit(imgtext, (x, y))


def display_text(running, won, lost, lvl, score, screen, HEIGHT, WIDTH, streak):
    difficulties = 'EASY MEDIUM HARD INSANE UNWINNABLE ??????'.split()
    if streak < 5:
        diff = streak
    else:
        diff = 5
    main_font = pygame.font.Font('Assets/AtariClassic-gry3.ttf', 24)
    if running:
        print_text(screen, main_font, 0, 0, f'SCORE : {score}')
        print_text(screen, main_font, 0, 20, f'LVL :{lvl}')
        print_text(screen, main_font, 0, 40, f'DIFFICULTY :{difficulties[diff]}')
    if not running:
        if won:
            print_text(screen, main_font, WIDTH // 2 - 100,
                       HEIGHT // 2, 'VICTORY')
        if lost:
            if streak:
                print_text(screen, main_font, WIDTH // 2 - 250,
                           HEIGHT // 2 + 30, f'WINS IN A ROW : {streak}')
            print_text(screen, main_font, WIDTH // 2 - 125,
                       HEIGHT // 2 - 35, 'GAME OVER')
            print_text(screen, main_font, WIDTH // 2 - 150,
                       HEIGHT // 2 + 65, f'SCORE : {score}')
            print_text(screen, main_font, WIDTH // 2 - 100,
                       HEIGHT // 2 + 95, f'LVL : {lvl}')
    if not running:
        if won:
            phrase = 'repeat'
        else:
            if lvl < 1:
                phrase = 'start'
            else:
                phrase = 'continue'
        print_text(screen, main_font, WIDTH // 2 - 250,
                   HEIGHT // 2 + 145, f"Press 'Enter' to {phrase}")