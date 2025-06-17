from abc import ABC, abstractmethod
import pygame
import uuid
import json
import os

working_directory = os.getcwd()

# TODO: How do we get the correct path to the assets directory when not at the root
class Asset(ABC):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

    @abstractmethod
    def load():
        pass

    def get_id(self):
        return self.uuid

class RenderableAsset(Asset, ABC):
    def __init__(self, canvas, start_loc=(0,0)):
        super().__init__()
        self.loc = start_loc
        self.canvas = canvas

    def set_loc(self, loc):
        self.loc = loc

    @abstractmethod
    def render(self, loc):
        pass
