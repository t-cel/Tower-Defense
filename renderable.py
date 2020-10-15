from component import *

# basic class responsible for rendering components
class Renderable(Component):

    def __init__(self, game_object):
        super().__init__(game_object)
        self.pos = (0, 0)
        self.z_pos = 100 # object with lower z pos is rendered first

    def init_component(self, **kwargs):
        self.pos = kwargs.get("pos")
        self.set_pos(self.pos)
        if "z_pos" in kwargs:
            self.z_pos = kwargs.get("z_pos")

    def set_pos(self, pos):
        self.pos = pos

    def render(self, screen):
        pass