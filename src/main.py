import pygame
import sys
from core.engine import Engine

#     def create_tilemap(self):
#         for i, row in enumerate(tilemap):
#             for j, col in enumerate(row):
#                 if col.isdigit():#this somehow needs to be split on spaces or commas
#                     Ground(self, j, i, tile_id=int(col))
#                 else:
#                     Ground(self, j, i, tile_id=354) #basically the floor tile so it's covered in something
#                 # instead need it to pull out 478 as the tile id and then get that image and build the correct blocl
#                 # instead of a if col == x we need a simple function to create and object,
#                 # but we don't know what that object is, unless
#                 # all integers are terrain tiles such as the ground
#                 # all letters are various interactable objects that have collision
#                 if col == 'B':
#                     Block(self, j, i, tile_id=478)
#                 if col == 'P':
#                     Player(self, j, i)


pygame.init()
e = Engine("Beanie Game")
e.intro_screen()
e.new()
while e.running:
    e.main()
    e.game_over()

pygame.quit()
sys.exit()



