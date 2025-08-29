import csv

import pygame
from pytmx.util_pygame import load_pygame
from config.config import TILE_SIZE
from src.entities.sprites import Ground, Block

map_folder_location = "assets/maps"
image_path = "assets/generic"

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(image_path + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, engine, tile_kinds, stage):
        # self.data = data
        self.engine = engine
        self.tile_kinds = tile_kinds
        # engine.background_drawables.append(self)

        # Set up the tiles from loaded data
        self.tiles = []

        # How big in pixels are the tiles?
        self.tile_size = TILE_SIZE

        self.stage = stage
        self.tiled_map = self.get_stage_map(self.stage)
        # self.get_collision_objects_to_draw()

    # def get_collision_objects_to_draw(self):
    #     from beanie_game.src.core.camera import camera
    #     for layer in self.tiled_map:
    #         if layer.name == "Collision":
    #             # col_sprites = self.tiled_map.get_layer_by_name("Collision")
    #             # # self.engine.collisions_drawables.append(col_sprites)
    #             for x, y, image in layer.tiles():
    #                 self.engine.collisions_drawables.append((x, y, image))

    def get_stage_map(self, stage):
        if stage == "start":
            # map_filename='/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/newmaptest.tmx'
            # map_filename='/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/starting_area.tmx'
            map_filename = '/Users/sgreen/PycharmProjects/BeanieGame/assets/maps/area1_withobjects.tmx'
            tiled_map = load_pygame(map_filename)
            return tiled_map
        else:
            return None


    # def draw(self, screen):
    #     from beanie_game.src.core.camera import camera
    #     for layer in self.tiled_map:
    #         if layer.name == "Background" or layer.name == "Background2":
    #             for x, y, image in layer.tiles():
    #                 # block creation doesnt' take in camera
    #                 # Block(self, x, y, image=image)
    #                 # screen = pygame.display.get_surface()
    #                 # todo: this is being drawn every frame, if it's taking in the camera
    #                 # every frame then it'll be updated accordingly.  we're passing in the
    #                 # screen, which is the camera, so as it moves, the image moves,
    #                 # we need to draw once....like the blocks.
    #
    #                 # good display but moves with camera
    #                 # screen.blit(image, (x * self.tile_size - camera.x, y * self.tile_size - camera.y))
    #                 # good display but moves with camera
    #                 screen.blit(image, (x * self.tile_size, y * self.tile_size))
    #                 # everything displays in top corner
    #                 # screen.blit(image, (x, y))
    #                 # top corner for all
    #                 # screen.blit(image, (x-camera.x, y-camera.y))




