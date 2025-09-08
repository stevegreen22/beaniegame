import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity
from random import randint, uniform
import random
import math
vec = pygame.math.Vector2

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
                self.image = pygame.transform.scale(self.image, (self.width-test, self.height-test))
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
                self.image = pygame.transform.scale(self.image, (self.width - test, self.height - test))
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  # every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def update(self):
        # self.movement()
        self.wander_movement()
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

    def wander_movement(self):
        self.acc = self.wander_improved()
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        if self.facing == "left":
            self.x_change -= 1#self.animal_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += 1  #self.animal_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

        self.pos.x += self.vel.x
        # if self.pos.x > self.width:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = self.width
        # if self.pos.y > self.height:
        #     self.pos.y = 0
        # if self.pos.y < 0:
        #     self.pos.y = self.height
        self.rect.center = self.pos