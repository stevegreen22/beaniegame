import pygame
import math
from config.config import PLAYER_LAYER, TILE_SIZE, PLAYER_SPEED

# todo: create a list of sprite sheets here with relevant info such as columns and pertinent ids
pygame.mixer.init()
# test_sound = pygame.mixer.Sound("../../../beanie_game/assets/generic/minecraft-villager-289282.mp3")
# test_sound.set_volume(0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self, engine, x, y):
        self.engine = engine
        self._layer = PLAYER_LAYER
        self.groups = self.engine.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

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

        picture = self.engine.main_player_spritesheet.get_sprite(xx, yy, self.width, self.height)

        x_ratio = self.width/16
        y_ratio = self.height/16
        self.image = (pygame.transform.scale(picture,(self.width - x_ratio, self.height - y_ratio)))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.static_down_image = self.engine.main_player_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.static_up_image = self.engine.main_player_spritesheet.get_sprite(0, 32, self.width, self.height)
        self.static_left_image = self.engine.main_player_spritesheet.get_sprite(0, 96, self.width, self.height)
        self.static_right_image = self.engine.main_player_spritesheet.get_sprite(0, 64, self.width, self.height)

        self.down_animations = [self.engine.main_player_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(64, 0, self.width, self.height)
        ]
        self.up_animations = [self.engine.main_player_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(64, 32, self.width, self.height)
                           ]
        self.left_animations = [self.engine.main_player_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(64, 96, self.width, self.height)
                           ]
        self.right_animations = [self.engine.main_player_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.engine.main_player_spritesheet.get_sprite(64, 64, self.width, self.height)
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
        self.collide_enemies()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        from src.core.camera import camera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.engine.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.engine.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.engine.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.engine.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        from src.core.camera import camera
        camera.x = self.x - camera.width / 2 + 16
        camera.y = self.y - camera.height / 2 + 16

    def collide_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.engine.enemies, False)
        # hits = pygame.sprite.spritecollide(self, self.engine.enemies, False, pygame.sprite.collide_mask)
        if hits:
            # removes from allsprites groups
            self.kill()
            # exit the game
            self.engine.playing = False

    def collide_blocks(self, direction):
        if direction == 'x':
            # hits = pygame.sprite.spritecollide(self, self.engine.blocks, False, pygame.sprite.collide_mask)
            hits = pygame.sprite.spritecollide(self, self.engine.blocks, False)
            if hits:
                # pygame.mixer.Sound.play(test_sound)
                # if we're moving right, and colliding, we put the character next to the block we collided with
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.engine.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.engine.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.engine.blocks, False)
            if hits:
                # moving down
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.engine.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.engine.all_sprites:
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