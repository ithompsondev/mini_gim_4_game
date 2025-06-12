import time
import pygame
from pygame.locals import *
from assets import *

pygame.init()

_width = 800
_height = 600

screen = pygame.display.set_mode((_width, _height))

running = True
prev_time = time.time()
dt = 0
elapsed = 0
fps = 30
clock = pygame.time.Clock()

def setup(surf):
    flame = Flame()
    flame.add_fuel(FuelSource(Source.TWIG))
    flame.add_fuel(FuelSource(Source.TWIG))
    flame.add_fuel(FuelSource(Source.TWIG))
    flame.add_fuel(FuelSource(Source.TWIG))
    flame.add_fuel(FuelSource(Source.TWIG))
   
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

    flame_size = flame.fuel/100
    pygame.draw.rect(flame.canvas, flame.color.value[1], pygame.Rect(flame.location, (30*flame_size,30*flame_size)))
    
    if len(flame.sources) > 0:
        flame.update(dt)

    pygame.display.flip()
