import math

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




class AnimatedTerrain(Entity):
    def __init__(self, engine, x, y, image=None, tile_properties=None):
        super().__init__(engine, x, y, image, tile_properties)

        self._layer = GROUND_LAYER
        if tile_properties['terrain'] == 'water':
            self.groups = [self.engine.all_sprites, self.engine.blocks]
        else:
            self.groups = [self.engine.all_sprites, self.engine.animated_terrain]
        pygame.sprite.Sprite.__init__(self, self.groups)

        # build the list once
        self.animated_tile_properties = animated_tile_properties

        self.tile_id = tile_properties["id"]

        # look up the details from the id in the dict
        self.image_1_xy = self.animated_tile_properties[self.tile_id]
        id_2 = int(self.tile_id + 10)
        self.image_2_xy = self.animated_tile_properties[id_2]

        self.images = [
            self.engine.main_terrain_spritesheet.get_sprite(self.image_1_xy[0], self.image_1_xy[1], self.width, self.height),
            self.engine.main_terrain_spritesheet.get_sprite(self.image_2_xy[0], self.image_2_xy[1], self.width, self.height),
            self.engine.main_terrain_spritesheet.get_sprite(self.image_1_xy[0], self.image_1_xy[1], self.width,
                                                            self.height),
            self.engine.main_terrain_spritesheet.get_sprite(self.image_2_xy[0], self.image_2_xy[1], self.width,
                                                            self.height),
        ]
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_loop = 1
        self.movement_loop = 0

    def update(self):
        self.animate()


    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1  # every ten frames we change image
        if self.animation_loop >= 4:
            self.animation_loop = 1

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
            for i in range(19):
                x+=32
                resultset[start_id+i] = (x, y)
            y+=32
        print(resultset)
        return resultset



# tile1 id 109, x 1440, y 32
# tile2 id 119, x 1760, y 32
# 13 down, 10 across
animated_tile_properties = {
     109: (1440, 32), 110: (1472, 32), 111: (1504, 32), 112: (1536, 32), 113: (1568, 32), 114: (1600, 32), 115: (1632, 32), 116: (1664, 32), 117: (1696, 32),
     118: (1728, 32), #blank
     119: (1760, 32), 120: (1792, 32), 121: (1824, 32), 122: (1856, 32), 123: (1888, 32), 124: (1920, 32), 125: (1952, 32), 126: (1984, 32), 127: (2016, 32),
     173: (1440, 64), 174: (1472, 64), 175: (1504, 64), 176: (1536, 64), 177: (1568, 64), 178: (1600, 64), 179: (1632, 64), 180: (1664, 64), 181: (1696, 64),
     182: (1728, 64),
     183: (1760, 64), 184: (1792, 64), 185: (1824, 64), 186: (1856, 64), 187: (1888, 64),188: (1920, 64), 189: (1952, 64), 190: (1984, 64), 191: (2016, 64),
     237: (1440, 96), 238: (1472, 96),239: (1504, 96), 240: (1536, 96), 241: (1568, 96), 242: (1600, 96), 243: (1632, 96), 244: (1664, 96), 245: (1696, 96),
     246: (1728, 96),
     247: (1760, 96), 248: (1792, 96), 249: (1824, 96), 250: (1856, 96), 251: (1888, 96), 252: (1920, 96), 253: (1952, 96), 254: (1984, 96), 255: (2016, 96),
     301: (1440, 128), 302: (1472, 128), 303: (1504, 128), 304: (1536, 128), 305: (1568, 128), 306: (1600, 128), 307: (1632, 128),308: (1664, 128), 309: (1696, 128),
     310: (1728, 128),
     311: (1760, 128), 312: (1792, 128), 313: (1824, 128),314: (1856, 128), 315: (1888, 128), 316: (1920, 128), 317: (1952, 128), 318: (1984, 128), 319: (2016, 128),
     365: (1440, 160), 366: (1472, 160), 367: (1504, 160), 368: (1536, 160), 369: (1568, 160), 370: (1600, 160), 371: (1632, 160), 372: (1664, 160), 373: (1696, 160),
     374: (1728, 160),
     375: (1760, 160), 376: (1792, 160),377: (1824, 160), 378: (1856, 160), 379: (1888, 160), 380: (1920, 160), 381: (1952, 160), 382: (1984, 160), 383: (2016, 160),
     429: (1440, 192), 430: (1472, 192), 431: (1504, 192), 432: (1536, 192), 433: (1568, 192),434: (1600, 192), 435: (1632, 192), 436: (1664, 192), 437: (1696, 192),
     438: (1728, 192),
     439: (1760, 192), 440: (1792, 192), 441: (1824, 192), 442: (1856, 192), 443: (1888, 192), 444: (1920, 192), 445: (1952, 192), 446: (1984, 192), 447: (2016, 192),
     493: (1440, 224), 494: (1472, 224), 495: (1504, 224), 496: (1536, 224), 497: (1568, 224), 498: (1600, 224), 499: (1632, 224), 500: (1664, 224), 501: (1696, 224),
     502: (1728, 224),
     503: (1760, 224), 504: (1792, 224), 505: (1824, 224), 506: (1856, 224), 507: (1888, 224), 508: (1920, 224), 509: (1952, 224), 510: (1984, 224), 511: (2016, 224),
     557: (1440, 256), 558: (1472, 256), 559: (1504, 256),560: (1536, 256), 561: (1568, 256), 562: (1600, 256), 563: (1632, 256), 564: (1664, 256), 565: (1696, 256),
     566: (1728, 256),
     567: (1760, 256), 568: (1792, 256), 569: (1824, 256), 570: (1856, 256), 571: (1888, 256), 572: (1920, 256), 573: (1952, 256), 574: (1984, 256), 575: (2016, 256),
     621: (1440, 288), 622: (1472, 288),623: (1504, 288), 624: (1536, 288), 625: (1568, 288), 626: (1600, 288), 627: (1632, 288), 628: (1664, 288), 629: (1696, 288),
     630: (1728, 288),
     631: (1760, 288), 632: (1792, 288), 633: (1824, 288), 634: (1856, 288),635: (1888, 288), 636: (1920, 288), 637: (1952, 288), 638: (1984, 288), 639: (2016, 288),
     685: (1440, 320), 686: (1472, 320), 687: (1504, 320), 688: (1536, 320), 689: (1568, 320), 690: (1600, 320), 691: (1632, 320), 692: (1664, 320), 693: (1696, 320),
     694: (1728, 320),
     695: (1760, 320), 696: (1792, 320), 697: (1824, 320),698: (1856, 320), 699: (1888, 320), 700: (1920, 320), 701: (1952, 320), 702: (1984, 320), 703: (2016, 320),
     749: (1440, 352), 750: (1472, 352), 751: (1504, 352), 752: (1536, 352), 753: (1568, 352), 754: (1600, 352),755: (1632, 352), 756: (1664, 352), 757: (1696, 352),
     758: (1728, 352),
     759: (1760, 352), 760: (1792, 352), 761: (1824, 352), 762: (1856, 352), 763: (1888, 352), 764: (1920, 352), 765: (1952, 352), 766: (1984, 352), 767: (2016, 352),
     813: (1440, 384), 814: (1472, 384), 815: (1504, 384), 816: (1536, 384), 817: (1568, 384),818: (1600, 384), 819: (1632, 384), 820: (1664, 384), 821: (1696, 384),
     822: (1728, 384),
     823: (1760, 384), 824: (1792, 384), 825: (1824, 384), 826: (1856, 384), 827: (1888, 384), 828: (1920, 384), 829: (1952, 384),830: (1984, 384), 831: (2016, 384),
     877: (1440, 416), 878: (1472, 416), 879: (1504, 416), 880: (1536, 416), 881: (1568, 416), 882: (1600, 416), 883: (1632, 416), 884: (1664, 416), 885: (1696, 416),
     886: (1728, 416),
     887: (1760, 416), 888: (1792, 416), 889: (1824, 416), 890: (1856, 416), 891: (1888, 416), 892: (1920, 416), 893: (1952, 416), 894: (1984, 416), 895: (2016, 416)
}
