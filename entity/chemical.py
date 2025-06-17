from .asset import Asset
import json
import os

class Chem(Asset):
    def __init__(self, chemical, debug=False):
        super().__init__()
        
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