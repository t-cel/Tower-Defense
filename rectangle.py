from renderable import Renderable
import map
import pygame

class Rectangle(Renderable):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.w = 5
        self.h = 5
        self.thickness = 1
        self.surface = None

    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.w = kwargs.get("w")
        self.h = kwargs.get("h")
        self.thickness = kwargs.get("thickness")

    def render(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.pos[0] + self.game_object.pos[0], self.pos[1] + self.game_object.pos[1], self.w, self.h),
            self.thickness
        )