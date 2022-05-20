import pygame
from random import randrange as rnd


# Функция для определения столкновения с блоками
def detect_block_hit(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


# Настройка ширины и высоты игрового окна
Width, Height = 1200, 800

# Настройка кадров игры
FPS = 60

# Настройки игрового поля
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(Width // 2 - paddle_w // 2, Height - paddle_h - 10, paddle_w, paddle_h)

# Параметры шара
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, Width - ball_rect), Height // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Блоки в игре
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

# Инициализация игры
pygame.init()
sc = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

# Заставка
image = pygame.image.load('Sprite.jpg').convert()

# Процесс работы игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(image, (0, 0))

    # Отрисовка объектов игры
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('Orange'), paddle)
    pygame.draw.circle(sc, pygame.Color('White'), ball.center, ball_radius)
    # Движение шара
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # Условия отражения шарика от левой и правой стен
    if ball.centerx < ball_radius or ball.centerx > Width - ball_radius:
        dx = -dx
    # Условия отражения шарика от вверха
    if ball.centery < ball_radius:
        dy = -dy

    # Условия столкновения
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_block_hit(dx, dy, ball, paddle)

    # Проверка столкновения мяча с блоками
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_block_hit(dx, dy, ball, hit_rect)

    # Ситуации проигрыша и выигрыша
    if ball.bottom > Height:
        print('Game over :(\nLets try again!')
        exit()
    elif not len(block_list):
        print('VICTORY!\nYou are amazing!')
        exit()

    # Управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < Width:
        paddle.right += paddle_speed

    # Обновление кадров экрана
    pygame.display.flip()
    clock.tick(FPS)
