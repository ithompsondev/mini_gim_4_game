import time
import json
import pygame
import os
from abc import ABC, abstractmethod
from pygame.locals import *
from assets import *

working_directory = os.getcwd()

class Game(ABC):
    def __init__(self, properties):
        pygame.init()
        self.directory = os.path.join(working_directory, 'game', f'{properties}.json')
        self.running = False
        self.prev_time = time.time()
        self.dt = 0
        self.elapsed = 0
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.load()
    
    def load(self):
        with open(self.directory, 'r') as props:
            info = json.load(props)

            self.scr_width = info['width']
            self.scr_height = info['height']
            self.title = info['title']
            self.bg_color = tuple(info['bg_color'])
            self.window = pygame.display.set_mode(size=(self.scr_width, self.scr_height))
            pygame.display.set_caption(self.title)

    def limit_frames(self):
        self.clock.tick(self.fps)

    def compute_dt(self):
        self.curr_time = time.time()
        self.dt = self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    def record_time(self):
        self.elapsed += self.dt

    def show_bg(self):
        self.window.fill(self.bg_color)

    @abstractmethod   
    def run(self):
        pass

    @abstractmethod
    def process_events(self):
        pass

    def process_exit_event(self, e_exit):
        if e_exit.type == K_QUIT:
            self.running = False

            
