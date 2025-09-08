import pygame
from config.config import *
from src.entities.sprites.sprite_manager import Entity

# todo: create a list of sprite sheets here with relevant info such as columns and pertinent ids

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


"""
Tricksy, we animate sand and water, water is a collision block and should be on the 
collision layer, sand is walkable and on another layer so if we put sand and water on the same layer we
have a potential conflict there but also with the logic for creating them.

for now we can use water as a simpler example, each tile has two tiles in total that can be used for the 
animation.  it's counterpart is always 10 tiles over from the original.

if we can't pull through it's tileset x and y we will need a dict to store that info, but it needs
to a bit more rigourous as there are 50 odd tiles.  If we can pull through the tile id, that would help.
"""
animated_terrain = {
    "id": None,
    "type": None,
    "terrain": None,
    "x": None,
    "y": None,
    "image": None,
}

# tile1 id 109, x 1440, y 32
# tile2 id 119, x 1760, y 32
#
# 13 down, 10 across



class AnimatedTerrain(Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)

        # build the list once
        #
        # if animated_tile_properties is None:
        #     animated_tile_properties = self.build_list_of_tile_ids_and_corresponding_coordinates()


        self.tile_id = tile_properties["id"]


        # look up the details from the id in the dict
        self.image_1_xy = ()
        self.image_2_xy = ()

        self.images = [
        ]

    animated_tile_properties = None
    """
    tiles start at 109, the counterpart is ten tiles across so 109 is mapped with 119 for example
    109 would be 1440,32 and 119 would be 1440+(10*320), 32.
    every 20 tiles we need to increment y by 32 as we drop a layer, but this isn't accurate in this
    tileset as they are at the end of the page. a difference of 64 each time
    109 : 127 (+18)
    173 : 191 (+18)
    # this currently builds the correct mapping dict of tile ids and the corresponding x,y
    # on the sprite sheet
    """
    def build_list_of_tile_ids_and_corresponding_coordinates(self):
        starting_id_list=[109,173,237,301,365,429,493,557,621,685,749,813,877]
        y = 32
        resultset = {}
        for start_id in starting_id_list:
            x=1408
            for i in range(18):
                x+=32
                resultset[start_id+i] = (x, y)
            y+=32
        print(resultset)
        return resultset




