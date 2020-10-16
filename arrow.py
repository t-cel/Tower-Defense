from component import Component
from utils import *
from map import *

class Arrow(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.target_enemy = None
        self.t = 0.0
        self.speed = 4.0
        self.start_pos = game_object.pos
        self.dir = (0, 0)

    def get_target_pos(self):
        return self.target_enemy.game_object.pos[0] + TILE_SIZE / 4, \
               self.target_enemy.game_object.pos[1] + TILE_SIZE / 4

    def init_component(self, **kwargs):
        self.target_enemy = kwargs.get("target_enemy")
        target_pos = self.get_target_pos()
        self.dir = normalize(
            (target_pos[0] - self.game_object.pos[0],
             target_pos[1] - self.game_object.pos[1])
        )
        angle = -math.atan2(self.dir[1], self.dir[0]) * 57.2957795 + 180
        self.game_object.set_rotation(angle)

    def update(self, dt):
        self.t += dt * self.speed

        if sqr_magnitude(self.game_object.pos, self.get_target_pos()) <= 200:
            self.target_enemy.take_damage(15)
            self.game_object.destroy = True
        else:

            self.game_object.set_pos((self.game_object.pos[0] + self.dir[0] * self.speed, self.game_object.pos[1] + self.dir[1] * self.speed))

            """
            self.game_object.set_pos(lerp(
                self.start_pos,
                self.get_target_pos(),
                self.t
            ))
            """
