import pygame
from pytmx.util_pygame import load_pygame
from config.config import TILE_SIZE
from src.entities.sprites.static_sprites import Ground, Block

map_folder_location = "assets/maps"
image_path = "assets/maps/img"

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(image_path + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, engine, tile_kinds, stage):
        self.engine = engine
        self.tile_kinds = tile_kinds

        # Set up the tiles from loaded data
        self.tiles = []

        # How big in pixels are the tiles?
        self.tile_size = TILE_SIZE

        self.stage = stage
        self.tiled_map = self.get_stage_map(self.stage)

    def get_stage_map(self, stage):
        if stage == "start":
            # map_filename = f"{map_folder_location}/tmx/area1_withobjects.tmx"
            map_filename = f"{map_folder_location}/tmx/area_1_main.tmx"
            # map_filename = f"{map_folder_location}/tmx/{stagebla}.tmx"
            tiled_map = load_pygame(map_filename)
            return tiled_map
        else:
            return None





