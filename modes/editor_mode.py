from modes.mode import *

import map
import editor

from ui.ui import *

from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_panel import UIPanel

class EditorMode(Mode):

    @staticmethod
    def init_gui():

        # top panel
        UIPanel(
            pygame.Rect(0, 0, SCREEN_WIDTH, 30),
            starting_layer_height=4,
            manager=ui_manager
        )

        # right panel
        right_panel_w = SCREEN_WIDTH - TILE_SIZE * MAP_W
        right_panel_h = SCREEN_HEIGHT - 30
        right_panel = UIPanel(
            pygame.Rect(TILE_SIZE * MAP_W, 30, right_panel_w, right_panel_h),
            starting_layer_height=4,
            manager=ui_manager
        )

        # back button
        back_btn = UIButton(
            pygame.Rect(20, 200, right_panel_w * 0.8, 40),
            "Back To Menu",
            ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(back_btn, pygame_gui.UI_BUTTON_PRESSED, lambda: print("back"))

        # load button
        load_btn = UIButton(
            pygame.Rect(20, 120, right_panel_w * 0.8, 40),
            "Load",
            ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(
            load_btn,
            pygame_gui.UI_BUTTON_PRESSED,
            lambda: (
                 map.load_map("test.bin"),
                 editor.update_indicators()
            )
        )

        # save button
        save_btn = UIButton(
            pygame.Rect(20, 60, right_panel_w * 0.8, 40),
            "Save",
            ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(
            save_btn,
            pygame_gui.UI_BUTTON_PRESSED,
            lambda: (
                map.save_map("test.bin")
            )
        )

    def init_mode(self):
        EditorMode.init_gui()
        map.create_map()
        editor.init_editor(ui_manager)

        # start path indicators
        for y in range(0, map.MAP_H):
            editor.add_enemy_path_indicator(-1, y, editor.PATH_INDICATOR_DIR_RIGHT)

    def deinit_mode(self):
        pass