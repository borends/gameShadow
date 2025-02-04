import pygame
import random
from player import *
from blocks import *
import os
import csv
import pygame.mixer
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join('blocks', 'saw.png')).convert_alpha()
        # Уменьшаем размер изображения в 4 раза
        new_size = (self.original_image.get_width() // 4, self.original_image.get_height() // 4)
        self.original_image = pygame.transform.scale(self.original_image, new_size)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.start_x = x
        self.direction = 1
        self.xvel = 2
        self.angle = 0

    def update(self):
        # Движение
        self.rect.x += self.direction * self.xvel
        if abs(self.rect.x - self.start_x) > 100:
            self.direction *= -1

        # Вращение
        self.angle = (self.angle + 5) % 360  # Увеличиваем угол на 5 градусов каждый кадр
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
class Fly(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join('blocks', 'fly.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.yvel = 2

    def update(self):
        self.rect.y += self.yvel
        if abs(self.rect.y - self.start_y) > 50:
            self.yvel *= -1

class Slug(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join('blocks', 'slug.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect(center=(x, y))
        self.xvel = 1

    def update(self):
        self.rect.x += self.xvel
        if abs(self.rect.x - self.start_x) > 100:
            self.xvel *= -1
            self.image = pygame.transform.flip(self.image, True, False)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('blocks', 'spike.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

class FallingRock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('blocks', 'rock.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.falling = False
        self.start_y = y

    def update(self, player):
        if not self.falling and abs(self.rect.x - player.rect.x) < 50:
            self.falling = True
        if self.falling:
            self.rect.y += 5
        if self.rect.y > WIN_HEIGHT:
            self.rect.y = self.start_y
            self.falling = False

class Trigger(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow color for visibility
        self.rect = self.image.get_rect(center=(x, y))

LEVELS = [
    {
        "map": [
            "----------------------------------------------------",
            "-                                                  -",
            "-                    E                             -",
            "-           ---                                    -",
            "-                          E                       -",
            "-     ---                                          -",
            "-                 ---              -               -",
            "-                                                  -",
            "-                       ---                        -",
            "-                                   E              -",
            "-      E          ---                              -",
            "-    -----                                         -",
            "-                                 ---              -",
            "-             ---                                  -",
            "-                                                  -",
            "-                                                  -",
            "-                                                  -",
            "----------------------------------------------------"
        ],
        "background": "forest_bg.png",
        "music": "forest_music.mp3"
    },
    {
        "map": [
            "----------------------------------------------------",
            "-                |                   |             -",
            "-     -----      |    ----     S     |             -",
            "-                |         |         |             -",
            "-          S     |         |    P    |             -",
            "-     ---------  |         |  -----  |             -",
            "-                |                   |             -",
            "-           -----|         |---------|             -",
            "-                                                  -",
            "-     ------                         -------       -",
            "-                S                                 -",
            "-          ---------------                         -",
            "-                        |          P              -",
            "-                        |     --------------      -",
            "-                        |                         -",
            "-                        |                         -",
            "-                        |                         -",
            "----------------------------------------------------"
        ],
        "background": "house_bg.png",
        "music": "house_music.mp3"
    },
    {
        "map": [
            "----------------------------------------------------",
            "-                                                  -",
            "-              O                 O                 -",
            "-        ------           ------                   -",
            "-                                                  -",
            "-                                                  -",
            "-    O        ------     ------        O           -",
            "-                                                  -",
            "-           O                    O                 -",
            "-     ------                        ------         -",
            "-                                                  -",
            "-                                                  -",
            "-        O              T               O          -",
            "-  ------                            ------        -",
            "-                                                  -",
            "-                                                  -",
            "-              O                 O                 -",
            "----------------------------------------------------"
        ],
        "background": "white_bg.png",
        "music": "puzzle_music.mp3"
    }
]
# Объявляем переменные
WIN_WIDTH = 1280
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#778899"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.target_state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.target_state = self.camera_func(self.target_state, target.rect)
        # Плавное движение камеры
        self.state.x += (self.target_state.x - self.state.x) * 0.05
        self.state.y += (self.target_state.y - self.state.y) * 0.05

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width-WIN_WIDTH), l)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)

def show_start_screen(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    for _ in range(100):
        x = random.randint(0, WIN_WIDTH)
        y = random.randint(0, WIN_HEIGHT)
        pygame.draw.circle(background, (20, 20, 20), (x, y), random.randint(20, 100))

    font = pygame.font.Font(None, 72)
    text = font.render("SHADOW", True, (200, 200, 200))
    text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

    font_small = pygame.font.Font(None, 36)
    instruction = font_small.render("Press Enter to start", True, (150, 150, 150))
    instruction_rect = instruction.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2 + 100))

    screen.blit(background, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(instruction, instruction_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    return True

def show_death_screen(screen):
    fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 300, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True
def show_end_screen(screen):
    font = pygame.font.Font(None, 72)
    text = font.render("Congratulations! You've completed the game!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    return True


def load_sound(filename):
    sound = pygame.mixer.Sound(os.path.join('sounds', filename))
    return sound
def save_game(player):
    with open('save_game.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player.rect.x, player.rect.y])

def load_game():
    try:
        with open('save_game.csv', 'r') as file:
            reader = csv.reader(file)
            row = next(reader)
            return int(row[0]), int(row[1])
    except (FileNotFoundError, StopIteration, ValueError):
        return None

def create_background_layers():
    layers = []
    for i in range(3):
        layer = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        for _ in range(20):
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(0, WIN_HEIGHT)
            radius = random.randint(10, 50)
            alpha = random.randint(10, 40)
            # Используем черные круги с прозрачностью
            color = (0, 0, 0, alpha)
            pygame.draw.circle(layer, color, (x, y), radius)
        layers.append(layer)
    return layers

def main():
    # Загрузка звуков
    pygame.mixer.init()
    sound_walk = load_sound('walk.wav')
    sound_jump = load_sound('jump.wav')
    sound_enemy = load_sound('enemy.wav')
    sound_death = load_sound('death.wav')
    pygame.mixer.music.load(os.path.join('sounds', 'background_music.mp3'))

    # Настройка громкости
    sound_walk.set_volume(0.3)
    sound_jump.set_volume(0.4)
    sound_enemy.set_volume(0.2)  # Уменьшаем громкость звука врага
    sound_death.set_volume(0.5)
    pygame.mixer.music.set_volume(0.3)  # Настройка громкости фоновой музыки

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Game Shadow")

    if not show_start_screen(screen):
        return

    # Начать воспроизведение фоновой музыки
    pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

    bg_layers = create_background_layers()
    bg_speeds = [0.2, 0.5, 0.8]  # Скорости движения слоев

    # Загрузка сохраненной позиции
    saved_position = load_game()
    if saved_position:
        hero = Player(saved_position[0], saved_position[1])
    else:
        hero = Player(100, 55)  # Начальная позиция, если нет сохранения

    left = right = up = False
    is_jumping = False  # Флаг для отслеживания состояния прыжка

    entities = pygame.sprite.Group()
    platforms = []
    enemies = pygame.sprite.Group()

    entities.add(hero)


    level = [
       "---------------------------------------------------",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                -",
       "-                                                 -",
       "-                                                 -",
       "--                                                -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-            E                                     -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "--------                                                                                                                                                                                                                                                                                                          -",
       "---------------         ------                                                                                                                                                                                                                                                                                    -",
       "-----------------------------------------                                                                                    -                                                                                    -                                                                                               -",
       "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "E":
                enemy = Enemy(x, y)
                entities.add(enemy)
                enemies.add(enemy)
                enemy.start_x = x
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    bg_offsets = [0, 0, 0]

    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                save_game(hero)
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                save_game(hero)
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_SPACE:
                if not is_jumping:  # Проверяем, не в прыжке ли уже герой
                    up = True
                    is_jumping = True
                    sound_jump.play()
            if e.type == KEYDOWN and e.key == K_a:
                left = True
                if not is_jumping:  # Воспроизводим звук ходьбы только если не в прыжке
                    sound_walk.play(-1)
            if e.type == KEYDOWN and e.key == K_d:
                right = True
                if not is_jumping:  # Воспроизводим звук ходьбы только если не в прыжке
                    sound_walk.play(-1)
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
                is_jumping = False
            if e.type == KEYUP and e.key == K_d:
                right = False
                sound_walk.stop()
            if e.type == KEYUP and e.key == K_a:
                left = False
                sound_walk.stop()

        screen.fill((200, 200, 200))  # Светло-серый фон

        # Отрисовка фоновых слоев с параллакс-эффектом
        for i, layer in enumerate(bg_layers):
            bg_offsets[i] -= bg_speeds[i]
            if bg_offsets[i] <= -WIN_WIDTH:
                bg_offsets[i] = 0
            screen.blit(layer, (bg_offsets[i], 0))
            screen.blit(layer, (bg_offsets[i] + WIN_WIDTH, 0))

        camera.update(hero)
        hero.update(left, right, up, platforms)
        enemies.update()

        # Проверка столкновения с врагом
        # Проверка столкновения с врагом
        if pygame.sprite.spritecollide(hero, enemies, False):
            sound_death.play()
            if not show_death_screen(screen):
                save_game(hero)  # Сохраняем текущую позицию перед выходом
                return  # Выход из игры, если игрок решил выйти после смерти
            # Загружаем сохраненную позицию вместо возврата в начальную точку
            saved_position = load_game()
            if saved_position:
                hero.rect.x, hero.rect.y = saved_position
            else:
                hero.rect.x, hero.rect.y = 100, 55
        # Воспроизведение звука врага
        for enemy in enemies:
            if abs(hero.rect.x - enemy.rect.x) < 300:  # Если герой близко к врагу
                if not pygame.mixer.get_busy() or not sound_enemy.get_num_channels():
                    sound_enemy.play()

        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))

        pygame.display.update()

if __name__ == "__main__":
    main()