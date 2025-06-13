import pygame
from pygame.locals import *
from assets import *
import asset_id
from base_game import Game

class AssetLoader(Game):
    def __init__(self):
        Game.__init__('asset_loader')
        self.flame_generated = False
        self.renderable_assets = []

    def run(self):
        self.running = True
        while self.running:
            self.limit_frames()
            self.compute_dt()
            self.record_time()
            self.show_bg()
            self.process_events()
            
            pygame.display.flip()

    def process_events(self):
        for event in pygame.events.get():
            self.process_exit_event(event)

    def process_keydown_events(self, e_key):
        if e_key.type == KEYDOWN:
            if e_key.key == K_SPACE:
                self.init_flame()

    def init_flame(self):
        twigs = []
        for i in range(0, 5):
            twigs.append(FuelSource(self.window, Chem(asset_id.Chem.CARBON), asset_id.FuelSource.TWIG))
        
        self.renderable_assets.append(Flame(self.window, twigs))