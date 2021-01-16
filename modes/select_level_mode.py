from modes.mode import *

import pygame

from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_button import UIButton

from ui.ui import *
from ui.save_load_window import SaveLoadWindow

class SelectLevelMode(Mode):

    def init_gui(self):
        bg_panel = UIPanel(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            starting_layer_height=4,
            manager=ui_manager
        )

        UILabel(
            pygame.Rect(SCREEN_WIDTH / 2 - 300, 10, 600, 100),
            "Select Level",
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

        LEVEL_BUTTON_SIZE = 125
        MARGIN = 15

        for y in range(0, 4):
            for x in range(0, 6):
                level_btn = UIButton(
                    pygame.Rect(
                        SCREEN_WIDTH / 2 - (3 * LEVEL_BUTTON_SIZE + 2 * MARGIN + MARGIN / 2) + x * (LEVEL_BUTTON_SIZE + MARGIN),
                        SCREEN_HEIGHT / 2 - (2 * LEVEL_BUTTON_SIZE + MARGIN + MARGIN / 2) + y * (LEVEL_BUTTON_SIZE + MARGIN),
                        LEVEL_BUTTON_SIZE, LEVEL_BUTTON_SIZE
                    ),
                    str(1 + x + y * 6),
                    ui_manager,
                    container=bg_panel,
                    anchors={
                        "left": "left",
                        "right": "right",
                        "top": "top",
                        "bottom": "bottom"
                    }
                )
                #register_ui_callback(self.start_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_GAME))

        back_btn = UIButton(
            pygame.Rect(40, -80, 200, 60),
            "Back",
            ui_manager,
            container=bg_panel,
            anchors={
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom"
            }
        )
        register_ui_callback(back_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_MENU))

        select_custom_btn = UIButton(
            pygame.Rect(-240, -80, 200, 60),
            "Select Custom",
            ui_manager,
            container=bg_panel,
            anchors={
                "left": "right",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom"
            }
        )
        register_ui_callback(select_custom_btn, pygame_gui.UI_BUTTON_PRESSED,
            lambda e: SaveLoadWindow(
                "maps",
                "Select Map",
                lambda f: switch_mode(MODE_GAME, file_name=f),
                False
            )
        )


    def init_mode(self, **kwargs):
        self.init_gui()


    def deinit_mode(self):
        pass