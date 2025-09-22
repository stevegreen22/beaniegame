import csv
import pygame
from src.core.map import Map

area = None
# map_folder_location = "assets/maps"
# filename = "/Users/sgreen/PycharmProjects/PythonProject1/beanie_game/assets/maps/area_map_terrain_layer.csv"


class Area:
    def __init__(self, stage, editor_mode=False):
        global area
        area = self
        self.editor_mode = editor_mode
        self.stage = stage

        # have a list of maps for the current area/world
        self.area_maps = []
        self.dict_maps = {}
        self.populate_area_maps()
        self.current_map = self.get_current_map()


    # With this being our world creator, at the start, we create and load the maps needed.
    def populate_area_maps(self):
        if self.stage == "start_world_1":
            current_map = Map("world_1_1", is_current_map=True)
            # self.area_maps.append(current_map)
            self.dict_maps["world_1_1"] = current_map
            print(f"adding map {current_map} to list")
            current_map = Map("world_1_2", is_current_map=False)
            # self.area_maps.append(current_map)
            self.dict_maps["world_1_2"] = current_map
            print(f"adding map {current_map} to list")
        elif self.stage == "end":
            pass
        else:
            pass


    def get_current_map(self):
        for map in self.dict_maps.values():
            if not map.is_current_map:
                pass
            else:
                return map

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
    def load_new_map(self, teleporter_properties):
        # self.reset_sprites()
        map_stage = 'world_1_2' #teleporter_properties['target_map']
        # set the current map to not current
        self.current_map.is_current_map = False
        self.dict_maps[map_stage].is_current_map = True

        self.current_map = self.get_current_map()



    # clear out everything for map transitions
    def reset_sprites(self):
        self.map.all_sprites.empty()
        self.map.animals.empty()
        # all_groups = []
        # for group in all_groups:
        #     group.empty()