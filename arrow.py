from component import Component
from map import *

import enemy

import math_utils
import math

class Arrow(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.t = 0.0
        self.speed = 4.0
        self.start_pos = game_object.pos
        self.dir = (0, 0)

    def get_target_pos(self, e):
        return e.game_object.pos[0] + TILE_SIZE / 4, \
               e.game_object.pos[1]

    def init_component(self, **kwargs):
        target_pos = self.get_target_pos(kwargs.get("target_enemy"))
        self.dir = math_utils.normalize(
            (target_pos[0] - self.game_object.pos[0],
             target_pos[1] - self.game_object.pos[1])
        )
        angle = -math.atan2(self.dir[1], self.dir[0]) * 57.2957795 + 180
        self.game_object.set_rotation(angle)

    def update(self, dt):
        self.t += dt * self.speed

        for e in enemy.enemies:
            if math_utils.sqr_magnitude(self.game_object.pos, self.get_target_pos(e)) <= 200:
                e.take_damage(15)
                self.game_object.mark_to_destroy = True
                return
            else:
                self.game_object.set_pos((
                    self.game_object.pos[0] + self.dir[0] * self.speed,
                    self.game_object.pos[1] + self.dir[1] * self.speed
                ))

