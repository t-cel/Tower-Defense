from static_sprite import *

game_objects = []

# Basic game object, container for components and sprites.
class GameObject:
    def __init__(self, pos, size, angle, name=""):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.name = name

        self.components = []

        self.mark_to_destroy = False
        game_objects.append(self)

    def set_size(self, size):
        self.size = size
        for sprite in self.get_components(StaticSprite):
            sprite.set_size(sprite.size)

    def set_pos(self, pos):
        self.pos = pos

    def set_rotation(self, angle):
        self.angle = angle
        for sprite in self.get_components(StaticSprite):
            sprite.set_rotation(sprite.angle)

    def destroy(self):
        for component in self.components:
            component.change_activity(False)
        self.components = []

    def add_component(self, component_type):
        if issubclass(component_type, Component):
            component = component_type(self)
            self.components.append(component)
            return component
        else:
            raise Exception("Tried to add object to components that doesn't inherit Component class")

    def get_components(self, component_type):
        target_components = []
        for component in self.components:
            if issubclass(type(component), component_type) or isinstance(component, component_type):
                target_components.append(component)
        return target_components
