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
        return sprite

    # todo: more elegant way to get columns, store sprite data in the obj
    def get_sprite_co_ordinates_by_tile_id(self, tile_id, columns, spacing=0, margin=0):
        x = tile_id % columns  # in tiles
        x = x * (TILE_SIZE + spacing) + margin  # // now in pixels
        y = math.floor(tile_id / columns)  # // in tiles
        y = y * (TILE_SIZE + spacing) + margin  # // now in pixels
        return x, y

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


class Trap (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = TRAP_LAYER
        self.groups = [self.engine.all_sprites, self.engine.traps]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = NPC_LAYER
        self.groups = [self.engine.all_sprites, self.engine.npcs]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

animal_props = {"chicken" : {
                    "speed" : 2, "max_health" : 100,"friendly": "True",
                    "image_folder": "chicken",
                    "audio_folder": "location",
                    "image_names": ["0.png", "1.png"],
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy" : [64,32],
                    "sprite_1_xy" : [96,32],
                    },
                "rabbit" : {
                    "speed" : 3, "max_health" : 100,"friendly": "True",
                    "image_folder": "rabbit",
                    "audio_folder": "location",
                    "image_names": ["0.png", "1.png"],
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy" : [64,64],
                    "sprite_1_xy" : [96,64],
                    },
                "hedgehog" : {
                    "speed" : 1, "max_health" : 100,"friendly": "True",
                    "image_folder": "hedgehog",
                    "audio_folder": "location",
                    "image_names": ["0.png", "1.png"],
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy": [64, 128],
                    "sprite_1_xy": [96, 128],
                },
                "capybara" : {
                    "speed" : 1, "max_health" : 100,"friendly": "True",
                    "image_folder": "chicken",
                    "audio_folder": "location",
                    "image_names": ["0.png", "1.png"],
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy": [0, 128],
                    "sprite_1_xy": [32, 128],
                }
}
animal_drops = {
            "chicken": { "type": "chicken_meat", "quantity" : 1},
            "rabbit": { "type": "rabbit_meat", "quantity" : 1},
            "hedgehog": { "type": "hedgehog_meat", "quantity" : 1},
            "capybara": { "type": None, "quantity" : 0},
            }


class Animal (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = ANIMAL_LAYER
        self.groups = [self.engine.all_sprites, self.engine.animals]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animal_name = self.properties["name"]
        # setting speed here fails to get passed in to the move method.
        self.animal_speed = animal_props[self.animal_name]["speed"]

        self.build_animal()

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.animal_speed = None
        # moves back and forth between 12 and 64 pixels
        self.max_travel = random.randint(12, 64)

        self.sprite_0_xy = animal_props[self.animal_name]["sprite_0_xy"]
        self.sprite_1_xy = animal_props[self.animal_name]["sprite_1_xy"]
        self.left_animations = [
            self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height),
            self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width, self.height),
        ]
        self.right_animations = [
            pygame.transform.flip(self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height), True, False),
            pygame.transform.flip(self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width, self.height), True, False)
        ]

        # Set a default image to save calling it in the animation loop when not moving
        # could/should be a left and right facing but for now this is fine.
        self.image = self.left_animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # Get the tile properties, from that determine type of animal and from there
    # get the sprites and set the movement range
    # chicken for example, speed slow, move little, but want it animated when within
    # a certain distance so that will need to be checked also.
    def build_animal(self):
        animal_max_health = animal_props[self.animal_name]["max_health"]
        if animal_props[self.animal_name]["item_drop_on_death"] == "True":
            drop = animal_drops[self.animal_name]["type"]
            qty = animal_drops[self.animal_name]["quantity"]

    # todo: update spritesheet so all animals are facing left by default.
    def animate(self):
        if self.facing == "left":
            # image for standing still
            if self.x_change == 0:
                self.image = self.image
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  # every ten frames we change image
                if self.animation_loop >= 2:
                    self.animation_loop = 1

        if self.facing == "right":
            # image for standing still
            if self.x_change == 0:
                self.image = self.image
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  # every ten frames we change image
                if self.animation_loop >= 2:
                    self.animation_loop = 1

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    # every frame we subtract from x and movement loop
    # if below max travel we change direction
    def movement(self):
        if self.facing == "left":
            self.x_change -= 1#self.animal_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += 1#self.animal_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"


class Block (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = BLOCK_LAYER
        self.groups = [self.engine.all_sprites, self.engine.blocks]
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
        self._layer = GROUND_LAYER

        self.groups = self.engine.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        pygame.sprite.Sprite.__init__(self)
        self.engine = engine
        self._layer = ENEMY_LAYER

        self.groups = self.engine.all_sprites, self.engine.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.properties = tile_properties

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

        self.left_animations = [self.engine.main_enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.engine.main_enemy_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.engine.main_enemy_spritesheet.get_sprite(64, 96, self.width, self.height)
                                ]
        self.right_animations = [self.engine.main_enemy_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.engine.main_enemy_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.engine.main_enemy_spritesheet.get_sprite(64, 64, self.width, self.height)
                                 ]

        self.image = self.engine.main_enemy_spritesheet.get_sprite(0, 0, self.width, self.height).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
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

    def animate(self):
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.engine.main_enemy_spritesheet.get_sprite(0, 96, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.engine.main_enemy_spritesheet.get_sprite(0, 64, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

