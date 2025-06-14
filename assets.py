from abc import ABC, abstractmethod
import pygame
import uuid
import json
import os

working_directory = os.getcwd()

class Asset(ABC):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.assets_dir = os.path.join(working_directory, 'assets')

    @abstractmethod
    def load():
        pass

    def get_id(self):
        return self.uuid

class RenderableAsset(Asset, ABC):
    def __init__(self, canvas, start_loc=(0,0)):
        super.__init__()
        self.loc = start_loc
        self.canvas = canvas

    @abstractmethod
    def render(self, loc):
        pass

class Chem(Asset):
    def __init__(self, chemical, debug=False):
        super.__init__()
        
        self.directory = os.path.join(self.assets_dir, 'chemicals', f'ch_{chemical.value}.json')
        self.debug = debug
        self.load()

    def load(self):
        with open(self.directory, 'r') as chem:
            info = json.load(chem)

            self.name = info['name']
            self.symbol = info['symbol']
            self.producing_color = tuple(info['producing_color'])

    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        if not self.debug:
            return f'{self.name} ({self.symbol}) produces a {self.producing_color} colored flame'
        else:
            return f"""
                [CHEMICAL]
                \tid = {self.uuid}
                \tdir = {self.directory}
                \tname = {self.name}
                \tsymbol = {self.symbol}
                \tproducing color = {self.producing_color}


            """
    
class FuelSource(RenderableAsset):
    def __init__(self, canvas, chemical, source, debug=False):
        Asset.__init__()
        RenderableAsset.__init__(canvas)
        
        self.directory = os.path.join(self.assets_dir, 'fuel_sources', f'src_{source.value}.json')
        self.chemical = chemical
        self.has_rendered = False
        self.is_depleted = False
        self.debug = debug
        self.load()

    def load(self):
        with open(self.directory, 'r') as src:
            info = json.load(src)

            self.name = info['name']
            self.max_fuel = info['max_fuel']
            self.fuel = self.max_fuel
            self.burn_rate_multiplier = info['burn_rate_multiplier']
            self.primary_color = tuple(info['primary_color'])
            self.width = info['width']
            self.height = info['height']

    def update(self, dt):
        fuel_burned = self.fuel - self.burn_rate_multiplier * dt
        self.fuel -= fuel_burned
        self.is_depleted = self.fuel > 0
        
        return fuel_burned

    def get_rect(self):
        if self.has_rendered:
            return self.bounding_rect
        else:
            None

    def render(self, loc):
        self.bounding_rect = pygame.Rect(loc, (self.width, self.height))
        pygame.draw.rect(
            self.canvas,
            self.primary_color,
            self.bounding_rect
        )

    def __eq__(self, other):
        return self.name == other.name and self.chemical.eq(other.chemical)
    
    def __str__(self):
        if not self.debug:
            return f'The fuel source: {self.name} has a max fuel potential of {self.max_fuel} with a burn rate of {self.burn_rate_multiplier}'
        else:
            return f"""
                [Fuel Source]
                \tid = {self.uuid}
                \tdir = {self.directory}
                \trendered? = {self.has_rendered}
                \tdepleted? = {self.is_depleted}
                \tname = {self.name}
                \tmax fuel = {self.max_fuel}
                \tcurrent fuel = {self.fuel}
                \tburn rate = {self.burn_rate_multiplier}
                \tprimary color = {self.primary_color}
                \tself.dimensions = ({self.width}, {self.height})
                {self.chemical.__str__()}
            """
    
class Flame(RenderableAsset):
    def __init__(self, canvas, initial_fuel_sources=[], debug=False):
        Asset.__init__()
        RenderableAsset.__init__(canvas)
        
        self.directory = os.path.join('flame', 'base_flame.json')
        self.sources = initial_fuel_sources
        
        self.total_fuel = load_initial_fuel_sources(self.sources)
        self.curr_fuel = self.total_fuel
        self.flame_size = self.curr_fuel/self.total_fuel
        self.has_rendered = False
        self.debug = debug
        self.load()

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
        
            if curr_source.is_depleted():
                self.total_fuel -= curr_source.max_fuel
                self.sources.pop(0)
            
            self.flame_size = self.curr_fuel/self.total_fuel
            print(self.__str__())

    def get_rect(self):
        if self.has_rendered():
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

    def __str__(self):
        if not self.debug:
            return f'Flame is {"burning" if self.has_fuel() else "extinguished"} with fuel level {self.curr_fuel}'
        else:
            return f"""
                [FLAME]
                \tid = {self.uuid}
                \tdir = {self.directory}
                \trendered? = {self.has_rendered}
                \tsources = {map(lambda src: src.name, self.sources)}
                \ttotal fuel = {self.total_fuel}
                \tcurrent fuel = {self.curr_fuel}
                \tflame size = {self.flame_size}
            """