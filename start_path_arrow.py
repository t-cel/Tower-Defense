from component import Component
from math import sin
from map import *
import random

class StartPathArrpw(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.start_y = game_object.pos[1]
        self.t = random.randrange(4.0)

    def update(self, dt):
        self.t += dt * 3.0
        self.game_object.set_pos((
            self.game_object.pos[0],
            self.start_y + (sin(self.t) * (TILE_SIZE / 20))
        ))
