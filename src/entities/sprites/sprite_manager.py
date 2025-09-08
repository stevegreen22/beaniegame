import math

import pygame
from config.config import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, image=None, tile_properties=None,):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.engine = engine

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.properties = tile_properties
        self.image = image


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    #     pull image from sprite sheet
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

    # todo: more elegant way to get columns, store sprite data in the obj
    def get_sprite_co_ordinates_by_tile_id(self, tile_id, columns, spacing=0, margin=0):
        x = tile_id % columns  # in tiles
        x = x * (TILE_SIZE + spacing) + margin  # // now in pixels
        y = math.floor(tile_id / columns)  # // in tiles
        y = y * (TILE_SIZE + spacing) + margin  # // now in pixels
        return x, y