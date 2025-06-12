import time
import pygame
from pygame.locals import *

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

    pygame.display.flip()
