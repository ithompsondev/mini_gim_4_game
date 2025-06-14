import pygame
from pygame.locals import *
from assets import *
import asset_id
from base_game import Game

class AssetLoader(Game):
    def __init__(self):
        super().__init__('asset_loader')
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
            
            if self.flame_generated:
                flame_index = -1
                for i, asset in enumerate(self.renderable_assets):
                    if asset.uuid == self.flame_id:
                        flame_index = i
                    asset.update()
                    asset.render()

                if not self.renderable_assets[flame_index].has_fuel():
                    self.renderable_assets.pop(flame_index)
                    self.flame_generated = False

            pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            self.process_exit_event(event)

    def process_keydown_events(self, e_key):
        if e_key.type == KEYDOWN:
            if e_key.key == K_SPACE:
                if not self.flame_generated:
                    self.init_flame()
                    self.flame_generated = True

    def init_flame(self):
        twigs = []
        for i in range(0, 5):
            twig = FuelSource(self.window, Chem(asset_id.Chem.CARBON), asset_id.FuelSource.TWIG, debug=True)
            twigs.append(twig)
            print('<< LOADED ASSET >>')
            print(twig)
        
        flame = Flame(self.window, twigs, debug=True)
        print('<< LOADED ASSET >>')
        print(flame)

        self.renderable_assets.append(flame)
        self.flame_id = flame.uuid

if __name__ == '__main__':
    game = AssetLoader()
    game.run()