import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity
from random import randint, uniform
import random
import math
vec = pygame.math.Vector2

# wandering Variables
# MAX_SPEED = 1
# MAX_FORCE = 0.4
# RAND_TARGET_TIME = 500
# WANDER_RING_DISTANCE = 150
# WANDER_RING_RADIUS = 100

class Animal (Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)
        self._layer = ANIMAL_LAYER
        self.groups = [self.engine.all_sprites, self.engine.animals]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # get values from properties
        self.animal_name = self.properties["name"]
        if self.animal_name == "rabbit_2":
            # set the sprite sheet and create the random starting y position
            # 0,0; 0,64;0,128;0,192;0,256
            #"start_coord" : (0,0)
            self.animal_spritesheet = self.engine.rabbit_2_spritesheet
            self.start_xy = (0, random.choice([0,64,128,192,256]))
            self.animation_speed = random.choice([0.1, 0.2, 0.25])
        else:
            self.animal_spritesheet = self.engine.main_animal_spritesheet
            self.start_xy = animal_props[self.animal_name]["start_coord"]
            self.animation_speed = random.choice([0.1, 0.2])

        self.animal_speed = animal_props[self.animal_name]["speed"]
        # self.build_animal()

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])

        self.animation_loop = 1
        self.movement_loop = 0
        # moves back and forth between 12 and 64 pixels
        self.max_travel = random.randint(50, 64)

        # get the spritesheet locations by using the animal properties

        self.movement_sprites = animal_props[self.animal_name]["animation_quantity"]
        self.move_sprites = []
        # build sprites
        self.sprite_reduction_pixels = 0
        for i in range(self.movement_sprites):
            self.move_sprites.append(pygame.transform.scale(self.animal_spritesheet.get_sprite(
                self.start_xy[0] + (TILE_SIZE * i), self.start_xy[1], self.width, self.height), (self.width-self.sprite_reduction_pixels, self.height-self.sprite_reduction_pixels)))

        self.right_animations = self.move_sprites
        self.left_animations = [pygame.transform.flip(img, True, False) for img in self.move_sprites]

        # Set a default image to save calling it in the animation loop when not moving
        # could/should be a left and right facing but for now this is fine.
        self.image = self.left_animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    #     wander test
    #     self.pos = vec(self.rect.x, self.rect.y)
        # self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))


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
                self.image = pygame.transform.scale(self.image, (self.width-self.sprite_reduction_pixels, self.height-self.sprite_reduction_pixels))
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed#0.1  # every ten frames we change image
                if self.animation_loop >= self.movement_sprites: #3
                    self.animation_loop = 1

        if self.facing == "right":
            # image for standing still
            if self.x_change == 0:
                self.image = pygame.transform.scale(self.image, (self.width - self.sprite_reduction_pixels, self.height - self.sprite_reduction_pixels))
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += self.animation_speed#0.1  # every ten frames we change image
                if self.animation_loop >= self.movement_sprites: #3:
                    self.animation_loop = 1

    def update(self):
        self.movement()
        # self.wander_movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0


    # every frame we subtract from x and movement loop
    # if below max travel we change direction
    def movement(self):
        if self.facing == "left":
            self.x_change -= self.animal_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += self.animal_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"


#     test wander code
#     def seek(self, target):
#         self.desired = (target - self.pos).normalize() * MAX_SPEED
#         steer = (self.desired - self.vel)
#         if steer.length() > MAX_FORCE:
#             steer.scale_to_length(MAX_FORCE)
#         return steer
#
#     def wander_improved(self):
#         future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
#         target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
#         self.displacement = target
#         return self.seek(target)
#
#     def wander_movement(self):
#         self.acc = self.wander_improved()
#         # equations of motion
#         self.vel += self.acc
#         if self.vel.length() > MAX_SPEED:
#             self.vel.scale_to_length(MAX_SPEED)
#
#         if self.facing == "left":
#             self.x_change -= 1#self.animal_speed
#             self.movement_loop -= 1
#             if self.movement_loop <= -self.max_travel:
#                 self.facing = "right"
#         if self.facing == "right":
#             self.x_change += 1  #self.animal_speed
#             self.movement_loop += 1
#             if self.movement_loop >= self.max_travel:
#                 self.facing = "left"
#
#         self.pos.x += self.vel.x
#         # if self.pos.x > self.width:
#         #     self.pos.x = 0
#         # if self.pos.x < 0:
#         #     self.pos.x = self.width
#         # if self.pos.y > self.height:
#         #     self.pos.y = 0
#         # if self.pos.y < 0:
#         #     self.pos.y = self.height
#         self.rect.center = self.pos

animal_props = {
    "sheep" : {
        "speed" : 1, "max_health" : 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance" : 10, #distance that animal can move when activated
        "activation_distance" : 10, #distance to player before movement
        "item_drop_on_death" : "True", #lookup from list
        "start_coord" : (0,0), #starting coor of first image in sprite sheet
        "animation_quantity" : 4, # number of sprites we're using for the animal animation
       },
    "dog" : {
        "speed" : 1, "max_health" : 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance" : 10, #distance that animal can move when activated
        "activation_distance" : 10, #distance to player before movement
        "item_drop_on_death" : "True", #lookup from list
        "start_coord" : (0,32), #starting coor of first image in sprite sheet
        "animation_quantity" : 4, # number of sprites we're using for the animal animation
       },
    "bull" : {
        "speed" : 1, "max_health" : 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance" : 10, #distance that animal can move when activated
        "activation_distance" : 10, #distance to player before movement
        "item_drop_on_death" : "True", #lookup from list
        "start_coord" : (0,64), #starting coor of first image in sprite sheet
        "animation_quantity" : 4, # number of sprites we're using for the animal animation
       },
    "cat" : {
        "speed" : 1, "max_health" : 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance" : 10, #distance that animal can move when activated
        "activation_distance" : 10, #distance to player before movement
        "item_drop_on_death" : "True", #lookup from list
        "start_coord" : (0,96), #starting coor of first image in sprite sheet
        "animation_quantity" : 4, # number of sprites we're using for the animal animation
       },
    "capybara": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 128),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "crocodile": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 160),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "bear": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 192),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "kangaroo": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 224),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "lion": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 256),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "squirrel": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 288),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "llama": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 320),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "chicken": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 352),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "rabbit": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 384),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "pig": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 416),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "hedgehog": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 60,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 448),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "fox" : {
        "speed" : 1, "max_health" : 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance" : 10, #distance that animal can move when activated
        "activation_distance" : 10, #distance to player before movement
        "item_drop_on_death" : "True", #lookup from list
        "start_coord" : (0,480), #starting coor of first image in sprite sheet
        "animation_quantity" : 4, # number of sprites we're using for the animal animation
       },
    "mouse": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 512),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "monkey": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 0),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "duck": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 32),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "guinea_pig": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 64),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "donkey": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 96),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "goat": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 128),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "cow": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 160),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "elephant": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 192),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "panda": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 224),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "penguin": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 256),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "polar_bear": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 288),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "deer": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 320),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "horse": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 352),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "rhino": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 384),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "seal": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 10,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 416),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    "tiger": {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 60,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (128, 448),  # starting coor of first image in sprite sheet
        "animation_quantity": 4,  # number of sprites we're using for the animal animation
    },
    # End of spritesheet animals with 4 animations.

    # Animals not on the original sprite sheet
    "rabbit_2" : {
        "speed": 1, "max_health": 100, "friendly": "True",
        "audio_folder": "location",
        "max_travel_distance": 8,  # distance that animal can move when activated
        "activation_distance": 10,  # distance to player before movement
        "item_drop_on_death": "True",  # lookup from list
        "start_coord": (0, 0),  # starting coor of first image in sprite sheet
        "animation_quantity": 8,  # number of sprites we're using for the animal animation
    }
}
animal_drops = {
            "chicken": { "type": "chicken_meat", "quantity" : 1},
            "rabbit": { "type": "rabbit_meat", "quantity" : 1},
            "hedgehog": { "type": "hedgehog_meat", "quantity" : 1},
            "capybara": { "type": None, "quantity" : 0},
            "duck": { "type": None, "quantity" : 0},
            }