from enum import Enum

GLOBAL_BURN_AMT = 1.0

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

class Source(Enum):
    TWIG = {'fuel_provided': 10.0, 'burn_rate_multiplier': 0.1, 'chemical_comp': Chem.CARBON}
    LOG = {'fuel_provided': 100.0, 'burn_rate_multiplier': 0.05, 'chemical_comp': Chem.CARBON}

def get_flame_color_from_chemical(chem):
    for color in FlameColor:
        if color.value[0] == chem:
            return color
    return None

# Frame independent burn rate = x/dt where x is some arbitrary measure of what burns for some period of delta time, e.g mass
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
        self.amount = source.value['fuel_provided']
        self.burn_rate_multiplier = source.value['burn_rate_multiplier']
        self.comp = source.value['chemical_comp']

    def burn(self, dt):
        print(f'dt = {dt}')
        print(f'current fuel for this source = {self.amount}')
        print(f'burning {self.burn_rate_multiplier*dt} fuel\n')
        fuel_burned = self.burn_rate_multiplier*dt
        self.amount -= fuel_burned
        return fuel_burned
    

class Flame(Asset):
    def __init__(self, fuel=0.0, color=FlameColor.ORANGE_YELLOW):
        self.fuel = fuel
        self.color = color
        self.sources = []

    def add_fuel(self, fuel_source):
        self.sources.append(fuel_source)
        self.fuel += fuel_source.amount

    def update(self, dt):
        recently_burned_source = None
        if self.sources[0].amount <= 0.0:
            recently_burned_source = self.sources.pop(0)

        if len(self.sources) > 0:
            self.color = get_flame_color_from_chemical(self.sources[0].comp)
            fuel_burned = self.sources[0].burn(dt)
            self.fuel -= fuel_burned
        else:
            self.fuel = 0.0
