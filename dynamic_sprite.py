from static_sprite import *

# sprite consisted from > 1 images
class DynamicSprite(StaticSprite):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.timer = 0.0
        self.max_time = 0.02

    def init_component(self, **kwargs):
        super().init_component(**kwargs)

    def update(self, dt):
        # print(self.timer)
        self.timer += dt
        if self.timer >= self.max_time:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.timer = 0.0