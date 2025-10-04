import pygame
from config.config import *
from src.entities.inventory import Inventory
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
            self.groups = [map.all_sprites, self.map.foreground_trees]


        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# each chest object much like a door will have it's own set of attributes.
# either need to give each chest an id and map that in code,
# or give each chest a list of properties.
# easier to manage in code
chest_loot = {
    1 : {
        "mana_potion" : 2,
        "cooked_food" : 2,
        "wooden_sword": 1
    },
    2 : {
        "fireball_spell" : 1,
        "cooked_food" : 1,
    }
}


"""
Instead of having 50 different chests, is there a way instead to have the contents randomly
generated. Certain things will need to be static though, but perhaps weapons and spells
can be given by NPCs instead.  That way I won't need 50 odd chests with 50 different combinations
of loot.  They can have a random number of coins, random potions etc.
"""

class Chest(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if tile_properties is not None:
            if tile_properties.type is "chest":
                chest_loot_id = tile_properties["chest_id"]
                self.inventory = Inventory("chest", chest_loot[chest_loot_id])

