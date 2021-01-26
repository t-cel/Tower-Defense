from modes.mode import *
from dynamic_sprite import DynamicSprite
from enemy import Enemy
from circle import Circle
from rectangle import Rectangle
from tower import Tower
from spell import Spell
from enemies_spawner import EnemiesSpawner
from game_gui_updater import GameGUIUpdater
from ui.level_end_window import LevelEndWindow
from ui.save_load_window import SaveLoadWindow

import map
import file_utils

import tower
import enemy
import spell

from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_world_space_health_bar import UIWorldSpaceHealthBar

from ui.ui import *
import pygame_gui

import session_data

class GameMode(Mode):

    def on_calcel_build(self):
        tower.towers.remove(self.dragging_tower)
        self.dragging_tower.game_object.mark_to_destroy = True
        self.on_finish_build()


    def on_place_tower(self):
        session_data.player_gold -= self.dragging_tower.definition.cost
        self.on_finish_build()
        self.game_gui_updater.update_stats_gui()


    def on_finish_build(self):
        self.building_panel.hide()
        self.dragging_tower = None
        for t in tower.towers:
            t.change_range_indicators_activity(False)


    def spawn_tower(self, index):
        self.building_panel.show()
        definition = tower.tower_definitions[index]

        tower_object = GameObject(
            get_tile_coords(3, 0),
            (1, 1),
            0
        )

        tower_object.add_component(StaticSprite).init_component(
            pos=(0, 0),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            image_path=TOWERS_PATH + definition.image + '.png',
            alpha=True
        )

        if definition.range_type == tower.CIRCULAR_RANGE_TYPE:
            tower_object.add_component(Circle).init_component(
                pos=(0, 0),
                radius=map.TILE_SIZE * 2,
                color=(25, 25, 225, 200),
                thickness=1
            )
        else:
            tower_object.add_component(Rectangle).init_component(
                pos=(0, 0),
                w=map.TILE_SIZE,
                h=map.TILE_SIZE,
                color=(25, 25, 225, 200),
                thickness=1
            )
            tower_object.add_component(Rectangle).init_component(
                pos=(0, 0),
                w=map.TILE_SIZE,
                h=map.TILE_SIZE,
                color=(25, 25, 225, 200),
                thickness=1
            )

        tower_object.add_component(Tower).init_component(
            enemies_path_coords=map_settings.settings.enemies_path_coords,
            definition=definition,
            on_build_callback=lambda: self.on_place_tower()
        )

        self.dragging_tower = tower_object.get_components(Tower)[0]


    def start_fall(self):
        self.build_mode_active = False
        self.enemies_spawner.start_spawn()
        self.start_fall_btn.disable()
        for btn in self.tower_build_buttons:
            btn.disable()
        self.game_gui_updater.update_stats_gui()

        self.switch_right_panel(False)
        self.towers_btn.disable()
        self.spells_btn.disable()


    def on_fall_end(self):
        self.build_mode_active = True
        self.start_fall_btn.enable()
        curr_fall = map_settings.settings.falls[self.enemies_spawner.current_fall]
        session_data.player_gold += curr_fall.gold_reward
        self.game_gui_updater.update_stats_gui()

        self.switch_right_panel(True)
        self.towers_btn.enable()
        self.spells_btn.enable()


    def on_map_end(self):
        self.game_gui_updater.update_stats_gui()
        level_end_window = LevelEndWindow(True, self)


    def on_add_damages_to_player(self):
        if session_data.player_hp <= 0 and not self.game_over:
            level_end_window = LevelEndWindow(False, self)
            self.game_over = True


    def on_enemy_destruction(self):
        self.game_gui_updater.update_stats_gui()


    def replay_map(self):
        switch_mode(MODE_GAME, file_name=self.current_map)


    def play_next_map(self):
        """
        Works only for campaign levels named as numbers where number means order of levels.
        """

        only_name = self.current_map.split('.')[0] # remove extension

        if only_name.isnumeric():
            as_num = int(only_name)

            maps = file_utils.get_all_files_in_path(MAPS_PATH)
            for m in maps:
                map_name = m.split('/')[1].split('.')[0]
                if map_name.isnumeric() and int(map_name) == as_num+1:
                    switch_mode(MODE_GAME, file_name=map_name + ".tdmap")
                    return

        # if we're not in campaign, select next level from list
        SaveLoadWindow(
            "maps",
            "Select Map",
            lambda f: switch_mode(MODE_GAME, file_name=f),
            False
        )


    def switch_right_panel(self, switch_to_towers):

        if switch_to_towers:
            self.towers_view_panel.show()
            self.spells_view_panel.hide()
        else:
            self.spells_view_panel.show()
            self.towers_view_panel.hide()

        self.game_gui_updater.update_stats_gui()


    def research_spell(self, index):

        definition = spell.spells_definitions[index]

        session_data.player_gold -= definition.research_cost
        session_data.spells_researched[index] = True

        self.game_gui_updater.update_stats_gui()


    def on_cancel_spell(self):
        self.casting_panel.hide()
        self.casting_spell.game_object.mark_to_destroy = True
        self.casting_spell = None


    def on_cast_spell_end(self):
        session_data.player_mana -= self.casting_spell.definition.use_cost
        self.casting_panel.hide()
        self.game_gui_updater.update_stats_gui()


    def on_cast_spell_start(self, index):
        self.casting_panel.show()

        definition = spell.spells_definitions[index]

        spell_go = GameObject(get_tile_coords(3, 0), (1, 1), 0)

        spell_go.add_component(Circle).init_component(
            pos=(0, 0),
            radius=map.TILE_SIZE * 2,
            color=(225, 25, 25, 200),
            thickness=1
        )

        spell_go.add_component(Spell).init_component(
            enemies_path_coords=map_settings.settings.enemies_path_coords,
            definition=definition,
            game_mode=self
        )

        self.casting_spell = spell_go.get_components(Spell)[0]


    def init_gui(self):
        # top panel
        top_panel = UIPanel(
            pygame.Rect(0, 0, SCREEN_WIDTH, 30),
            starting_layer_height=4,
            manager=ui_manager
        )

        # player's health bar
        self.player_hp_bar = UIPanel(
            relative_rect=pygame.Rect(SCREEN_WIDTH / 2, 5, SCREEN_WIDTH / 2 - 15, 15),
            manager=ui_manager,
            starting_layer_height=5,
            container=top_panel,
            object_id="#player_health_bar"
        )

        self.enemy_fall_bar = UIPanel(
            relative_rect=pygame.Rect(15, 5, SCREEN_WIDTH / 2 - 15, 15),
            manager=ui_manager,
            starting_layer_height=5,
            container=top_panel,
            object_id="#enemies_fall_bar"
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
            pygame.Rect(5, 40, 400, 35),
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

        self.gold_label = UITextBox(
            f"<b><font color=#DEAF21>Gold: </font>{session_data.player_gold}</b>, " +
            f"<b><font color=#4488FF>Mana: </font>{session_data.player_mana}</b>",
            pygame.Rect(5, 5, 500, 35),
            ui_manager,
            container=build_panel,
            object_id="#no_border_textbox",
        )

        """
        UITextBox(
            "<b>Towers</b>",
            pygame.Rect(5, 45, 300, 40),
            ui_manager,
            container=build_panel,
            object_id="#no_border_textbox",
        )
        """

        self.towers_btn = UIButton(
                pygame.Rect(5, 45, 145, 30),
                "Towers",
                ui_manager,
                container=build_panel,
        )
        register_ui_callback(self.towers_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.switch_right_panel(True))

        self.spells_btn = UIButton(
                pygame.Rect(155, 45, 145, 30),
                "Spells",
                ui_manager,
                container=build_panel,
        )
        register_ui_callback(self.spells_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.switch_right_panel(False))

        self.towers_view_panel = UIPanel(
            relative_rect=pygame.Rect(5, 80, right_panel_w - 20, 500),
            starting_layer_height=3,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=build_panel
        )

        self.towers_container = UIScrollingContainer(
            pygame.Rect(0, 0, right_panel_w - 30, 500 * Y_RATIO),
            ui_manager,
            container=self.towers_view_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            },
            object_id="#enemy_scrolling_container",
            starting_height=3
        )

        item_height = 200 * Y_RATIO
        self.towers_container.set_scrollable_area_dimensions((right_panel_w - 50, 2 + len(tower.tower_definitions) * item_height + 10 + 10))
        self.tower_build_buttons = []

        for n in range(0, len(tower.tower_definitions)):
            if n+1 > map_settings.settings.max_tower:
                break;

            definition = tower.tower_definitions[n]

            tower_panel = UIPanel(
                relative_rect=pygame.Rect(2, 5 + item_height * n, right_panel_w - 55, item_height),
                starting_layer_height=5,
                manager=ui_manager,
                container=self.towers_container,
                object_id="#tower_panel"
            )

            UITextBox(
                "<b>" + definition.name + "</b>",
                pygame.Rect(5, 5, 340 * X_RATIO, 30 * Y_RATIO),
                ui_manager,
                container=tower_panel,
                object_id="#no_border_textbox",
            )

            tower_stats_panel = UIPanel(
                relative_rect=pygame.Rect(7, 35, right_panel_w - 80, 120 * Y_RATIO),
                starting_layer_height=5,
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
            image_size = (76 * X_RATIO, 76 * Y_RATIO)
            image_panel = UIPanel(
                relative_rect=pygame.Rect(5, 5, image_size[0], image_size[1]),
                starting_layer_height=5,
                manager=ui_manager,
                container=tower_stats_panel,
            )

            UIImage(
                relative_rect=pygame.Rect(0, -8, image_size[0], image_size[1]),
                image_surface=resource_cache.get_resource(image_path,
                                                          resource_cache.SurfaceType, alpha=True),
                manager=ui_manager,
                container=image_panel
            )

            UITextBox(
                "<font color=#BB0000><b>Damages: </b></font>" + str(definition.damages) +
                "<br><br>"
                "<font color=#9141D1><b>Speed: </b></font>" + str(definition.projectile_speed) +
                "<br><br>" +
                "<font color=#4488FF><b>Reload Time: </b></font>" + str(definition.reload_time) +
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
                pygame.Rect(8, -34 * Y_RATIO, (right_panel_w - 80) * X_RATIO, 30 * Y_RATIO),
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
            self.tower_build_buttons.append(tower_build_btn)
            register_ui_callback(tower_build_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e, i=n: self.spawn_tower(i))


        # spells

        self.spells_view_panel = UIPanel(
            relative_rect=pygame.Rect(5, 80, right_panel_w - 20, 500),
            starting_layer_height=3,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=build_panel
        )

        spells_container = UIScrollingContainer(
            pygame.Rect(0, 0, right_panel_w - 30, 500 * Y_RATIO),
            ui_manager,
            container=self.spells_view_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            },
            object_id="#enemy_scrolling_container",
            starting_height=3
        )

        item_height = 320 * Y_RATIO
        spells_container.set_scrollable_area_dimensions(
            (right_panel_w - 50, 2 + len(spell.spells_definitions) * item_height + 10 + 10)
        )
        self.spell_research_buttons = []
        self.spell_use_buttons = []

        for n in range(0, len(spell.spells_definitions)):
            if n+1 > map_settings.settings.max_spell:
                break;

            definition = spell.spells_definitions[n]

            spell_panel = UIPanel(
                relative_rect=pygame.Rect(2, 5 + item_height * n, right_panel_w - 55, item_height),
                starting_layer_height=5,
                manager=ui_manager,
                container=spells_container,
                object_id="#tower_panel"
            )

            UITextBox(
                "<b>" + definition.name + "</b>",
                pygame.Rect(5, 5, 340 * X_RATIO, 30 * Y_RATIO),
                ui_manager,
                container=spell_panel,
                object_id="#no_border_textbox",
            )

            spell_stats_panel = UIPanel(
                relative_rect=pygame.Rect(7, 35, right_panel_w - 80, 240 * Y_RATIO),
                starting_layer_height=5,
                manager=ui_manager,
                container=spell_panel,
                anchors={
                    "left": "left",
                    "right": "right",
                    "top": "top",
                    "bottom": "bottom"
                }
            )

            image_path = EFFECTS_PATH + definition.icon_image + ".png"
            image_size = (76 * X_RATIO, 76 * Y_RATIO)
            image_panel = UIPanel(
                relative_rect=pygame.Rect((right_panel_w - 80) * 0.5 - image_size[0] * 0.5, 5, image_size[0], image_size[1]),
                starting_layer_height=5,
                manager=ui_manager,
                container=spell_stats_panel,
            )

            UIImage(
                relative_rect=pygame.Rect(0, -8, image_size[0], image_size[1]),
                image_surface=resource_cache.get_resource(image_path,
                                                          resource_cache.SurfaceType, alpha=True),
                manager=ui_manager,
                container=image_panel
            )

            UITextBox(
                spell.make_description(definition),
                pygame.Rect(5, 5 + image_size[1], right_panel_w - 80, item_height - image_size[1]),
                ui_manager,
                container=spell_stats_panel,
                object_id="#no_border_textbox"
            )

            spell_research_btn = UIButton(
                pygame.Rect(8, -34 * Y_RATIO, (right_panel_w - 200) * X_RATIO, 30 * Y_RATIO),
                "Research",
                ui_manager,
                container=spell_panel,
                anchors={
                    "left": "left",
                    "right": "right",
                    "top": "bottom",
                    "bottom": "bottom"
                }
            )
            self.spell_research_buttons.append(spell_research_btn)
            register_ui_callback(spell_research_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e, i=n: self.research_spell(i))

            spell_use_btn = UIButton(
                pygame.Rect(8 + (right_panel_w - 200) * X_RATIO, -34 * Y_RATIO, (right_panel_w - 200) * X_RATIO, 30 * Y_RATIO),
                "Use",
                ui_manager,
                container=spell_panel,
                anchors={
                    "left": "left",
                    "right": "right",
                    "top": "bottom",
                    "bottom": "bottom"
                }
            )
            self.spell_use_buttons.append(spell_use_btn)
            register_ui_callback(spell_use_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e, i=n: self.on_cast_spell_start(i))

        # bottom buttons section

        buttons_panel = UIPanel(
            relative_rect=pygame.Rect(0, -140 * Y_RATIO, right_panel_w - 5, 140 * Y_RATIO),
            starting_layer_height=100,
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
            pygame.Rect(20, -120 * Y_RATIO, right_panel_w * 0.8, 40 * Y_RATIO),
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
            pygame.Rect(20, -60 * Y_RATIO, right_panel_w * 0.8, 40 * Y_RATIO),
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


        # building
        self.building_panel = UIPanel(
            pygame.Rect(TILE_SIZE * MAP_W, 30, right_panel_w, right_panel_h),
            starting_layer_height=200,
            manager=ui_manager
        )

        UITextBox(
            "<font size=5><b>Place Tower On Map</b></font>",
            pygame.Rect(right_panel_w/6, right_panel_h/4, right_panel_w, 40),
            ui_manager,
            container=self.building_panel,
            object_id="#no_border_textbox"
        )

        cancel_btn = UIButton(
            pygame.Rect(80, (right_panel_h/4)+50, right_panel_w * 0.5, 40),
            "Cancel",
            ui_manager,
            container=self.building_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(cancel_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_calcel_build())

        self.building_panel.hide()

        # casting spell
        self.casting_panel = UIPanel(
            pygame.Rect(TILE_SIZE * MAP_W, 30, right_panel_w, right_panel_h),
            starting_layer_height=200,
            manager=ui_manager
        )

        UITextBox(
            "<font size=5><b>Click On Path To Cast Spell</b></font>",
            pygame.Rect(5, right_panel_h / 4, right_panel_w, 40),
            ui_manager,
            container=self.casting_panel,
            object_id="#no_border_textbox"
        )

        cancel_btn = UIButton(
            pygame.Rect(80, (right_panel_h / 4) + 50, right_panel_w * 0.5, 40),
            "Cancel",
            ui_manager,
            container=self.casting_panel,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom"
            }
        )
        register_ui_callback(cancel_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_cancel_spell())

        self.casting_panel.hide()


    def init_mode(self, **kwargs):

        session_data.player_hp = 100.0
        # session_data.player_mana = 1000
        session_data.enemies_in_level = 0

        tower.towers = []
        enemy.enemies = []
        session_data.spells_researched = [False] * len(spell.spells_definitions)

        self.build_mode_active = True

        map.create_map()
        self.current_map = kwargs.get("file_name")
        map.load_map(self.current_map)

        self.init_gui()

        enemies_spawner_gameobject = GameObject((0, 0), (0, 0), 0)
        enemies_spawner_gameobject.add_component(EnemiesSpawner).init_component(
            game_mode=self
        )
        self.enemies_spawner = enemies_spawner_gameobject.get_components(EnemiesSpawner)[0]

        game_gui_updater_go = GameObject((0, 0), (1, 1), 0)
        game_gui_updater_go.add_component(GameGUIUpdater).init_component(
            fall_label=self.fall_label,
            fall_reward_label=self.fall_reward_label,
            gold_label=self.gold_label,
            tower_build_buttons=self.tower_build_buttons,
            spell_research_buttons=self.spell_research_buttons,
            spell_use_buttons=self.spell_use_buttons,
            enemies_spawner=self.enemies_spawner,
            player_hp_bar=self.player_hp_bar,
            enemies_fall_bar=self.enemy_fall_bar,
            game_mode=self
        )
        self.game_gui_updater = game_gui_updater_go.get_components(GameGUIUpdater)[0]
        self.game_gui_updater.update_stats_gui()

        self.dragging_tower = None
        self.casting_spell = None

        # test effect
        """
        effect_go = GameObject((100, 100), (1, 1), 0)
        effect_go.add_component(DynamicSprite).init_component(
            pos=(0, 0),
            size=(256, 256),
            angle=0,
            images_paths=file_utils.get_all_files_in_path("sources\images\effects\explosion"),
            alpha=True,
            speed=0.3
        )
        """

        self.switch_right_panel(True)

        self.game_over = False


    def deinit_mode(self):
        pass