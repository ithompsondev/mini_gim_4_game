import os
import json
import pygame
from entity.asset import RenderableAsset

class Flame(RenderableAsset):
    def __init__(self, canvas, initial_fuel_sources=[], debug=False):
        super().__init__(canvas)
        
        self.directory = os.path.join(self.assets_dir, 'flame', 'base_flame.json')
        self.sources = initial_fuel_sources
        
        self.total_fuel = Flame.load_initial_fuel_sources(self.sources)
        self.curr_fuel = self.total_fuel
        self.flame_size = self.curr_fuel/self.total_fuel
        self.has_rendered = False
        self.debug = debug
        self.load()
        self.set_loc(((canvas.get_width()/2) - (self.width/2), (canvas.get_height()/2) - (self.height/2)))

    @staticmethod
    def load_initial_fuel_sources(sources):
        total_fuel = 0.0
        for source in sources:
            total_fuel += source.max_fuel
        return total_fuel
    
    def load(self):
        with open(self.directory, 'r') as flame:
            info = json.load(flame)

            self.width = info['width']
            self.height = info['height']

    def add_fuel_source(self, source):
        self.source.append(source)
        if self.curr_fuel + source.fuel >= self.total_fuel:
            self.total_fuel += source.max_fuel
        self.curr_fuel += source.max_fuel

    def has_fuel(self):
        return len(self.sources) > 0

    def update(self, dt):
        if self.has_fuel():
            curr_source = self.sources[0]
            self.curr_color = curr_source.chemical.producing_color
            fuel_burned = curr_source.update(dt)
            self.curr_fuel -= fuel_burned
        
            if curr_source.is_depleted:
                self.sources.pop(0)
            
            self.flame_size = self.curr_fuel/self.total_fuel
            self.set_loc((
                (self.canvas.get_width()/2) - (self.width/2), 
                (self.canvas.get_height()/2) - (self.height/2)
            ))
            print(self.__str__())

    def get_rect(self):
        if self.has_rendered:
            return self.bounding_rect
        else:
            None

    def render(self, loc):
        self.bounding_rect = pygame.Rect(loc, (self.width * self.flame_size, self.height * self.flame_size))
        pygame.draw.rect(
            self.canvas,
            self.curr_color,
            self.bounding_rect
        )
        self.has_rendered = True

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __str__(self):
        if not self.debug:
            return f'Flame is {"burning" if self.has_fuel() else "extinguished"} with fuel level {self.curr_fuel}'
        else:
            return f"""
                [FLAME]
                \tid = {self.uuid}
                \tdir = {self.directory}
                \trendered? = {self.has_rendered}
                \tcurrent source = {self.sources[0]}
                \tcurrent source fuel = {self.sources[0].fuel}
                \ttotal fuel = {self.total_fuel}
                \tcurrent fuel = {self.curr_fuel}
                \tflame size = {self.flame_size}
            """
