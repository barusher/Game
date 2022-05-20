import pygame
from copy import deepcopy
from random import choice, randrange

# Параметры экрана и блоков
TILE = 45
WIDTH, HEIGHT = 10, 20
RESOLUTION = WIDTH * TILE, HEIGHT * TILE
RES = 750, 940
FPS = 60

# Инициализация игры
pygame.init()
sc = pygame.display.set_mode(RES)
game_screen = pygame.Surface(RESOLUTION)
clock = pygame.time.Clock()

# Сетка
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]

# Координаты фигур и их отрисовка
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in positions] for positions in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

# Фон
background = pygame.image.load('Main.jpg').convert()
game_background = pygame.image.load('Not_Main.jpg').convert()

# Шрифт
main_font = pygame.font.Font('font.ttf', 65)
font = pygame.font.Font('font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('white'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record', True, pygame.Color('purple'))

# Цвет блоков
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
color, next_color = get_color(), get_color()
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

# Значения анимаций
anim_count, anim_speed, anim_limit = 0, 60, 2000

# Очки и их значениях
score, lines = 0, 0
scores = {0: 0, 1: 200, 2: 300, 3: 700, 4: 1500}


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


def check_borders():
    if figure[i].x < 0 or figure[i].x > WIDTH - 1:
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


# Процесс работы игры
while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(background, (0, 0))
    sc.blit(game_screen, (20, 20))
    game_screen.blit(game_background, (0, 0))

    # Задержка
    for i in range(lines):
        pygame.time.wait(200)

    # Управление
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    # Движение по х
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # Движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    # Вращение блоков
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # Проверка линий на заполненость
    line, lines = HEIGHT - 1, 0
    for row in range(HEIGHT - 1, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Подсчёт очков
    score += scores[lines]

    # Отрисовка сетки
    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Отрисовка фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_screen, color, figure_rect)

    # Отрисовка поля
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_screen, col, figure_rect)

    # Отрисовка следующей фигуры
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    # Надписи и титры
    sc.blit(title_tetris, (485, -10))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
    sc.blit(title_record, (525, 650))
    sc.blit(font.render(record, True, pygame.Color('red')), (550, 710))
    # Конец игры
    for i in range(WIDTH):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_screen, get_color(), i_rect)
                sc.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
