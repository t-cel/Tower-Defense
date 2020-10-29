import pygame
from renderable import *
import file_utils
import resource_cache

# static 1 image sprite
class StaticSprite(Renderable):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.images = []
        self.images_copy = []
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

            #todo: omtimalization: clone it only once
            self.images_copy.append(resource_cache.get_resource(
                kwargs.get("image_path"),
                pygame.Surface,
                alpha = kwargs.get("alpha") if "alpha" in kwargs else False,
                clone = True
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

        #self.images_copy = self.images.copy()

        self.size = kwargs.get("size")
        self.angle = kwargs.get("angle")

        self.set_size(self.size)
        self.set_rotation(self.angle)
        self.set_color(self.color)

    def set_size(self, size):
        self.size = size
        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.scale(
                self.images[i],
                (self.size[0] * self.game_object.size[0],
                 self.size[1] * self.game_object.size[1])
            )
            self.images_copy[i] = pygame.transform.scale(
                self.images_copy[i],
                (self.size[0] * self.game_object.size[0],
                 self.size[1] * self.game_object.size[1])
            )

    def set_color(self, color):
        super().set_color(color)
        for i in range(0, len(self.images)):
            w, h = self.images[i].get_size()
            for x in range(0, w):
                for y in range(0, h):
                    original = self.images_copy[i].get_at((x, y))

                    self.images[i].set_at((x, y), (
                        math_utils.clamp((original[0]/255.0 * self.color[0]/255.0)*255.0, 0, 255),
                        math_utils.clamp((original[1]/255.0 * self.color[1]/255.0)*255.0, 0, 255),
                        math_utils.clamp((original[2]/255.0 * self.color[2]/255.0)*255.0, 0, 255),
                        original[3]
                    ))

    def set_rotation(self, angle):
        self.angle = angle
        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], self.angle + self.game_object.angle)

    def render(self, screen):
        screen.blit(
            self.images[self.current_image],
            (self.game_object.pos[0] + self.pos[0], self.game_object.pos[1] + self.pos[1])
        )