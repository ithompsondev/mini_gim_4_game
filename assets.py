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

def get_flame_color_from_chemical(chem):
    for color in FlameColor:
        if color.value[0] == chem:
            return color
    return None

class FuelSource:
    def __init__(self, amount=1.0, burn_rate=1.0, chemical_composition=Chem.CARBON):
        self.amount = amount
        self.burn_rate = burn_rate
        self.comp = chemical_composition

    def burn(self):
        self.amount -= GLOBAL_BURN_AMT * self.burn_rate
    

class Flame:
    def __init__(self, fuel=0.0, color=FlameColor.ORANGE_YELLOW):
        self.fuel = fuel
        self.color = color
        self.sources = []

    def add_fuel(self, fuel_source):
        self.source.push(fuel_source)
        self.fuel += fuel_source.amount

    def update(self):
        recently_burned_source = None
        if self.sources[0].amount <= 0.0:
            recently_burned_source = self.sources.pop(0)

        self.color = get_flame_color_from_chemical(self.sources[0].comp)
        self.sources[0].burn()

    def __str__(self):
        return f'current fuel = {self.fuel}\ncurrent color = {self.color}\nfuel sources = {self.sources}'
