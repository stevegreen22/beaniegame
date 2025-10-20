import pygame

from config.config import TELEPORT_LAYER
from src.entities.sprites.sprite_manager import Entity


def teleport(area_file):
    from src.core.area import area
    area.load_file(area_file)


# will need a 'special door' to go to a new world.
teleport_counterpart_map = {
    1:2, #door 1 links to door 2
    2:1, #door 2 links to door 1
}

class Teleporter(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = TELEPORT_LAYER

        self.groups = [self.map.all_sprites, self.map.teleporters]
        pygame.sprite.Sprite.__init__(self, self.groups)

        if tile_properties is not None:
            self.tile_properties = tile_properties
            self.id = tile_properties["id"]
            self.counterpart_teleporter = teleport_counterpart_map.get(int(self.id))
            self.teleporter_info = self.teleport_info_map.get(int(self.id))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# two doors, they link to each other's id.


    teleport_info_map = {
        1: {
            "source_map": "world_1_1",
            "target_map": "world_1_2",#2
            "counterpart": "2"
        },
        2: {
            "source_map": "world_1_2",#2
            "target_map": "world_1_1",
            "counterpart": "1"
        },
        # same map test
        3: {
            "source_map": "world_1_1",
            "target_map": "world_1_1",
            "counterpart": "4"
        },
        4: {
            "source_map": "world_1_1",
            "target_map": "world_1_1",
            "counterpart": "3"
        },
        5: {
            "source_map": "world_1_1",
            "target_map": "world_1_1",
            "counterpart": "6"
        },
        6: {
            "source_map": "world_1_1",
            "target_map": "world_1_1",
            "counterpart": "5"
        }
    }
"""
Issue is that I  don't want to store lots of data in each of the tiles and
I don't want to have multiple door tiles with each one pointing to a 
different location.
ideally I want it so that one door links to it's counterpart in another
map, but i want the position of the door to make sense.

if a door is 0,0 on map 1, when we enter it and come out in map two, our location
should also be 0,0 so that there is some continuity, tunnel maps can be built
in the mountain that can link other maps etc.

data already available is the tile x and y which is where the player will spawn
when they return to the door.

We need:
Map the door is on, it's source
coordinates of the door

map the exit is on, it's destination
coordinates of the door

if the coords are the same we can get that from the tile.


"""

"""
for each door.
    - current x and y, can get from it's rect
    - target x and y, needs to be known upfront
    - target map
    - current map
    - it's unique identifier
    
    
    ooooor, each door is a pair...
    door 1, door 2.
    from this we can get the rest of the details?
    
"""
