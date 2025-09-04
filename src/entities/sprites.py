import pygame
from config.config import *
import math
import random
from random import randint, uniform
vec = pygame.math.Vector2

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

"""
the enemies and npcs 'may' have a differing number of sprites per animation, the 
same for some other animals and traps.
they may also have differing number of attack sprites.
Potential solution, while it isn't super pretty may be:
in each properties include an int for how many movement sprites either 4 for all 
cardinal directions or 4 per left/right and 4 per up/down for example.
this number could also be the 'animation loop' variable.

"movement_animation_quantity": 4,
"attack_animation_quantity" : 5

then when building the sprites we can loop through and then mutliply by the width
rather than having img_0_x, img_0_y, img....n_x etc.
we will just need to record the starting position of the initial sprite.
ah, but also we need to know the start position of move left/right, move up/down and attack sprites


"""
#


animal_props = {"chicken" : {
                    "speed" : 2, "max_health" : 100, "friendly": "True",
                    "audio_folder": "location",
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy" : [64,32],
                    "sprite_1_xy" : [96,32],
                    },
                "rabbit" : {
                    "speed" : 3, "max_health" : 100,"friendly": "True",
                    "audio_folder": "location",
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy" : [64,64],
                    "sprite_1_xy" : [96,64],
                    },
                "hedgehog" : {
                    "speed" : 1, "max_health" : 100,"friendly": "True",
                    "audio_folder": "location",
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy": [64, 128],
                    "sprite_1_xy": [96, 128],
                },
                "capybara" : {
                    "speed" : 1, "max_health" : 100,"friendly": "True",
                    "audio_folder": "location",
                    "max_travel_distance" : 10, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy": [0, 128],
                    "sprite_1_xy": [32, 128],
                },
                "duck" : {
                    "speed" : 1, "max_health" : 100,"friendly": "True",
                    "audio_folder": "location",
                    "max_travel_distance" : 8, #distance that animal can move when activated
                    "activation_distance" : 10, #distance to player before movement
                    "item_drop_on_death" : "True", #lookup from list
                    "sprite_0_xy": [128, 32],
                    "sprite_1_xy": [160, 32],
                }
}
animal_drops = {
            "chicken": { "type": "chicken_meat", "quantity" : 1},
            "rabbit": { "type": "rabbit_meat", "quantity" : 1},
            "hedgehog": { "type": "hedgehog_meat", "quantity" : 1},
            "capybara": { "type": None, "quantity" : 0},
            "duck": { "type": None, "quantity" : 0},
            }

MAX_SPEED = 1
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 100

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

        # get the spritesheet locations by using the animal properties
        self.sprite_0_xy = animal_props[self.animal_name]["sprite_0_xy"]
        self.sprite_1_xy = animal_props[self.animal_name]["sprite_1_xy"]

        # scaled test, y coor isn't correct
        self.left_animations = [
            pygame.transform.scale(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width,
                                                               self.height), (self.width - 8, self.height - 8)),
            pygame.transform.scale(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width,
                                                               self.height), (self.width - 8, self.height - 8)),
            pygame.transform.scale(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width,
                                                               self.height), (self.width - 8, self.height - 8)),
        ]

        self.right_animations = [
            pygame.transform.scale(pygame.transform.flip(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width,
                                                               self.height), True, False),(self.width - 8, self.height - 8)),
            pygame.transform.scale(pygame.transform.flip(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width,
                                                               self.height), True, False),(self.width - 8, self.height - 8)),
            pygame.transform.scale(pygame.transform.flip(
                self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width,
                                                               self.height), True, False),(self.width - 8, self.height - 8)),
        ]

        # self.left_animations = [
        #     self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height),
        #     self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width, self.height),
        #     self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height),
        # ]
        # self.right_animations = [
        #     pygame.transform.flip(self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height), True, False),
        #     pygame.transform.flip(self.engine.main_animal_spritesheet.get_sprite(self.sprite_1_xy[0], self.sprite_1_xy[1], self.width, self.height), True, False),
        #     pygame.transform.flip(self.engine.main_animal_spritesheet.get_sprite(self.sprite_0_xy[0], self.sprite_0_xy[1], self.width, self.height), True, False),
        # ]

        # Set a default image to save calling it in the animation loop when not moving
        # could/should be a left and right facing but for now this is fine.
        self.image = self.left_animations[0]
        self.rect = self.image.get_rect()#(bottomleft=(self.sprite_0_xy[0]-16, self.sprite_0_xy[1]-16))
        self.rect.x = self.x
        self.rect.y = self.y
        # self.rect.bottomleft = self.x - 16, self.y - 16 works but needs improving.

    #     wander test
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))


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
        test = 8
        if self.facing == "left":
            # image for standing still
            if self.x_change == 0:
                self.image = pygame.transform.scale(self.image(self.width-test, self.height-test))
                # self.image = self.image
            else:
                # before_scale = self.left_animations[math.floor(self.animation_loop)]
                # self.image = pygame.transform.scale(before_scale, (self.width -test, self.height-test))
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  # every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            # image for standing still
            if self.x_change == 0:
                self.image = self.image
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  # every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def update_old(self):
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


#     test wander code
    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    def update(self):
        self.acc = self.wander_improved()
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        # if self.pos.x > self.width:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = self.width
        # if self.pos.y > self.height:
        #     self.pos.y = 0
        # if self.pos.y < 0:
        #     self.pos.y = self.height
        self.rect.center = self.pos


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

enemy_props = { "whitey" :{
                    "speed": 3, "max_health": 100,
                    "audio_folder": "<<location>>",
                    "max_travel_distance": 10,  # distance that animal can move when activated
                    "activation_distance": 10,  # distance to player before movement
                    "item_drop_on_death": "True",  # lookup from list
                    "movement_animation_quantity": 6,  # number of movement sprites
                    "left_right_movement_start_coord": (0, 64),  # starting coordinate in sprite sheet
                    "up_down_movement_start_coord": None,  # not used with slime
                    "attack_animation_quantity": None,  # not yet configured
                },
                "bluey" :{
                    "speed": 3, "max_health": 100,
                    "audio_folder": "<<location>>",
                    "max_travel_distance": 10,  # distance that animal can move when activated
                    "activation_distance": 10,  # distance to player before movement
                    "item_drop_on_death": "True",  # lookup from list
                    "movement_animation_quantity": 6,  # number of movement sprites
                    "left_right_movement_start_coord": (0, 64),  # starting coordinate in sprite sheet
                    "up_down_movement_start_coord": None,  # not used with slime
                    "attack_animation_quantity": None,  # not yet configured
                },
                "pinky" :{
                    "speed": 3, "max_health": 100,
                    "audio_folder": "<<location>>",
                    "max_travel_distance": 10,  # distance that animal can move when activated
                    "activation_distance": 10,  # distance to player before movement
                    "item_drop_on_death": "True",  # lookup from list
                    "movement_animation_quantity": 6,  # number of movement sprites
                    "left_right_movement_start_coord": (0, 64),  # starting coordinate in sprite sheet
                    "up_down_movement_start_coord": None,  # not used with slime
                    "attack_animation_quantity": None,  # not yet configured
                },
                # slime will use the same set of sprites for all animation regardless of axis
                "slime" :{
                    "speed" : 3, "max_health" : 100,
                    "audio_folder" : "<<location>>",
                    "max_travel_distance": 10,  # distance that animal can move when activated
                    "activation_distance": 10,  # distance to player before movement
                    "item_drop_on_death": "True",  # lookup from list
                    "movement_animation_quantity": 6, # number of movement sprites
                    "left_right_movement_start_coord" : (0, 64), #starting coordinate in sprite sheet
                    "up_down_movement_start_coord" : None, # not used with slime
                    "attack_animation_quantity" : None, #not yet configured
                }
                }

class Enemy(Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = ENEMY_LAYER

        self.groups = self.engine.all_sprites, self.engine.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.enemy_name = self.properties["name"]
        self.enemy_speed = None #enemy_props[self.enemy_name]["speed"]
        self.max_health = enemy_props[self.enemy_name]["max_health"]

        # self.build_enemy() add extra things like whether it can shoot, drops, etc etc

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        # moves back and forth between 7 and 30 pixels
        self.max_travel = random.randint(32, 96)

        # obtain the number of sprites
        self.movement_sprites = enemy_props[self.enemy_name]["movement_animation_quantity"]
        self.start_xy = enemy_props[self.enemy_name]["left_right_movement_start_coord"]
        self.move_sprites = []
        for i in range(self.movement_sprites):
            self.move_sprites.append(self.engine.main_enemy_spritesheet.get_sprite(self.start_xy[0] + (TILE_SIZE * i), self.start_xy[1], self.width, self.height))

        self.right_animations = self.move_sprites
        self.left_animations = [pygame.transform.flip(img, True, False) for img in self.move_sprites]

        self.image = self.engine.main_enemy_spritesheet.get_sprite(0, 64, self.width, self.height).convert()
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
                self.image = self.image
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.image
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 5:
                    self.animation_loop = 1

