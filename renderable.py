from component import *
import math_utils

class Renderable(Component):
    """
        Basic class responsible for rendering components
    """

    def __init__(self, game_object):
        super().__init__(game_object)
        self.pos = (0, 0)
        self.z_pos = 100 # object with lower z pos is rendered first

        self.color = (0, 0, 0, 0)
        self.set_color((255, 255, 255, 255))


    def init_component(self, **kwargs):
        self.pos = kwargs.get("pos")
        self.set_pos(self.pos)

        if "z_pos" in kwargs:
            self.z_pos = kwargs.get("z_pos")

        if "color" in kwargs:
            self.set_color(kwargs.get("color"))


    def set_pos(self, pos):
        self.pos = pos


    def get_pos(self):
        return self.pos


    def set_color(self, color):
        self.color = color
        self.color = (
            math_utils.clamp(self.color[0], 0, 255),
            math_utils.clamp(self.color[1], 0, 255),
            math_utils.clamp(self.color[2], 0, 255),
            math_utils.clamp(self.color[3], 0, 255),
        )


    def get_color(self):
        return self.color


    def render(self, screen):
        pass