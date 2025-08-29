import pygame
from pytmx import pytmx, TiledElement

from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, FPS, GREEN, TILE_SIZE, DARK_GREEN
from src.core.area import Area
from src.entities.player import Player
from src.entities.sprites import Spritesheet, Ground, Block, Enemy

engine = None
default_width = WINDOW_WIDTH
default_height = WINDOW_HEIGHT

class Engine:
    def __init__(self, game_title):
        from src.core.camera import create_screen
        global engine
        engine = self

        # self.active_objs = []
        # self.usables = []
        # self.effects = []

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        # self.stages = {}
        # self.current_stage = None
        self.clock = pygame.time.Clock()
        self.running = True

        # self.character_spritesheet = Spritesheet('../../assets/generic/character.png')
        self.char_test_spritesheet = Spritesheet('assets/generic/char_test.png')
        # self.char_test_spritesheet = Spritesheet('assets/EditedSprites/PandaCharacter.png')
        # self.terrain_spritesheet = Spritesheet('../../assets/generic/terrain.png')
        # self.main_character_spritesheet = Spritesheet('../../assets/characters/main_character_male/Character_Walk.png')
        self.collision_objects_to_draw = []


    def new(self):
        # new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        # Create the Starting area, may be moved into 'stages' later
        self.area = Area(self, None, stage="start")
        # self.build_collision_objects_to_draw()
        # self.enemy_test = Enemy(self, 20,15)
        # self.enemy_test2 = Enemy(self, 2,15)
        # self.enemy_test3 = Enemy(self, 7,10)
        # self.enemy_test4 = Enemy(self, 20,20)
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
            if layer.name =="Background" or layer.name =="Background2":
                for x, y, image in layer.tiles():
                    Ground(self, x , y, image=image)


    def build_collisions(self):
        for layer in self.area.map.tiled_map:
            if layer.name =="Collision":
                for x, y, image in layer.tiles():
                    tile_id = self.area.map.tiled_map.get_tile_gid(x, y, 2)
                    tile_properties = self.area.map.tiled_map.get_tile_properties_by_gid(tile_id)
                    if tile_properties is not None:
                        tile_type = tile_properties['collision']
                        print(f"tile_type: {tile_type} - this can represent type f enemy, npc etc")
                    Block(self, x , y, image=image)


    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(DARK_GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles
        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        self.enemies.draw(self.screen)
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