class FuelSource(RenderableAsset):
    def __init__(self, canvas, chemical, source, debug=False):
        super().__init__(canvas)
        
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
        self.is_depleted = self.fuel <= 0.0
        
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
