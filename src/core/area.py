import csv
import pygame
from src.core.map import Map

area = None
map_folder_location = "assets/maps"
filename = "/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/area_map_terrain_layer.csv"


class Area:
    def __init__(self, engine, area_file, tile_types, stage, editor_mode=False):
        global area
        area = self
        self.engine = engine
        self.tile_types = tile_types
        self.editor_mode = editor_mode
        # self.load_file(engine, area_file)
        # self.tile_map_data = self.convert_csv_to_2d_list(filename)
        self.stage = stage
        self.map = Map(engine, self.tile_types, self.stage)


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