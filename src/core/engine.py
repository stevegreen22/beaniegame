import pygame
from pytmx import pytmx, TiledElement

from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, FPS, GREEN, TILE_SIZE, DARK_GREEN
from src.core.area import Area
from src.entities.player import Player
from src.entities.sprites import Spritesheet, Ground, Block, Enemy, NPC, Trap, Animal

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
        # self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/monster_spritesheet.png')
        self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/orc_right_spritesheet_resize_test.png')
        # self.main_enemy_spritesheet = Spritesheet('assets/characters/enemy/basic_player_clone.png')
        self.main_animal_spritesheet = Spritesheet('assets/animals/animal_spritesheet.png')

    def new(self):
        # new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.traps = pygame.sprite.LayeredUpdates()
        self.animals = pygame.sprite.LayeredUpdates()

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
            if (layer.name =="GroundLayer" or
                    layer.name == "GroundLayerMid" or
                    layer.name == "GroundLayerFore"):
                for x, y, image in layer.tiles():
                    Ground(self, x , y, image=image)

    def build_collisions(self):
        for layer in self.area.map.tiled_map:
            if layer.name =="Collision" or layer.name == "CollisionMid":
                for x, y, image in layer.tiles():
                    tile_id = self.area.map.tiled_map.get_tile_gid(x, y, 3)
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
                        Block(self, x , y, image=image)



    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(DARK_GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles
        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        self.enemies.draw(self.screen)
        self.npcs.draw(self.screen)
        self.traps.draw(self.screen)

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