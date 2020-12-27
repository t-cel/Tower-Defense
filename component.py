

# abstract component class
class Component:

    # invoked only by game_object
    def __init__(self, game_object):
        self.game_object = game_object
        self.enabled = True

    # invoked by user
    def init_component(self, **kwargs):
        pass

    def change_activity(self, enable):
        self.enabled = enable

    def update(self, dt):
        pass

    def process_event(self, event):
        pass