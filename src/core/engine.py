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
        self.current_map = None

    def new(self):
        # new game starts
        self.playing = True

        # Create the Starting area, may be moved into 'stages' later
        #world map, starting area world,
        # area contains multiple maps.
        # self.area = Area(self, None, stage="start")
        self.build_world()
        #we want the player to persis because of inventory etc
        self.player = Player(self, 10, 10)
        self.current_map = self.area.current_map

    def build_world(self):
        self.area = Area(stage="start_world_1")


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # all_sprites consists of player, ground and blocks
        self.current_map = self.area.current_map
        self.current_map.all_sprites.update()


    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(DARK_GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles

        self.current_map = self.area.current_map

        self.current_map.animated_terrain.draw(self.screen)  # needs this to animate sand but can then be walked under by player
        self.current_map.collision_blocks.draw(self.screen)
        self.current_map.all_sprites.draw(self.screen)
        self.current_map.enemies.draw(self.screen)
        self.current_map.npcs.draw(self.screen)
        self.current_map.traps.draw(self.screen)
        self.current_map.player_group.draw(self.screen)
        self.current_map.animals.draw(self.screen)

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