import pygame
from pygame import *

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = "#FF0000"
ENEMY_SPEED = 1

class Enemy(sprite.Sprite):
    def __init__(self, x, y, left, right):
        sprite.Sprite.__init__(self)
        self.image = Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(Color(ENEMY_COLOR))
        self.rect = Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.start_x = x
        self.end_x = right
        self.speed = ENEMY_SPEED
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < self.start_x:
            self.direction = 1
        if self.rect.right > self.end_x:
            self.direction = -1