from modes.mode import *
import enemy
import map
import editor

from ui.ui import *

from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.windows import UIFileDialog

from ui.save_load_window import SaveLoadWindow
from ui.map_settings_window import MapSettingsWindow

class EditorMode(Mode):

    def init_gui(self):

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

        # load button
        self.load_btn = UIButton(
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
        register_ui_callback(self.load_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.open_file_dialog(False))

        # save button
        self.save_btn = UIButton(
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
        register_ui_callback(self.save_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.open_file_dialog())

        # settings button
        self.settings_btn = UIButton(
            pygame.Rect(20, 180, right_panel_w * 0.8, 40),
            "Settings",
            ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(self.settings_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: print("settings"))

        # clear button
        self.clear_btn = UIButton(
            pygame.Rect(20, 260, right_panel_w * 0.8, 40),
            "Clear",
            ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(self.clear_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_clear_btn_click())

        # back button
        self.back_btn = UIButton(
            pygame.Rect(20, 320, right_panel_w * 0.8, 40),
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
        register_ui_callback(self.back_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_back_to_menu_btn_click())

        self.settings_window = MapSettingsWindow()

    def open_file_dialog(self, save=True):
        self.file_dialog = SaveLoadWindow(
            pygame.Rect(SCREEN_WIDTH / 2 - 440 / 2, SCREEN_HEIGHT / 2 - 500 / 2, 440, 500),
            "maps",
            "Save Map" if save else "Load Map",
            lambda f: self.on_save_confirm_btn_click(f) if save else self.on_load_confirm_btn_click(f),
            save
        )

    def on_save_confirm_btn_click(self, f):
        splitted = f.split('.')
        if len(splitted) > 2:
            show_message_box("<b><font face='verdana' color='#FF3333' size=3.5>"
                             "Invalid file name"
                             "</font></b>")
            return

        save_map(splitted[0] + MAPS_EXTENSION)

    def on_load_confirm_btn_click(self, f):
        load_map(f)
        editor.update_indicators()

    def on_clear_btn_click(self):
        if len(map_settings.settings.enemies_path_coords) == 0:
            return

        show_message_box(
            "Do you really want to clear this map?",
            MESSAGEBOX_TYPE_YES_NO,
            lambda result: (clear_map(), editor.update_indicators()) if result == MESSAGEBOX_RESULT_YES else ()
        )

    def on_back_to_menu_btn_click(self):
        show_message_box(
            "Do you really want to exit editor?",
            MESSAGEBOX_TYPE_YES_NO,
            lambda result: switch_mode(MODE_MENU) if result == MESSAGEBOX_RESULT_YES else ()
        )

    def init_mode(self, **kwargs):
        self.init_gui()
        map.create_map()
        editor.init_editor(ui_manager)

    def deinit_mode(self):
        clear_map()