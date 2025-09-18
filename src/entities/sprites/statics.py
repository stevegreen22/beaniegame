import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity

class Trap (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = TRAP_LAYER
        self.groups = [self.engine.all_sprites, self.engine.traps]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = BLOCK_LAYER
        self.groups = [self.engine.all_sprites, self.engine.collision_blocks, self.engine.collision_group]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # if self.image is None:
        #     if tile_id is None:
        #         self.image = self.engine.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)
        #     else:
        #         image_coords = self.engine.terrain_spritesheet.get_sprite_co_ordinates_by_tile_id(tile_id, 32)
        #         self.image = (
        #             self.engine.terrain_spritesheet.get_sprite(image_coords[0], image_coords[1], self.width, self.height))
        # else:
        #     self.image = self.image
        # self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

class Ground(Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)

        if tile_properties is None:
            self._layer = GROUND_LAYER
            self.groups = self.engine.all_sprites
        else: # presumption here that if a tile has properties it will be a tree...
            self._layer = FOREGROUND_TREES
            self.groups = self.engine.all_sprites, self.engine.foreground_trees


        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
