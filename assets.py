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

class RenderableAsset(ABC, Asset):
    def __init__(self, canvas, start_loc=(0,0)):
        super.__init__()
        self.loc = start_loc
        self.canvas = canvas

    @abstractmethod
    def render(self, loc):
        pass

class Chem(Asset):
    def __init__(self, chemical):
        super.__init__()
        
        self.directory = os.path.join(self.assets_dir, 'chemicals', f'ch_{chemical.value}.json')
        self.load()

    def load(self):
        with open(self.directory, 'r') as chem:
            info = json.load(chem)

            self.name = info['name']
            self.symbol = info['symbol']
            self.producing_color = tuple(info['producing_color'])

    def __eq__(self, other):
        return self.name == other.name
    
class FuelSource(RenderableAsset):
    def __init__(self, canvas, chemical, source):
        Asset.__init__()
        RenderableAsset.__init__(canvas)
        
        self.directory = os.path.join(self.assets_dir, 'fuel_sources', f'src_{source.value}.json')
        self.chemical = chemical
        self.has_rendered = False
        self.is_depleted = False
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
    
class Flame(RenderableAsset):
    def __init__(self, canvas, initial_fuel_sources=[]):
        Asset.__init__()
        RenderableAsset.__init__(canvas)
        
        self.directory = os.path.join('flame', 'base_flame.json')
        self.sources = initial_fuel_sources
        
        self.total_fuel = load_initial_fuel_sources(self.sources)
        self.curr_fuel = self.total_fuel
        self.flame_size = self.curr_fuel/self.total_fuel
        self.has_rendered = False
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
