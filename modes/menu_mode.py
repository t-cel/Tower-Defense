from modes.mode import *

import pygame

from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_button import UIButton

from ui.ui import *

from static_sprite import StaticSprite

class MenuMode(Mode):

    def init_gui(self):
        bg_panel = UIPanel(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            starting_layer_height=4,
            manager=ui_manager
        )

        UILabel(
            pygame.Rect(SCREEN_WIDTH / 2 - 300, 100, 600, 100),
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
        register_ui_callback(self.start_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_SELECT_LEVEL))

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

        pygame_gui.elements.ui_image.UIImage(
            relative_rect=pygame.Rect(SCREEN_WIDTH / 2 - 800, SCREEN_HEIGHT / 2 - 240, 720, 480),
            image_surface=resource_cache.get_resource(ENEMIES_PATH + "1/Golem_01_Walking_000.png", resource_cache.SurfaceType, alpha=True),
            manager=ui_manager,
            container=bg_panel
        )

        pygame_gui.elements.ui_image.UIImage(
            relative_rect=pygame.Rect(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2 - 240, 720, 480),
            image_surface=resource_cache.get_resource(ENEMIES_PATH + "2/reversed/Golem_02_Walking_000.png", resource_cache.SurfaceType, alpha=True),
            manager=ui_manager,
            container=bg_panel
        )

    def init_mode(self, **kwargs):
        self.init_gui()

    def deinit_mode(self):
        pass