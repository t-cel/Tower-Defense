from component import Component

class AutoDestroy(Component):

    def __init__(self, game_object):
        super().__init__(game_object)
        self.time_to_destroy = 0


    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.time_to_destroy = kwargs.get("time_to_destroy")


    def update(self, dt):
        self.time_to_destroy -= dt
        if self.time_to_destroy <= 0:
            self.game_object.mark_to_destroy = True