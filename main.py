#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *

#Объявляем переменные
WIN_WIDTH = 1280 #Ширина создаваемого окна
WIN_HEIGHT = 720 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#FFFFFF"

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # Call the parent class (Sprite) constructor
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Foreground(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.target = Rect(0, 0, width, height)
        self.lerp_speed = 0.05  # Скорость интерполяции (0.05 = 5%)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.target = self.camera_func(self.target, target.rect)
        # Плавное перемещение камеры к целевой позиции
        self.state.x += (self.target.x - self.state.x) * self.lerp_speed
        self.state.y += (self.target.y - self.state.y) * self.lerp_speed

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Shadow") # Пишем в шапку
    background = Background("blocks/background.png", [0, -400])

    hero = Player(100,55) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    ramps = []
    grass = []
    creates = [] # то, во что мы будем врезаться или опираться

    entities.add(background)
    entities.add(hero)
    #foreground = Foreground("blocks/foreground.png", [0, 0])  # Create a foreground sprite
    #entities.add(foreground)  # Add the foreground sprite to the entity group

    level = [
       "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                                                                                                                                                                                                                                                                                                          -",
       "-                      N                                                                                                                                                                                                                                                                                   -",
       "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",]

    timer = pygame.time.Clock()
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "G":
                pf = Grass(x,y)
                entities.add(pf)
                grass.append(pf)
            if col == "N":
                nb = NewBlock(x, y)
                entities.add(nb)
                platforms.append(nb)

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True


            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

             # Каждую итерацию необходимо всё перерисовывать


        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение

        # Отображаем все спрайты
        for e in entities:
            screen.blit(e.image, camera.apply(e))


        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
