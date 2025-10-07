import pygame
from pytmx.util_pygame import load_pygame
from config.config import TILE_SIZE, TILE_LAYERS
from src.entities.sprites.animals import Animal
from src.entities.sprites.animated_terrain import AnimatedTerrain
from src.entities.sprites.enemies import Enemy
from src.entities.sprites.npcs import NPC
from src.entities.sprites.sprite_manager import Spritesheet
from src.entities.sprites.statics import Ground, Block, Trap
from src.entities.sprites.teleporter import Teleporter

map_folder_location = "assets/maps"
image_path = "assets/maps/img"

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(image_path + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, stage, teleporter_list, is_current_map):
        self.is_current_map = is_current_map

        self.tiles = []
        self.tile_size = TILE_SIZE

        self.stage = stage
        self.tiled_map = self.get_stage_map(self.stage)

        self.all_sprite_list = []

        self.collision_blocks = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.collision_blocks)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.all_sprites)
        self.enemies = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.enemies)
        self.npcs = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.npcs)
        self.traps = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.traps)
        self.animals = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.animals)
        self.animated_terrain = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.animated_terrain)
        self.player_group = pygame.sprite.LayeredUpdates()
        self.all_sprite_list.append(self.player_group)
        self.attacks = pygame.sprite.LayeredUpdates()
        # self.all_sprite_list.append(self.attacks)
        self.foreground_trees = pygame.sprite.LayeredUpdates()  # trees that the player can walk behind.
        self.all_sprite_list.append(self.foreground_trees)

        self.collision_group = pygame.sprite.LayeredUpdates()
        # self.all_sprite_list.append(self.collision_group)

        self.teleporters = pygame.sprite.LayeredUpdates()
        # self.all_sprite_list.append(self.teleporters)

        self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/monster_spritesheet.png')
        # self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/orc_right_spritesheet_resize_test.png')
        self.main_animal_spritesheet = Spritesheet('assets/animals/animal_spritesheet.png')
        self.rabbit_2_spritesheet = Spritesheet('assets/animals/rabbits.png')
        self.main_terrain_spritesheet = Spritesheet('assets/maps/tmx/img/terrain.png')

        self.teleporter_list = teleporter_list

        self.build_terrain()
        self.build_mob_entities()


    def get_stage_map(self, stage):
        tiled_map = None
        if stage == "world_1_1":
            map_filename = f"{map_folder_location}/tmx/area_1_main.tmx"
            # map_filename = f"{map_folder_location}/tmx/{stagebla}.tmx"
            tiled_map = load_pygame(map_filename)
        elif stage == "world_1_2":
            map_filename = f"{map_folder_location}/tmx/area1_withobjects.tmx"
            tiled_map = load_pygame(map_filename)
        return tiled_map


    def build_terrain(self):
        for layer in self.tiled_map:
            layer_id = TILE_LAYERS[layer.name]
            if layer.name =="BaseTerrain" or layer.name == "BaseTerrain2" or layer.name == "TreeForeground":
                for x, y, image in layer.tiles():
                    tile_id = self.tiled_map.get_tile_gid(x, y, layer_id)
                    tile_properties = self.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        if tile_properties['type'] == "animated_block" and tile_properties['terrain'] == "sand":
                            AnimatedTerrain(self, x, y, tile_properties=tile_properties)
                        if tile_properties["type"] == "tree":
                            Ground(self, x, y, image=image, tile_properties=tile_properties)
                        if tile_properties["type"] == "teleporter":
                            tp = Teleporter(self, x, y, image=image, tile_properties=tile_properties)
                            self.teleporter_list[tile_properties["id"]] = tp
                    Ground(self, x , y, image=image)

            if layer.name == "CollisionBlocks" or layer.name == "CollisionBlocks2":
                for x, y, image in layer.tiles():
                    tile_id = self.tiled_map.get_tile_gid(x, y, layer_id)  # collision layer
                    tile_properties = self.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        print(f"Tile Properties: {tile_properties}")
                        tile_type = tile_properties['type']
                        if tile_type == "animated_block":
                            if tile_properties['terrain'] == "water" or tile_properties['terrain'] == "waterfall":
                                AnimatedTerrain(self, x, y, tile_properties=tile_properties)
                    else:
                        Block(self, x, y, image=image, tile_properties=tile_properties)


    def build_mob_entities(self):
        for layer in self.tiled_map:
            if layer.name =="CollisionMobs":
                layer_id = TILE_LAYERS["CollisionMobs"]
                for x, y, image in layer.tiles():
                    tile_id = self.tiled_map.get_tile_gid(x, y, layer_id)
                    # todo: this is only getting properties from layer 4, collision mid.
                    tile_properties = self.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        print(f"Tile Properties: {tile_properties}")
                        tile_type = tile_properties['type']
                        if tile_type == "mob":
                            Enemy(self, x, y, image=image, tile_properties=tile_properties)
                        elif tile_type == "animal":
                            Animal(self, x, y, tile_properties=tile_properties)
                        elif tile_type == "npc":
                            NPC(self, x, y, image=image, tile_properties=tile_properties)
                        elif tile_type == "trap":
                            Trap(self, x, y, image=image, tile_properties=tile_properties)
                    else:
                        pass
                        # this is where water was originally being created.
                        # Block(self, x , y, image=image)





