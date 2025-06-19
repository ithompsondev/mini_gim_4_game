import pygame
from pygame.locals import *
from assets import *
from entity.asset_id import Chem as Chem_ID
from entity.asset_id import FuelSource as FuelSource_ID
from entity.chemical import Chem
from entity.fuel_source import FuelSource
from entity.flame import Flame
from base_game import Game

class AssetLoader(Game):
    def __init__(self):
        super().__init__('asset_loader')
        self.renderable_assets = []
        self.flame_generated = False
        self.flame = None

    def run(self):
        self.running = True
        while self.running:
            self.limit_frames()
            self.compute_dt()
            self.record_time()
            self.show_bg()
            self.process_events()

            for asset in self.renderable_assets:
                asset.update(self.dt)
                asset.render(asset.loc)
                print(self.dt)

            if not self.flame in self.renderable_assets:
                self.flame_generated = False

            pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            self.process_exit_event(event)
            self.process_keydown_events(event)

    def process_keydown_events(self, e_key):
        if e_key.type == KEYDOWN:
            if e_key.key == K_SPACE:
                if not self.flame_generated:
                    self.init_flame()
                    self.flame_generated = True

    def init_flame(self):
        twigs = FuelSource.create_sources(self.window, Chem(Chem_ID.CARBON), FuelSource_ID.TWIG, 5, debug=True)
        flame = Flame(self.window, twigs, debug=True)
        
        self.renderable_assets.append(flame)
        self.flame = flame
        
        print('<< LOADED ASSET >>')
        print(flame)

if __name__ == '__main__':
    game = AssetLoader()
    game.run()