import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity

class Trap (Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = TRAP_LAYER
        self.groups = [map.all_sprites, map.traps]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block (Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = BLOCK_LAYER
        self.groups = [map.all_sprites, map.collision_blocks, map.collision_group]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)

        if tile_properties is None:
            self._layer = GROUND_LAYER
            self.groups = map.all_sprites
        else: # presumption here that if a tile has properties it will be a tree...
            self._layer = FOREGROUND_TREES
            self.groups = map.all_sprites, self.map.foreground_trees


        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
