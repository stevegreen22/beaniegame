import pygame
from config.config import *
import math
import random

# todo: create a list of sprite sheets here with relevant info such as columns and pertinent ids

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    #     pull image from sprite sheet
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        # panda black parts invisible
        return sprite

    # todo: more elegant way to get columns, store sprite data in the obj
    def get_sprite_co_ordinates_by_tile_id(self, tile_id, columns, spacing=0, margin=0):
        x = tile_id % columns  # in tiles
        x = x * (TILE_SIZE + spacing) + margin  # // now in pixels
        y = math.floor(tile_id / columns)  # // in tiles
        y = y * (TILE_SIZE + spacing) + margin  # // now in pixels
        return x, y

class Trap(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, tile_id=None, image=None):
        pygame.sprite.Sprite.__init__(self)
        self.engine = engine
        self._layer = TRAP_LAYER

        self.groups = self.engine.all_sprites, self.engine.traps
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.tile_id = tile_id
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, tile_id=None, image=None, enemy_type=None):
        pygame.sprite.Sprite.__init__(self)
        self.engine = engine
        self._layer = ENEMY_LAYER

        self.groups = self.engine.all_sprites, self.engine.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        # moves back and forth between 7 and 30 pixels
        self.max_travel = random.randint(32, 96)

        self.tile_id = tile_id
        self.image = self.engine.main_character_spritesheet.get_sprite(0, 0, self.width, self.height).convert_alpha()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        # self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            # every frame we subtract from x and movement loop
            # if below max travel we change direction
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"


class NPC(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, tile_id=None, image=None):
        pygame.sprite.Sprite.__init__(self)
        self.engine = engine
        self._layer = NPC_LAYER

        self.groups = self.engine.all_sprites, self.engine.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.tile_id = tile_id
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block (pygame.sprite.Sprite):
    def __init__(self, engine, x, y, tile_id=None, image=None):
        self.engine = engine
        self._layer = BLOCK_LAYER

        self.groups = self.engine.all_sprites, self.engine.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.tile_id = tile_id
        self.image = image
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

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, image, tile_id=None):
        self.engine = engine
        self._layer = GROUND_LAYER

        self.groups = self.engine.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = image
        self.tile_id = tile_id
        # if tile_id is None:
        #     self.image = self.engine.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        # else:
        #     image_coords = self.engine.terrain_spritesheet.get_sprite_co_ordinates_by_tile_id(tile_id, 32)
        #     self.image = (self.engine.terrain_spritesheet.get_sprite(image_coords[0], image_coords[1], self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y





