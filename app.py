import pygame
from pygame.locals import *

pygame.init()

_width = 800
_height = 600

screen = pygame.display.set_mode((_width, _height))

running = True
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pygame.display.flip()
