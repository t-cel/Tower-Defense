from component import Component
from map import *
from static_sprite import StaticSprite
import math

class Tile(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.available = False
        self.t = 0.0
        self.counter = 0.0
        self.graphics = game_object.get_components(StaticSprite)[0]

    def init_component(self, **kwargs):
        if "available" in kwargs:
            self.available = kwargs.get("available")

    def update(self, dt):
        self.t += dt
        self.counter += dt
        if self.available and self.counter > 1.0:
            mod = math.sin(self.t) * 0.5 + 1.0
            self.graphics.set_color((
                255 * mod,
                255 * mod,
                255 * mod
            ))
            self.counter = 0.0



