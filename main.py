#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import math
from pygame import *
from player import *
from blocks import *

import os

import pygame
import os

import pygame
import os
import math

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

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Game Shadow")

    if not show_start_screen(screen):
        return

    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    hero = Player(100, 55)
    left = right = up = False

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
       "-                                                 -",
       "-                                                 -",
       "-                                                 -",
       "-                 E                                -",
       "-                                                 -",
       "-                       ------                    -",
       "-                  ------                         -",
       "-----------------------------------------         -",
       "---------------------------------------------------"]

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

    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

        screen.blit(bg, (0, 0))

        camera.update(hero)
        hero.update(left, right, up, platforms)
        enemies.update()

        # Проверка столкновения с врагом
        if pygame.sprite.spritecollide(hero, enemies, False):
            if not show_death_screen(screen):
                return  # Выход из игры, если игрок решил выйти после смерти
            hero.rect.x, hero.rect.y = 100, 55  # Возвращаем героя в начальную точку

        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))

        pygame.display.update()

if __name__ == "__main__":
    main()