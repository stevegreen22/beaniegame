import pygame
import sys
from core.engine import Engine

pygame.init()
e = Engine("Beanie Game")
e.intro_screen()
e.new()
while e.running:
    e.main()
    e.game_over()

pygame.quit()
sys.exit()



