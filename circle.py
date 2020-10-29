from renderable import *
from map import *
import pygame

class Circle(Renderable):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.radius = 5
        self.thickness = 1

    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.radius = kwargs.get("radius")
        self.thickness = kwargs.get("thickness")

    def render(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos[0] + self.game_object.pos[0] + TILE_SIZE / 2),
             int(self.pos[1] + self.game_object.pos[1] + TILE_SIZE / 2)
             ),
            self.radius,
            self.thickness
        )