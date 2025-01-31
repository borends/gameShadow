#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Grass(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/grass.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class NewBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("blocks/new_block.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y