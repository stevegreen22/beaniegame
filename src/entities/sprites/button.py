import pygame


class Button:
    def __init__(self, x, y, width, height, fg_colour, bg_colour, font, content, content_size):
        self.font = font

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fgColour = fg_colour
        self.bgColour = bg_colour
        self.content = content
        self.content_size = content_size

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bgColour)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fgColour)
        self.text_rect = self.text.get_rect(centerx=self.width//2, centery=self.height//2)
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos) and pressed[0]:
            return True
        return False

