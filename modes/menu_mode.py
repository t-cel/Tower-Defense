from modes.mode import *

import pygame

from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_button import UIButton

from ui.ui import *

class MenuMode(Mode):

    def init_gui(self):
        bg_panel = UIPanel(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            starting_layer_height=4,
            manager=ui_manager
        )

        UILabel(
            pygame.Rect(SCREEN_WIDTH / 2 - 100, 100, 200, 40),
            "Tower Defender",
            ui_manager,
            container=bg_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            },
            object_id="#title_label"
        )

        self.start_btn = UIButton(
            pygame.Rect(SCREEN_WIDTH / 2 - 100, 260, 200, 40),
            "Start",
            ui_manager,
            container=bg_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(self.start_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_GAME))

        self.editor_btn = UIButton(
            pygame.Rect(SCREEN_WIDTH / 2 - 100, 320, 200, 40),
            "Editor",
            ui_manager,
            container=bg_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(self.editor_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_EDITOR))

    def init_mode(self):
        self.init_gui()

    def deinit_mode(self):
        pass