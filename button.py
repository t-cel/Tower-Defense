import pygame_gui
import pygame
from component import *

# wrapper class for pygame_gui button
class Button(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.size = (0, 0)
        self.text = ""
        self.callback = None
        self.button = None

    def init_component(self, **kwargs):
        # args: size, label, gui_manager, callback
        self.size = kwargs.get("size")
        if "text" in kwargs:
            self.text = kwargs.get("text")
        self.callback = kwargs.get("callback")

        if not callable(self.callback):
            raise Exception("Passed callback object is not callable")

        self.button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect(self.game_object.pos, self.size),
            text = self.text,
            manager = kwargs.get("gui_manager"),
            tool_tip_text = kwargs.get("tool_tip_text") if "tool_tip_text" in kwargs else None,
            object_id = kwargs.get("object_id") if "object_id" in kwargs else None
        )

    def change_activity(self, enable):
        super().change_activity(enable)
        if enable:
            self.button.show()
        else:
            self.button.hide()

    def process_event(self, event):
        if event.type == pygame.USEREVENT and \
                event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                event.ui_element == self.button:
            self.callback()