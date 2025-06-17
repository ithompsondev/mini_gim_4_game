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
        self.flame_generated = False
        self.renderable_assets = []

    def run(self):
        flame_loc = self.init_flame()
        self.running = True
        while self.running:
            self.limit_frames()
            self.compute_dt()
            self.record_time()
            self.show_bg()
            self.process_events()

            self.flame.update(self.dt)
            self.flame.render(flame_loc)
            for asset in self.renderable_assets:
                asset.update(self.dt)
                # TODO: Logic to determine the location of renderable assets besides the flame
                asset.render((0, 0))

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
        twigs = []
        for i in range(0, 5):
            twig = FuelSource(self.window, Chem(Chem_ID.CARBON), FuelSource_ID.TWIG, debug=True)
            twigs.append(twig)
            print('<< LOADED ASSET >>')
            print(twig)
        
        self.flame = Flame(self.window, twigs, debug=True)
        print('<< LOADED ASSET >>')
        print(self.flame)

        return ((self.scr_width/2) - (self.flame.width/2), (self.scr_height/2) - (self.flame.height/2)) # TODO: Fix me

if __name__ == '__main__':
    game = AssetLoader()
    game.run()