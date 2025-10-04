import pygame
from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DARK_GREEN, TILE_LAYERS, BLACK, BLUE, YELLOW
from src.core.area import Area
from src.entities.player import Player
from src.entities.sprites.button import Button

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
        self.intro_background = pygame.image.load("assets/backgrounds/intro_background.jpg")
        # self.stages = {}
        # self.current_stage = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.current_map = None
        self.player = None
        self.area = None


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
        self.screen.fill("silver")
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles
        self.current_map = self.area.current_map
        # todo: put these into a list and iterate through them
        self.current_map.collision_blocks.draw(self.screen)
        self.current_map.all_sprites.draw(self.screen)
        self.current_map.enemies.draw(self.screen)
        self.current_map.npcs.draw(self.screen)
        self.current_map.traps.draw(self.screen)
        self.current_map.animals.draw(self.screen)
        # player has to come after animated terrain for z level
        self.current_map.animated_terrain.draw(self.screen)  # needs this to animate sand but can then be walked under by player
        self.current_map.player_group.draw(self.screen)

        self.clock.tick(FPS)
        self.fonts("Some text")

        pygame.display.set_caption("Beanie Game: FPS:" + str(self.clock.get_fps()))
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            self.update()
            # self.fonts()
            self.draw()
        self.running = False


    def game_over(self):
        pass


    def intro_screen(self):
        intro_screen = True

        # title = self.font.render("Beanie's Awesome Game", True, DARK_GREEN)
        # title_rect = title.get_rect(x=WINDOW_WIDTH //2, y=WINDOW_HEIGHT // 4)
        font =  download_font = pygame.font.Font("/Users/sgreen/PycharmProjects/BeanieGame/assets/fonts/black-north-font/blacknorth.otf", 32)
        play_button = Button(self.screen.get_width()//2-100, 50, 200, 80, YELLOW, BLUE, font,'Play Game', 32)

        while intro_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro_screen = False
                    self.playing = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro_screen = False

            self.screen.blit(self.intro_background, (0, 0))
            # self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def fonts(self, text):
        system_font = pygame.font.SysFont("monospace", 200)
        download_font = pygame.font.Font("/Users/sgreen/PycharmProjects/BeanieGame/assets/fonts/black-north-font/blacknorth.otf", 20)

        system_font = system_font.render("SystemFont", True, DARK_GREEN)
        download_font = download_font.render(str(text) , True, DARK_GREEN)
        system_font_rect = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        download_font_rect = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        # self.screen.blit(system_font, system_font_rect)
        self.screen.blit(download_font, download_font_rect)