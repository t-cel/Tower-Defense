from renderable import *
from map import *
import pygame

class Circle(Renderable):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.radius = 5
        self.thickness = 1
        self.surface = None

    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.radius = kwargs.get("radius")
        self.thickness = kwargs.get("thickness")

        #self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        #self.surface.set_colorkey((0, 0, 0))
        #self.surface.set_alpha(128)

    def render(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos[0] + self.game_object.pos[0] + TILE_SIZE / 2),
             int(self.pos[1] + self.game_object.pos[1] + TILE_SIZE / 2)
             ),
            int(self.radius),
            self.thickness
        )

        #screen.blit(
        #    self.surface,
        #    (self.game_object.pos[0] + self.pos[0], self.game_object.pos[1] + self.pos[1])
        #)