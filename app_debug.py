import pygame
from pygame.locals import *
from assets import *

pygame.init()

_width = 800
_height = 600

screen = pygame.display.set_mode((_width, _height))
pygame.display.set_caption('DEBUG - Ignite, Sustain, Survive')

debug_font_size = 16
debug_font = pygame.font.SysFont('Monaco', debug_font_size)
debug_font_height = debug_font.render('D', False, (0,0,0)).get_height()
debug_surf = pygame.Surface((_width, _height))
debug_scroll_bar = pygame.Surface((30,30))
debug_log = []
def write(surf, font, text, loc=(0,0)):
    surf.blit(font.render(text, False, (255,255,255)), loc)
    

flame = Flame()
debug_head_pos = _height - debug_font_height
is_scrollable = False
debug_surf.fill((125,125,125))
debug_scroll_bar.fill((255,0,0))

running = True
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                debug_log.append('Flame created!')
                debug_log.append(f'{flame}')
        elif event.type == MOUSEWHEEL:
            debug_log.append('Mouse scroll detected')
    
    # iterate from last element in list to -1th element exclusive in increments of 1
    for i in range(len(debug_log)-1, -1, -1):
        write(
            debug_surf, 
            debug_font, 
            debug_log[i], 
            (0, _height - ((i+1)*debug_font_height)) # always drawn from abs left of screen and text appears from the bottom up
        )

    if (len(debug_log)*debug_font_height) > _height:
        debug_surf.blit(debug_scroll_bar, (_width-15,_height-20))
    screen.blit(debug_surf, (0,0))
    pygame.display.flip()
