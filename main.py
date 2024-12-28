import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Limbo Shadow")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# ФПС
FPS = 60
clock = pygame.time.Clock()

# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 20)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.dragging_box = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -5
        if keys[pygame.K_d]:
            self.vel_x = 5
        if keys[pygame.K_SPACE] and self.on_ground and not self.dragging_box:
            self.vel_y = -15
            self.on_ground = False
        if not self.on_ground:
            self.vel_y += 1  # Гравитация

        # Обновляем позицию игрока
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.vel_y = 0

# Класс для контейнера
class Container(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.vel_y += 1  # Гравитация

        # Обновляем позицию контейнера
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

# Класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

# Класс для камеры
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Ограничение прокрутки камеры
        x = min(0, x)  # Левая граница
        y = min(0, y)  # Верхняя граница
        x = max(-(self.width - WIDTH), x)  # Правая граница
        y = max(-(self.height - HEIGHT), y)  # Нижняя граница

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

containers = pygame.sprite.Group()
container = Container(WIDTH // 3, HEIGHT - 20)
all_sprites.add(container)
containers.add(container)

platforms = pygame.sprite.Group()
platform = Platform(WIDTH // 2 - 100, HEIGHT - 10, 200, 10)
all_sprites.add(platform)
platforms.add(platform)

# Создание камеры
camera = Camera(WIDTH * 2, HEIGHT)

# Функция для отрисовки слоев
def draw_layers():
    screen.fill(GRAY)  # Задний декоративный слой

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 20))  # Передний декоративный слой

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        if pygame.sprite.collide_rect(player, container):
            player.dragging_box = True
    else:
        player.dragging_box = False

    if player.dragging_box:
        container.vel_x = player.vel_x
    else:
        container.vel_x = 0

    # Проверка столкновения с игроком
    if pygame.sprite.collide_mask(player, container):
        if player.vel_x > 0:
            player.rect.right = container.rect.left
        elif player.vel_x < 0:
            player.rect.left = container.rect.right

    # Проверка если игрок стоит на контейнере
    if player.vel_y >= 0 and player.rect.bottom <= container.rect.top and player.rect.right > container.rect.left and player.rect.left < container.rect.right:
        player.rect.bottom = container.rect.top
        player.on_ground = True
        player.vel_y = 0
    elif (player.rect.right <= container.rect.left or player.rect.left >= container.rect.right) and player.rect.bottom <= container.rect.top:
        player.on_ground = False

    # Проверка столкновения с платформой
    if pygame.sprite.spritecollide(player, platforms, False):
        for platform in platforms:
            if player.vel_y >= 0 and player.rect.bottom <= platform.rect.top and player.rect.right > platform.rect.left and player.rect.left < platform.rect.right:
                player.rect.bottom = platform.rect.top
                player.on_ground = True
                player.vel_y = 0
            elif (
                    player.rect.right <= platform.rect.left or player.rect.left >= platform.rect.right) and player.rect.bottom <= platform.rect.top:
                player.on_ground = False

    # Обновление всех спрайтов
    all_sprites.update()

    # Обновление камеры
    camera.update(player)

    # Отрисовка слоев
    draw_layers()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
