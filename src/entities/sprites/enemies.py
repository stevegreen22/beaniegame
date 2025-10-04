import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity
import math
import random



enemy_props = { "whitey" :{
                    "speed": 3, "max_health": 100,
                    "audio_folder": "<<location>>",
                    "max_travel_distance": 10,  # distance that animal can move when activated
                    "activation_distance": 10,  # distance to player before movement
                    "item_drop_on_death": "True",  # lookup from list
                    "movement_animation_quantity": 6,  # number of movement sprites
                    "left_right_movement_start_coord": (0, 192),  # starting coordinate in sprite sheet
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
                    "left_right_movement_start_coord": (0, 256),  # starting coordinate in sprite sheet
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
                    "left_right_movement_start_coord": (0, 128),  # starting coordinate in sprite sheet
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
# todo: add collision with trees etc.

class Enemy(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = ENEMY_LAYER

        self.groups = self.map.all_sprites, self.map.enemies
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
            self.move_sprites.append(self.map.main_enemy_spritesheet.get_sprite(self.start_xy[0] + (TILE_SIZE * i), self.start_xy[1], self.width, self.height))

        self.right_animations = self.move_sprites
        self.left_animations = [pygame.transform.flip(img, True, False) for img in self.move_sprites]

        self.image = self.map.main_enemy_spritesheet.get_sprite(0, 64, self.width, self.height)
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