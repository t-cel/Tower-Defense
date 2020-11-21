from modes.mode import *
from dynamic_sprite import DynamicSprite
from enemy import Enemy
from circle import Circle
from tower import Tower

import map
import file_utils

from pygame_gui.elements.ui_label import UILabel
from ui.ui import *

class GameMode(Mode):

    @staticmethod
    def spawn_enemy():
        enemy_object = GameObject(
            get_tile_coords(enemies_path_coords[0][0] - 1, enemies_path_coords[0][1]),
            (1, 1),
            0
        )

        rand_enemy = 1 + random.randrange(3)
        enemy_object.add_component(DynamicSprite).init_component(
            pos=(0, -map.TILE_SIZE / 4),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            images_paths=file_utils.get_all_files_in_path(ENEMIES_PATH + str(rand_enemy)),
            alpha=True
        )

        enemy_object.add_component(DynamicSprite).init_component(
            pos=(0, -map.TILE_SIZE / 4),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            images_paths=file_utils.get_all_files_in_path(ENEMIES_PATH + str(rand_enemy) + "/reversed"),
            alpha=True
        )
        enemy_object.get_components(DynamicSprite)[1].change_activity(False)
        enemy_object.add_component(StaticSprite).init_component(
            pos=(250, -20),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            image_path=ENEMIES_PATH + "hp_bar.png",
            z_pos=800,
            alpha=True
        )

        enemy_object.add_component(Enemy).init_component(
            path_coords=enemies_path_coords,
        )

    @staticmethod
    def spawn_tower():
        tower_object = GameObject(
            get_tile_coords(3, 0),
            (1, 1),
            0
        )

        tower_object.add_component(StaticSprite).init_component(
            pos=(0, 0),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            image_path=TOWERS_PATH + '1.png',
            alpha=True
        )

        tower_object.add_component(Circle).init_component(
            pos=(0, 0),
            radius=map.TILE_SIZE * 2,
            color=(25, 25, 225, 200),
            thickness=1
        )

        tower_object.add_component(Tower).init_component(
            enemies_path_coords=enemies_path_coords
        )

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

        # back button
        self.back_btn = UIButton(
            pygame.Rect(20, 260, right_panel_w * 0.8, 40),
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
        register_ui_callback(self.back_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_MENU))

        """
        test_spawn_enemy_btn = GameObject(
            (25, SCREEN_HEIGHT - 100),
            (1, 1),
            0
        )
        test_spawn_enemy_btn.add_component(Button).init_component(
            size=(150, 40),
            text='Spawn Enemy',
            callback=lambda: GameMode.spawn_enemy(),
            gui_manager=ui_manager
        )

        test_spawn_tower_btn = GameObject(
            (25 + 150 + 25, SCREEN_HEIGHT - 100),
            (1, 1),
            0
        )
        test_spawn_tower_btn.add_component(Button).init_component(
            size=(150, 40),
            text='Tower 1',
            callback=lambda: GameMode.spawn_tower(),
            gui_manager=ui_manager,
            # tool_tip_text = "<font face=Montserrat color=#000000 size=2>"
            #                    "<font color=#FFFFFF>Adds tower</font>"
            #                "</font>",
            # object_id = "#test_btn"
        )
        """

    def init_mode(self, **kwargs):
        self.init_gui()
        map.create_map()
        map.load_map(kwargs.get("file_name"))

    def deinit_mode(self):
        pass