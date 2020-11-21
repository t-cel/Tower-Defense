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
from pygame_gui.core import IncrementalThreadedResourceLoader

#loader = IncrementalThreadedResourceLoader()
ui_manager = UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame_gui.PackageResource(package="sources.themes", resource="ui_theme.json")
)
#ui_manager.set_visual_debug_mode(True)

"""
ui_manager.add_font_paths("Montserrat",
                          "sources/fonts/Montserrat-Regular.ttf",
                          "sources/fonts/Montserrat-Bold.ttf",
                          "sources/fonts/Montserrat-Italic.ttf",
                          "sources/fonts/Montserrat-BoldItalic.ttf")

ui_manager.preload_fonts([{'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'bold_italic'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'bold'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'bold_italic'}
                          ])
loader.start()
finished_loading = False
while not finished_loading:
    finished_loading, progress = loader.update()
"""
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

MESSAGEBOX_TYPE_OK = 0
MESSAGEBOX_TYPE_YES_NO = 1

MESSAGEBOX_RESULT_OK = 0
MESSAGEBOX_RESULT_YES = 1
MESSAGEBOX_RESULT_NO = 2

class MessageBox(UIWindow):
    def __init__(self, rect, text, messagebox_type, result_callback=None):
        super().__init__(
            rect,
            ui_manager,
            window_display_title="Message"
        )

        self.result_callback = result_callback
        self.text_box = UITextBox(
            text,
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

        buttons_right_anchor = {
            "left" : "right",
            "right" : "right",
            "top" : "bottom",
            "bottom" : "bottom"
        }

        if messagebox_type == MESSAGEBOX_TYPE_OK:
            self.ok_btn = UIButton(pygame.Rect(-110, -50, 100, 40), "OK", ui_manager, container=self, anchors=buttons_right_anchor)
            register_ui_callback(self.ok_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: (
                #unregister_ui_callback(self.ok_btn, pygame_gui.UI_BUTTON_PRESSED),
                self.result_callback(MESSAGEBOX_RESULT_OK) if self.result_callback else (),
                self.kill(),
            ))
        else:
            self.yes_btn = UIButton(pygame.Rect(-110, -50, 100, 40), "YES", ui_manager, container=self, anchors=buttons_right_anchor)
            register_ui_callback(self.yes_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: (
                self.result_callback(MESSAGEBOX_RESULT_YES) if self.result_callback else (),
                self.kill(),
            ))

            self.no_btn = UIButton(pygame.Rect(10, -50, 100, 40), "NO", ui_manager, container=self, anchors={
                "left" : "left",
                "right" : "left",
                "top" : "bottom",
                "bottom" : "bottom"
            })
            register_ui_callback(self.no_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: (
                self.result_callback(MESSAGEBOX_RESULT_NO) if self.result_callback else (),
                self.kill(),
            ))

        self.set_blocking(True)


def show_message_box(text, messagebox_type=MESSAGEBOX_TYPE_OK, messagebox_result_callback=None):
    MessageBox(
        pygame.Rect(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 150, 400, 200),
        text,
        messagebox_type,
        messagebox_result_callback
    )