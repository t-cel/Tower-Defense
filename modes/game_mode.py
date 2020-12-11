from modes.mode import *
from dynamic_sprite import DynamicSprite
from enemy import Enemy
from circle import Circle
from tower import Tower
from enemies_spawner import EnemiesSpawner

import map
import file_utils

import tower

from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer
from pygame_gui.elements.ui_image import UIImage
from ui.ui import *

class GameMode(Mode):

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
            enemies_path_coords=map_settings.settings.enemies_path_coords
        )

    def start_fall(self):
        self.enemies_spawner.start_spawn()

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

        fall_info_panel = UIPanel(
            relative_rect=pygame.Rect(0, 0, right_panel_w - 5, 120),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "top"
            }
        )

        self.fall_label = UITextBox(
            "<b>Fall:</b> 0 / 10",
            pygame.Rect(5, 5, 300, 35),
            ui_manager,
            container=fall_info_panel,
            object_id="#no_border_textbox",
        )

        self.fall_reward_label = UITextBox(
            "<b>Reward:</b> 1000 gold coins",
            pygame.Rect(5, 75, 400, 35),
            ui_manager,
            container=fall_info_panel,
            object_id="#no_border_textbox",
        )

        # build panel
        build_panel = UIPanel(
            relative_rect=pygame.Rect(0, 120, right_panel_w - 5, 600),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )

        UITextBox(
            "<b>Towers</b>",
            pygame.Rect(5, 5, 300, 35),
            ui_manager,
            container=build_panel,
            object_id="#no_border_textbox",
        )

        self.towers_view_panel = UIPanel(
            relative_rect=pygame.Rect(5, 40, right_panel_w - 20, 540),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=build_panel
        )

        self.towers_container = UIScrollingContainer(
            pygame.Rect(0, 0, right_panel_w - 30, 540),
            ui_manager,
            container=self.towers_view_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            },
            object_id="#enemy_scrolling_container",
            starting_height=4
        )

        item_height = 190
        self.towers_container.set_scrollable_area_dimensions((right_panel_w - 50, 2 + len(tower.tower_definitions) * item_height + 10))

        for n in range(0, len(tower.tower_definitions)):

            definition = tower.tower_definitions[n]

            tower_panel = UIPanel(
                relative_rect=pygame.Rect(2, 5 + item_height * n, right_panel_w - 55, item_height),
                starting_layer_height=4,
                manager=ui_manager,
                container=self.towers_container,
                object_id="#tower_panel"
            )

            UITextBox(
                "<b>" + definition.name + "</b>",
                pygame.Rect(5, 5, 340, 30),
                ui_manager,
                container=tower_panel,
                object_id="#no_border_textbox",
            )

            tower_stats_panel = UIPanel(
                relative_rect=pygame.Rect(7, 35, right_panel_w - 80, 110),
                starting_layer_height=4,
                manager=ui_manager,
                container=tower_panel,
                anchors={
                    "left": "left",
                    "right": "right",
                    "top": "top",
                    "bottom": "bottom"
                }
            )

            image_path = TOWERS_PATH + definition.image + ".png"
            image_size = (76, 76)
            image_panel = UIPanel(
                relative_rect=pygame.Rect(5, 5, image_size[0], image_size[1]),
                starting_layer_height=4,
                manager=ui_manager,
                container=tower_stats_panel,
            )

            UIImage(
                relative_rect=pygame.Rect(5, -8, image_size[0], image_size[1]),
                image_surface=resource_cache.get_resource(image_path,
                                                          resource_cache.SurfaceType, alpha=True),
                manager=ui_manager,
                container=image_panel
            )

            UITextBox(
                "<font color=#BB0000><b>Damages: </b></font>" + str(definition.damages) +
                "<br><br>"
                "<font color=#4488FF><b>Speed: </b></font>" + str(definition.speed) +
                "<br><br>" +
                "<font color=#00FF00><b>Range: </b></font>" + str(definition.range) +
                "<br><br>" +
                "<font color=#DEAF21><b>Cost: </b></font>" + str(definition.cost)
                ,
                pygame.Rect(5 + image_size[0], 0, 160, 140),
                ui_manager,
                container=tower_stats_panel,
                object_id="#no_border_textbox"
            )

            tower_build_btn = UIButton(
                pygame.Rect(8, -34, right_panel_w - 80, 30),
                "Build",
                ui_manager,
                container=tower_panel,
                anchors={
                    "left": "left",
                    "right": "right",
                    "top": "bottom",
                    "bottom": "bottom"
                }
            )
            register_ui_callback(tower_build_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.spawn_tower())

        buttons_panel = UIPanel(
            relative_rect=pygame.Rect(0, -140, right_panel_w - 5, 140),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=right_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom"
            }
        )

        # start fall button
        self.start_fall_btn = UIButton(
            pygame.Rect(20, -120, right_panel_w * 0.8, 40),
            "Start Fall",
            ui_manager,
            container=buttons_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom"
            }
        )
        register_ui_callback(self.start_fall_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.start_fall())

        # back button
        self.back_btn = UIButton(
            pygame.Rect(20, -60, right_panel_w * 0.8, 40),
            "Back To Menu",
            ui_manager,
            container=buttons_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
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

        enemies_spawner_gameobject = GameObject((0, 0), (0, 0), 0)
        enemies_spawner_gameobject.add_component(EnemiesSpawner).init_component()
        self.enemies_spawner = enemies_spawner_gameobject.get_components(EnemiesSpawner)[0]

    def deinit_mode(self):
        pass