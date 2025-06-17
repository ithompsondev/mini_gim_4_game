import time
import pygame
from pygame.locals import *
from assets import *
from entity.flame import Flame
from entity.fuel_source import FuelSource
from entity.asset_id import FuelSource as FuelSource_ID

pygame.init()

_width = 800
_height = 600

screen = pygame.display.set_mode((_width, _height))

running = True
prev_time = time.time()
dt = 0
elapsed = 0
fps = 20
clock = pygame.time.Clock()

def setup(surf):
    flame = Flame(0.0, 150, 150)
    flame.add_fuel(FuelSource(FuelSource_ID.TWIG))
    flame.add_fuel(FuelSource(FuelSource_ID.TWIG))
    flame.add_fuel(FuelSource(FuelSource_ID.TWIG))
    flame.add_fuel(FuelSource(FuelSource_ID.TWIG))
    flame.add_fuel(FuelSource(FuelSource_ID.TWIG))
   
    flame.set_canvas(surf)
    flame.set_location((_width/2 - 15, _height/2 - 15))

    return flame

flame = setup(screen)

# Game loop from start to finish is considered 1 frame
while running:
    clock.tick(fps) # limit fps, ensure framerate does not exceed fps value    

    curr_time = time.time()
    dt = curr_time - prev_time
    elapsed += dt

    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    if flame.has_fuel():
        flame.update(dt)
        flame.render()

    pygame.display.flip()
