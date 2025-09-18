import pygame

from config.config import TELEPORT_LAYER
from src.entities.sprites.sprite_manager import Entity


def teleport(area_file):
    from src.core.area import area
    area.load_file(area_file)

class Teleporter(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = TELEPORT_LAYER

        self.groups = [self.map.all_sprites, self.map.teleporters]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y