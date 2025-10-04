import pygame
from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DARK_GREEN, TILE_LAYERS, BLACK, BLUE, YELLOW, WHITE
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
        self.game_over_background = pygame.image.load("assets/backgrounds/game_over_background.jpg")

        self.fonts = {
            "monospace": pygame.font.SysFont("monospace", 32),
            "black_north": pygame.font.Font("assets/fonts/black-north-font/blacknorth.otf", 32)
        }

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
        # todo: fix enemies walking behind trees.
        for sprite in self.current_map.all_sprite_list:
            sprite.draw(self.screen)

        self.clock.tick(FPS)
        # interestingly enough, this could be used to draw the inventory as it moves with the player.
        self.draw_font(self.fonts["black_north"],"x")

        pygame.display.set_caption("Beanie Game: FPS:" + str(self.clock.get_fps()))
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        # self.running = False


    # todo: font or text drawn when not relative to the player isn't showing on screen...but buttons are...
    # make a text container class?
    def game_over(self):
        font = self.fonts["black_north"]
        text_content = "Game Over"
        text = font.render(text_content, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        # self.draw_font(font, text_content)

        button_content = "Restart Game"
        restart_button = Button(self.screen.get_width() // 2 - 100, 250, 200, 80,
                                YELLOW, BLUE, font, button_content, 32)

        for sprite in self.current_map.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(text, text_rect)
            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self):
        intro_screen = True
        # title = self.font.render("Beanie's Awesome Game", True, DARK_GREEN)
        # title_rect = title.get_rect(x=WINDOW_WIDTH //2, y=WINDOW_HEIGHT // 4)
        font = self.fonts["black_north"]
        button_content = 'Play Game'
        play_button = Button(self.screen.get_width()//2-100, 50, 200, 80, YELLOW, BLUE, font, button_content, 32)

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


    # todo: refactor this out of here to somewhere more meaningful
    def draw_font(self, font, text):
        rendered_font = font.render(str(text) , True, DARK_GREEN)
        rendered_font_rect = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.screen.blit(rendered_font, rendered_font_rect)