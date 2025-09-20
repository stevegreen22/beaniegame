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
from src.entities.sprites.teleporter import Teleporter

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


    def new(self):
        # new game starts
        self.playing = True

        # Create the Starting area, may be moved into 'stages' later
        #world map, starting area world,
        # area contains multiple maps.
        # self.area = Area(self, None, stage="start")
        self.build_starting_area()
        #we want the player to persis because of inventory etc
        self.player = Player(self, 10, 10)

    def build_starting_area(self):
        self.area = Area(self, None, stage="start")


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # all_sprites consists of player, ground and blocks
        current_map = None
        for map in self.area.area_maps:
            if map.current_map:
                current_map = map
        current_map.all_sprites.update()


    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(DARK_GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles

        current_map = None
        for map in self.area.area_maps:
            if map.current_map:
                current_map = map

        current_map.animated_terrain.draw(self.screen)  # needs this to animate sand but can then be walked under by player
        current_map.collision_blocks.draw(self.screen)
        current_map.all_sprites.draw(self.screen)
        current_map.enemies.draw(self.screen)
        current_map.npcs.draw(self.screen)
        current_map.traps.draw(self.screen)
        # self.player_group.draw(self.screen)
        current_map.animals.draw(self.screen)

        self.clock.tick(FPS)
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