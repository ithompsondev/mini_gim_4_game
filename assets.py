from enum import Enum
import pygame

class Chem(Enum):
    CARBON = 'C'
    LITHIUM = 'Li+'
    SODIUM = 'Na+'
    POTASSIUM = 'K+'
    RUBIDIUM = 'Rb+'
    CESIUM = 'Cs+'
    CALCIUM = 'Ca2+'
    STRONTIUM = 'Sr2+'
    BARIUM = 'Ba2+'
    COPPER = 'Cu2+'
    IRON = 'Fe2+'

FC_CHEM = 0
FC_COL = 1
class FlameColor(Enum):
    CRIMSON = (Chem.LITHIUM, (244,66,66))
    YELLOW = (Chem.SODIUM, (255,242,0))
    LILAC = (Chem.POTASSIUM, (194,123,160))
    PINK = (Chem.RUBIDIUM, (246, 84, 16))
    VIOLET = (Chem.CESIUM, (179, 158, 181))
    ORANGE_RED = (Chem.CALCIUM, (255, 94, 0))
    RED_RED = (Chem.STRONTIUM, (255, 36, 0))
    YELLOW_GREEN = (Chem.BARIUM, (181, 230, 29))
    TURQUOISE = (Chem.COPPER, (0, 217, 192))
    GOLD_YELLOW = (Chem.IRON, (255, 195, 0))
    ORANGE_YELLOW = (Chem.CARBON, (255, 165, 0))

SRC_AMT = 'fuel_provided'
SRC_RATE = 'burn_rate_multiplier'
SRC_CHEM = 'chemical_comp'
class Source(Enum):
    TWIG = {'fuel_provided': 10.0, 'burn_rate_multiplier': 0.1, 'chemical_comp': Chem.CARBON}
    LOG = {'fuel_provided': 100.0, 'burn_rate_multiplier': 0.05, 'chemical_comp': Chem.CARBON}

def get_flame_color_from_chemical(chem):
    for color in FlameColor:
        if color.value[0] == chem:
            return color.value[FC_COL]
    return None

# Frame independent burn rate = x*dt where x is some arbitrary measure of what burns for some period of delta time, e.g mass
class Asset:
    def __init__(self):
        self.surface = None
        self.location = (0,0)
    
    def set_canvas(self, canvas):
        self.canvas = canvas

    def set_location(self, loc):
        self.location = loc

class FuelSource(Asset):
    def __init__(self, source):
        self.name = source.name.lower()
        self.amount = source.value[SRC_AMT]
        self.burn_rate_multiplier = source.value[SRC_RATE]
        self.comp = source.value[SRC_CHEM]

    def burn(self, dt):
        fuel_burned = self.burn_rate_multiplier*dt
        self.amount -= fuel_burned
        return fuel_burned
    

class Flame(Asset):
    def __init__(self, fuel, width, height):
        self.fuel = fuel
        self.color = None
        self.sources = []
        self.size = 0
        self.width = width
        self.height = height

    def add_fuel(self, fuel_source):
        self.sources.append(fuel_source)
        self.fuel += fuel_source.amount
    
    def has_fuel(self):
        return len(self.sources) > 0

    def get_color(self):
        return get_flame_color_from_chemical(self.sources[0].comp)

    def render(self):
        if self.has_fuel():
            pygame.draw.rect(self.canvas, self.get_color(), pygame.Rect(self.location, (self.width*self.size, self.height*self.size)))

    def update(self, dt):
        recently_burned_source = None
        self.size = self.fuel/100.00
        if self.sources[0].amount <= 0.0:
            recently_burned_source = self.sources.pop(0)

        if self.has_fuel():
            self.color = self.get_color()
            fuel_burned = self.sources[0].burn(dt)
            self.fuel -= fuel_burned
        else:
            self.fuel = 0.0
