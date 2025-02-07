from pygame import sprite, Surface, Color, Rect, image
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

# Предзагрузка изображений
platform_image = image.load(os.path.join(ICON_DIR, "blocks", "platform.png"))
grass_image = image.load(os.path.join(ICON_DIR, "blocks", "grass.png"))
chain_image = image.load(os.path.join(ICON_DIR, "blocks", "chain.png"))
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_image
        self.rect = self.image.get_rect(x=x, y=y)

class Grass(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = grass_image
        self.rect = self.image.get_rect(x=x, y=y)

class Chain(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = chain_image
        self.rect = self.image.get_rect(x=x, y=y)