from component import Component
from map import *

from circle import Circle

import enemy

import math_utils
import math

class Arrow(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.speed = 1.0
        self.start_pos = game_object.pos
        self.dir = (0, 0)
        self.damages = 15
        self.target_pos = (0, 0)
        self.hit_ground = False
        self.falling = False
        self.t = 0.0

        self.last_pos = (0, 0)

    def init_component(self, **kwargs):
        self.target_pos = kwargs.get("target_pos")
        self.dir = math_utils.normalize(
            (self.target_pos[0] - self.game_object.pos[0],
             self.target_pos[1] - self.game_object.pos[1])
        )
        # print("dir: " + str(self.dir))
        # print("sqr mag: " + str(math_utils.sqr_magnitude((0, 0), self.dir)))
        angle = -math.atan2(self.dir[1], self.dir[0]) * 57.2957795 + 180
        self.game_object.set_rotation(angle)

        self.speed = kwargs.get("speed")
        self.damages = kwargs.get("damages")

        # tests
        """
        self.game_object.add_component(Circle).init_component(
            pos=(0, 0),
            radius=5,
            color=(25, 25, 225, 200),
            thickness=1
        )
        """


    def update(self, dt):
        #print("delta time: " + str(dt))

        if not self.hit_ground:
            for e in enemy.enemies:
                if math_utils.sqr_magnitude(self.game_object.pos, e.get_target_pos()) <= 200:
                    e.take_damage(self.damages)
                    self.game_object.mark_to_destroy = True
                    return

            self.game_object.set_pos((
                self.game_object.pos[0] + self.dir[0] * self.speed * dt * 100,
                self.game_object.pos[1] + self.dir[1] * self.speed * dt * 100
            ))


                    # print("speed of arrow: " + str(self.speed * dt))

        if self.falling:
            if math_utils.sqr_magnitude(self.game_object.pos, self.target_pos) > 300:
                self.hit_ground = True
        else:
            if math_utils.sqr_magnitude(self.game_object.pos, self.target_pos) < 100:
                self.falling = True

        self.t += dt
        if self.t > 5.0:
            self.game_object.mark_to_destroy = True

        # print("sqr mag: " + str(math_utils.sqr_magnitude(self.game_object.pos, self.last_pos)))
        self.last_pos = self.game_object.pos