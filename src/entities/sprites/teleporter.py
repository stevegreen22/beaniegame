import pygame

from config.config import TELEPORT_LAYER
from src.entities.sprites.sprite_manager import Entity


def teleport(area_file):
    from src.core.area import area
    area.load_file(area_file)

class Teleporter(Entity):
    def __init__(self, map, x, y, image=None, tile_properties=None):
        super().__init__(map, x, y, image, tile_properties)
        self._layer = TELEPORT_LAYER

        self.groups = [self.map.all_sprites, self.map.teleporters]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

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

teleports_map = {"identifier" :
                         {"source_map" : "name",
                          "target_map" : "name",
                          "source_x" : 1,
                          "source_y" : 1,
                          "target_x" : 1,
                          "target_y" : 1,}}