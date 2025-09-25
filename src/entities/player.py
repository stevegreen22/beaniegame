import pygame
import math
from config.config import PLAYER_LAYER, TILE_SIZE, PLAYER_SPEED
from src.core.area import Area
from src.entities.sprites.sprite_manager import Spritesheet

# todo: create a list of sprite sheets here with relevant info such as columns and pertinent ids
pygame.mixer.init()
# test_sound = pygame.mixer.Sound("../../../beanie_game/assets/generic/minecraft-villager-289282.mp3")
# test_sound.set_volume(0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self, engine, x, y):
        self.engine = engine
        self._layer = PLAYER_LAYER
        self.groups = self.engine.area.current_map.player_group, self.engine.area.current_map.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.main_player_spritesheet = Spritesheet('assets/characters/player/main_character.png')
        # self.main_player_spritesheet = Spritesheet('assets/characters/player/red_main_spritesheet.png')


        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        tileID = 0
        columnCount = 96
        spacing = 0
        margin = 0
        xx = tileID % columnCount # in tiles
        xx = xx * (TILE_SIZE + spacing) + margin #// now in pixels
        yy = math.floor(tileID / columnCount) #// in tiles
        yy = yy * (TILE_SIZE + spacing) + margin #// now in pixels

        picture = self.main_player_spritesheet.get_sprite(xx, yy, self.width, self.height)

        x_ratio = self.width/16
        y_ratio = self.height/16
        self.image = (pygame.transform.scale(picture,(self.width - x_ratio, self.height - y_ratio)))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.static_down_image = self.main_player_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.static_up_image = self.main_player_spritesheet.get_sprite(0, 32, self.width, self.height)
        self.static_left_image = self.main_player_spritesheet.get_sprite(0, 96, self.width, self.height)
        self.static_right_image = self.main_player_spritesheet.get_sprite(0, 64, self.width, self.height)

        self.down_animations = [self.main_player_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(64, 0, self.width, self.height)
        ]
        self.up_animations = [self.main_player_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(64, 32, self.width, self.height)
                           ]
        self.left_animations = [self.main_player_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(64, 96, self.width, self.height)
                           ]
        self.right_animations = [self.main_player_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.main_player_spritesheet.get_sprite(64, 64, self.width, self.height)
                           ]

        # self.mask = None

    # def draw(self):
    #     # bounding box to visualise the collisions
    #     pygame.draw.rect(self.engine.screen, pygame.Color('red'), (self.rect.x, self.rect.y, self.width, self.height), 1)
    #
    #     # create a mask around the image and draw it
    #     self.mask = pygame.mask.from_surface(self.image)
    #     mask_outline = self.mask.outline()
    #     pygame.draw.lines(self.image, "blue", True, mask_outline, 5)


    def update(self):
        self.movement()
        self.animate()
        self.collide_teleports()
        self.collide_enemies()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


    # def fonts(self):
    #     system_font = pygame.font.SysFont("monospace", 200)
    #     download_font = pygame.font.Font("/Users/sgreen/PycharmProjects/BeanieGame/assets/fonts/black-north-font/blacknorth.otf", 20)
    #
    #     system_font = system_font.render("SystemFont", True, "black")
    #     download_font = download_font.render(str(self.x) , True, "black")
    #     system_font_rect = (200, 200)
    #     download_font_rect = (200, 200)
    #     # self.screen.blit(system_font, system_font_rect)
    #     self.engine.screen.blit(download_font, download_font_rect)

    def movement(self):
        from src.core.camera import camera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for sprite in self.engine.area.current_map.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for sprite in self.engine.area.current_map.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for sprite in self.engine.area.current_map.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for sprite in self.engine.area.current_map.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        from src.core.camera import camera
        camera.x = self.x - camera.width / 2 + 16
        camera.y = self.y - camera.height / 2 + 16

    def collide_teleports(self):
        hits = pygame.sprite.spritecollide(self, self.engine.area.current_map.teleporters, False)
        if hits:
            # if we walk into a door, get the door details of where it leads and create that map
            door = self.engine.area.current_map.teleporters._spritelist[0]
            door_properties = door.properties
            print(f"Door {door_properties}")

            #we have the player hitting the teleporter so we now need to move to the new map and update the player location
            self.engine.area.load_new_map(door_properties)
            self.rect.x = door.x #320#door_properties['player_spawn'][0] update to give props x and y
            self.rect.y = door.y #320#door_properties['player_spawn'][1]
            self.update_player_sprite_groups()

    def update_player_sprite_groups(self):
        self.engine.area.current_map.all_sprites.add(self)
        self.engine.area.current_map.player_group.add(self)

    def collide_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.engine.area.current_map.enemies, False)
        # hits = pygame.sprite.spritecollide(self, self.engine.enemies, False, pygame.sprite.collide_mask)
        if hits:
            # removes from allsprites groups and exits games
            self.kill()
            self.engine.playing = False

    def collide_blocks(self, direction):
        if direction == 'x':
            # hits = pygame.sprite.spritecollide(self, self.engine.blocks, False, pygame.sprite.collide_mask)
            hits = pygame.sprite.spritecollide(self, self.engine.area.current_map.collision_blocks, False)
            if hits:
                # pygame.mixer.Sound.play(test_sound)
                # if we're moving right, and colliding, we put the character next to the block we collided with
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.engine.area.current_map.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.engine.area.current_map.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.engine.area.current_map.collision_blocks, False)
            if hits:
                # moving down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.engine.area.current_map.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.engine.area.current_map.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.static_down_image
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.static_up_image
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.static_left_image
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.static_right_image
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1 #every ten frames we change image
                if self.animation_loop >= 3:
                    self.animation_loop = 1