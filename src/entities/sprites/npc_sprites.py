import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity


class NPC (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = NPC_LAYER
        self.groups = [self.engine.all_sprites, self.engine.npcs]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

