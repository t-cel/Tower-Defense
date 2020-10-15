import pygame
from renderable import *
from utils import *
import resource_cache

# static 1 image sprite
class StaticSprite(Renderable):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.images = []
        self.current_image = 0
        self.size = (0, 0)
        self.angle = 0

    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.current_image = 0
        if "image_path" in kwargs:
            #  self.images.append(load_image(kwargs.get("image_path"), kwargs.get("alpha")))
            self.images.append(resource_cache.get_resource(
                kwargs.get("image_path"),
                pygame.Surface,
                alpha = kwargs.get("alpha") if "alpha" in kwargs else False,
                clone = kwargs.get("clone") if "clone" in kwargs else False
            ))
        elif "images_paths" in kwargs: # called from DynamicSprite
            # for path in kwargs.get("images_paths"):
            #     self.images.append(load_image(path, kwargs.get("alpha")))
            self.images = resource_cache.get_resource(
                kwargs.get("images_paths"),
                resource_cache.ImagesPack,
                alpha = kwargs.get("alpha") if "alpha" in kwargs else False,
                clone = kwargs.get("clone") if "clone" in kwargs else False
            )

        self.size = kwargs.get("size")
        self.angle = kwargs.get("angle")

        self.set_size(self.size)
        self.set_rotation(self.angle)

    def set_size(self, size):
        self.size = size
        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.scale(
                self.images[i],
                (self.size[0] * self.game_object.size[0],
                 self.size[1] * self.game_object.size[1])
            )

    def set_rotation(self, angle):
        self.angle = angle
        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], self.angle + self.game_object.angle)

    def render(self, screen):
        screen.blit(
            self.images[self.current_image],
            (self.game_object.pos[0] + self.pos[0], self.game_object.pos[1] + self.pos[1])
        )