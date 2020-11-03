import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
from map import *

from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_window import UIWindow

from collections.abc import Sequence

ui_manager = UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame_gui.PackageResource(package="sources.themes", resource="ui_theme.json")
)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(ui_manager.get_theme().get_colour('dark_bg'))

# list of 3-element tuples (ui_item, event_id, callback)
ui_callbacks = []

def register_ui_callback(ui_item, event_id, callback):
    ui_callbacks.append((ui_item, event_id, callback))

def unregister_ui_callback(ui_item, event_id):
    for callback in ui_callbacks:
        if callback[0] == ui_item and callback[1] == event_id:
            ui_callbacks.remove(callback)
            return

class MessageBox(UIWindow):
    def __init__(self, rect):
        super().__init__(
            rect,
            ui_manager,
            window_display_title="Message"
        )

        self.text_box = UITextBox(
            "pusto tu",
            pygame.Rect(5, 5, 350, 80),
            ui_manager,
            container=self,
            anchors={
                "left" : "left",
                "right" : "right",
                "top" : "top",
                "bottom" : "top"
            }
        )
        ok_btn = UIButton(
            pygame.Rect(-110, -50, 100, 40),
            "OK",
            ui_manager,
            container=self,
            anchors={
                "left" : "right",
                "right" : "right",
                "top" : "bottom",
                "bottom" : "bottom"
            }
        )
        register_ui_callback(ok_btn, pygame_gui.UI_BUTTON_PRESSED, lambda: self.hide())
        self.set_blocking(True)

    def set_text(self, text):
        self.text_box.html_text = text
        self.text_box.rebuild()

message_box = MessageBox(
    pygame.Rect(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 150, 400, 200),
)
message_box.hide()

def show_message_box(text):
    global message_box

    message_box.set_text(text)
    message_box.show()