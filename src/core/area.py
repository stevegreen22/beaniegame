import csv
import pygame
from src.core.map import Map

area = None
# map_folder_location = "assets/maps"
# filename = "/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/area_map_terrain_layer.csv"


class Area:
    def __init__(self, engine, tile_types, stage, editor_mode=False, teleporter_properties=None):
        global area
        area = self
        self.engine = engine
        self.tile_types = tile_types
        self.editor_mode = editor_mode
        self.stage = stage
        self.teleporter_properties = teleporter_properties

        # self.load_file(engine, area_file)
        # self.tile_map_data = self.convert_csv_to_2d_list(filename)

        # have a list of maps for the current area/world
        self.area_maps = []
        self.populate_area_maps(self.stage, True)


    def populate_area_maps(self, stage, current_map):
        map = Map(self.engine, self.tile_types, stage, current_map)
        self.area_maps.append(map)

    # def convert_csv_to_2d_list(self, csv_file: str):
    #     tile_map = []
    #     with open(csv_file, "r") as f:
    #         for map_row in csv.reader(f):
    #             tile_map.append(list(map(int, map_row)))
    #     return tile_map
    #
    #
    # def load_file(self, engine, area_file):
    #     # Read all the data from the file
    #     # file = open(map_folder_location + "/" + area_file, "r")
    #     file = open("/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/area_map_terrain_layer.csv", "r")
    #     data = file.read()
    #     file.close()
    #
    #     # Load the map
    #     self.map = Map(engine, data, self.tile_types, stage=self.stage)


## Todo: take current map and set current to false
    # create new map, set it to current and add to the list
    # update player coordiate
    def build_new_map(self, teleporter_properties):
        # self.reset_sprites()
        map_stage = teleporter_properties['target_map']
        self.map = None
        self.map = Map(self.engine, None, map_stage, True)
        self.area_maps.append(map_stage)


    # clear out everything for map transitions
    def reset_sprites(self):
        self.map.all_sprites.empty()
        self.map.animals.empty()
        # all_groups = []
        # for group in all_groups:
        #     group.empty()