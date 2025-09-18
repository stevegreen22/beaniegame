import pygame

from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DARK_GREEN, TILE_LAYERS
from src.core.area import Area
from src.entities.player import Player
from src.entities.sprites.animated_terrain import AnimatedTerrain
from src.entities.sprites.animals import Animal
from src.entities.sprites.enemies import Enemy
from src.entities.sprites.statics import Block,Ground, Trap
from src.entities.sprites.npcs import NPC
from src.entities.sprites.sprite_manager import Spritesheet

engine = None
default_width = WINDOW_WIDTH
default_height = WINDOW_HEIGHT

class Engine:
    def __init__(self, game_title):
        from src.core.camera import create_screen
        global engine
        engine = self

        # self.usables = []
        # self.effects = []

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        # self.stages = {}
        # self.current_stage = None
        self.clock = pygame.time.Clock()
        self.running = True

        self.main_player_spritesheet = Spritesheet('assets/characters/player/main_character.png')
        # self.main_player_spritesheet = Spritesheet('assets/characters/player/red_main_spritesheet.png')
        self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/monster_spritesheet.png')
        # self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/orc_right_spritesheet_resize_test.png')
        self.main_animal_spritesheet = Spritesheet('assets/animals/animal_spritesheet.png')
        self.rabbit_2_spritesheet = Spritesheet('assets/animals/rabbits.png')
        self.main_terrain_spritesheet = Spritesheet('assets/maps/tmx/img/terrain.png')

    def new(self):
        # new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.collision_blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.traps = pygame.sprite.LayeredUpdates()
        self.animals = pygame.sprite.LayeredUpdates()
        self.foreground_trees = pygame.sprite.LayeredUpdates() #trees that the player can walk behind.
        self.animated_terrain = pygame.sprite.LayeredUpdates()
        self.collision_group = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()

        # Create the Starting area, may be moved into 'stages' later
        self.area = Area(self, None, stage="start")
        self.build_terrain()
        self.build_collisions()
        self.player = Player(self, 10, 10)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # all_sprites consists of player, ground and blocks
        self.all_sprites.update()

    def build_terrain(self):
        for layer in self.area.map.tiled_map:
            layer_id = TILE_LAYERS[layer.name]
            if layer.name =="BaseTerrain" or layer.name == "BaseTerrain2" or layer.name == "TreeForeground":
                for x, y, image in layer.tiles():
                    tile_id = self.area.map.tiled_map.get_tile_gid(x, y, layer_id)  # collision layer
                    tile_properties = self.area.map.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        if tile_properties['type'] == "animated_block" and tile_properties['terrain'] == "sand":
                            AnimatedTerrain(self, x, y, tile_properties=tile_properties)
                        if tile_properties["type"] == "tree":
                            Ground(self, x, y, image=image, tile_properties=tile_properties)
                    Ground(self, x , y, image=image)

            if layer.name == "CollisionBlocks" or layer.name == "CollisionBlocks2":
                for x, y, image in layer.tiles():
                    tile_id = self.area.map.tiled_map.get_tile_gid(x, y, layer_id)  # collision layer
                    tile_properties = self.area.map.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        print(f"Tile Properties: {tile_properties}")
                        tile_type = tile_properties['type']
                        if tile_type == "animated_block":
                            if tile_properties['terrain'] == "water":
                                AnimatedTerrain(self, x, y, tile_properties=tile_properties)
                    # normal generic collision block such as the wall, pond or lava...
                    else:
                        Block(self, x, y, image=image, tile_properties=tile_properties)


    # Todo: CollisionMid shoudl be renamed for collision mobs, all mob in map should be on this
    # layer.  the '3' below dictates the tiles coming from that layer.
    def build_collisions(self):
        for layer in self.area.map.tiled_map:
            if layer.name =="CollisionMobs":
                layer_id = TILE_LAYERS["CollisionMobs"]
                for x, y, image in layer.tiles():
                    tile_id = self.area.map.tiled_map.get_tile_gid(x, y, layer_id)
                    # todo: this is only getting properties from layer 4, collision mid.
                    tile_properties = self.area.map.tiled_map.get_tile_properties_by_gid(tile_id)
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



    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(DARK_GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles
        self.all_sprites.draw(self.screen)
        self.animated_terrain.draw(self.screen) #needs this to animate sand but can then be walked under by player
        self.collision_blocks.draw(self.screen)
        self.enemies.draw(self.screen)
        self.npcs.draw(self.screen)
        self.traps.draw(self.screen)
        self.player_group.draw(self.screen)
        self.animals.draw(self.screen)
        self.clock.tick(FPS)
        # self.player.draw()
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False


    def game_over(self):
        pass


    def intro_screen(self):
        pass