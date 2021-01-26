from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer

import pygame_gui
from ui.ui import *

import resource_cache
import file_utils
import math_utils
import utils
import tower
import spell

from pathlib import Path
import enemy

import map_settings
from map_settings import EnemiesFall
from map_settings import EnemiesGroup

class MapSettingsWindow(UIWindow):

    def on_fall_add_btn_click(self):
        map_settings.settings.falls.append(
            EnemiesFall(
                [EnemiesGroup(
                    [0] * len(enemy.enemies_definitions),
                    1.0,
                    [0.5, 1.0]
                )],
            100)
        )
        self.current_selected_group = 0
        self.update_settings()


    def on_fall_remove_btn_click(self):
        if len(map_settings.settings.falls) > 1:
            map_settings.settings.falls.remove(map_settings.settings.falls[self.current_selected_fall])
            self.current_selected_fall = 0
            self.current_selected_group = 0
            self.update_settings()


    def on_fall_list_item_select(self):
        for i in range(0, len(self.falls_ui_list.item_list)):
            if self.falls_ui_list.item_list[i]['selected']:
                self.current_selected_fall = i
                self.current_selected_group = 0
                self.update_groups_list()
                self.update_fall_panel()
                return


    def on_group_add_btn_click(self):
        map_settings.settings.falls[self.current_selected_fall].groups.append(
            EnemiesGroup(
                [0] * len(enemy.enemies_definitions),
                1.0,
                [0.5, 1.0]
            )
        )
        self.update_groups_list()
        self.update_group_panel()
        self.update_enemies_panel()


    def on_group_remove_btn_click(self):
        curr_fall = map_settings.settings.falls[self.current_selected_fall]
        if len(curr_fall.groups) > 1:
            curr_fall.groups.remove(curr_fall.groups[self.current_selected_group])
        self.current_selected_group = 0
        self.update_groups_list()


    def on_fall_gold_text_changed(self, e):
        if len(map_settings.settings.falls) > 0:
            if len(e.text) > 0 and e.text.isnumeric():
                map_settings.settings.falls[self.current_selected_fall].gold_reward = int(e.text)
            else:
                map_settings.settings.falls[self.current_selected_fall].gold_reward = 0
                self.update_fall_panel()


    def on_start_gold_text_changed(self, e):
        if len(e.text) > 0 and e.text.isnumeric():
            map_settings.settings.start_gold = int(e.text)
        else:
            map_settings.settings.start_gold = 0
            self.update_general_panel()


    def on_start_mana_text_changed(self, e):
        if len(e.text) > 0 and e.text.isnumeric():
            map_settings.settings.start_mana = int(e.text)
        else:
            map_settings.settings.start_mana = 0
            self.update_general_panel()


    def on_group_list_item_select(self, e):
        for i in range(0, len(self.groups_ui_list.item_list)):
            if self.groups_ui_list.item_list[i]['selected']:
                self.current_selected_group = i
                self.update_group_panel()
                self.update_enemies_panel()
                return


    def on_group_spawn_delay_changed(self, e):
        if len(map_settings.settings.falls) > 0:
            if len(map_settings.settings.falls[self.current_selected_fall].groups) > 0:
                curr_group = map_settings.settings.falls[self.current_selected_fall].groups[self.current_selected_group]
                if len(e.text) > 0 and utils.is_float(e.text):
                    curr_group.spawn_delay = float(e.text)
                else:
                    curr_group.spawn_delay = 0.0
                    self.update_group_panel()



    def on_group_spawn_interval_left_changed(self, e):
        if len(map_settings.settings.falls) > 0:
            if len(map_settings.settings.falls[self.current_selected_fall].groups) > 0:
                curr_group = map_settings.settings.falls[self.current_selected_fall].groups[self.current_selected_group]
                if len(e.text) > 0 and utils.is_float(e.text):
                    curr_group.interval[0] = float(e.text)
                else:
                    curr_group.interval[0] = 0.0
                    self.update_group_panel()


    def on_group_spawn_interval_right_changed(self, e):
        if len(map_settings.settings.falls) > 0:
            if len(map_settings.settings.falls[self.current_selected_fall].groups) > 0:
                curr_group = map_settings.settings.falls[self.current_selected_fall].groups[self.current_selected_group]
                if len(e.text) > 0 and utils.is_float(e.text):
                    curr_group.interval[1] = float(e.text)
                else:
                    curr_group.interval[1] = 0.0
                    self.update_group_panel()


    def on_change_enemy_count(self, e, i):
        if len(map_settings.settings.falls) > 0:
            if len(map_settings.settings.falls[self.current_selected_fall].groups) > 0:
                curr_group = map_settings.settings.falls[self.current_selected_fall].groups[self.current_selected_group]
                if len(e.text) > 0 and e.text.isnumeric():
                    curr_group.enemies_counts[i] = int(e.text)
                else:
                    curr_group.enemies_counts[i] = 0
                    self.update_enemies_panel()


    def on_max_tower_text_changed(self, e):
        if len(e.text) > 0 and e.text.isnumeric():
            map_settings.settings.max_tower =  math_utils.clamp(int(e.text), 0, len(tower.tower_definitions))
        else:
            map_settings.settings.max_tower = len(tower.tower_definitions)
            self.update_general_panel()


    def on_max_spell_text_changed(self, e):
        if len(e.text) > 0 and e.text.isnumeric():
            map_settings.settings.max_spell =  math_utils.clamp(int(e.text), 0, len(spell.spells_definitions))
        else:
            map_settings.settings.max_spell = len(spell.spells_definitions)
            self.update_general_panel()


    def __init__(self):
        windowWidth = 1340
        windowHeight = 600
        super().__init__(
            pygame.Rect(
                SCREEN_WIDTH * 0.5 - windowWidth * 0.5,
                SCREEN_HEIGHT * 0.5 - windowHeight * 0.5,
                windowWidth,
                windowHeight,
            ),
            ui_manager,
            window_display_title="Settings",
            resizable=False
        )

        UILabel(pygame.Rect(0, 0, 80, 30), "General", ui_manager, container=self)

        general_panel = UIPanel(
            pygame.Rect(10, 30, 250, 600 - 100),
            starting_layer_height=4,
            manager=ui_manager,
            container=self,
            object_id="#thicker_panel"
        )
        UILabel(pygame.Rect(10, 10, 80, 30), "Start Gold", ui_manager, container=general_panel)

        self.start_gold_text_line = UITextEntryLine(
            pygame.Rect(100, 10, 60, 20),
            manager=ui_manager,
            container=general_panel,
            #object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        register_ui_callback(self.start_gold_text_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_start_gold_text_changed(e))

        UILabel(pygame.Rect(10, 40, 80, 30), "Start Mana", ui_manager, container=general_panel)
        self.start_mana_text_line = UITextEntryLine(
            pygame.Rect(100, 40, 60, 20),
            manager=ui_manager,
            container=general_panel,
            #object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        register_ui_callback(self.start_mana_text_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_start_mana_text_changed(e))

        UILabel(pygame.Rect(10, 70, 80, 30), "Max Tower", ui_manager, container=general_panel)

        self.max_tower_text_line = UITextEntryLine(
            pygame.Rect(100, 70, 60, 20),
            manager=ui_manager,
            container=general_panel,
            #object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        register_ui_callback(self.max_tower_text_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_max_tower_text_changed(e))

        UILabel(pygame.Rect(10, 100, 80, 30), "Max Spell", ui_manager, container=general_panel)

        self.max_spell_text_line = UITextEntryLine(
            pygame.Rect(100, 100, 60, 20),
            manager=ui_manager,
            container=general_panel,
            #object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        register_ui_callback(self.max_spell_text_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_max_spell_text_changed(e))


        # ---------------------------- falls

        UILabel(pygame.Rect(250, 0, 80, 30), "Falls", ui_manager, container=self)

        self.falls_list = ["Dummy", "Dummy"]
        self.current_selected_fall = 0
        self.falls_ui_list = UISelectionList(
            pygame.Rect(270, 30, 250, 220),
            item_list=self.falls_list,
            manager=ui_manager,
            container=self,
            object_id="#thicker_panel",
        )

        register_ui_callback(self.falls_ui_list, pygame_gui.UI_SELECTION_LIST_NEW_SELECTION, lambda e: self.on_fall_list_item_select())

        self.fall_add_btn = UIButton(pygame.Rect(270, 250, 125, 30), "Add Fall", ui_manager, container=self)
        self.fall_remove_btn = UIButton(pygame.Rect(395, 250, 125, 30), "Remove Fall", ui_manager, container=self)

        register_ui_callback(self.fall_add_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_fall_add_btn_click())
        register_ui_callback(self.fall_remove_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_fall_remove_btn_click())

        UILabel(pygame.Rect(262, 290, 120, 30), "Fall Settings", ui_manager, container=self)

        self.fall_settings_panel = UIPanel(
            pygame.Rect(270, 320, 250, 210),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=self
        )

        # gold reward

        UILabel(pygame.Rect(5, 10, 100, 30), "Gold Reward", ui_manager, container=self.fall_settings_panel)

        self.fall_gold_reward = UITextEntryLine(
            pygame.Rect(105, 10, 60, 20),
            manager=ui_manager,
            container=self.fall_settings_panel,
        )

        register_ui_callback(self.fall_gold_reward, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_fall_gold_text_changed(e))

        # ---------------------------- groups

        UILabel(pygame.Rect(515, 0, 80, 30), "Groups", ui_manager, container=self)

        self.groups_list = []
        self.current_selected_group = 0
        self.groups_ui_list = UISelectionList(
            pygame.Rect(530, 30, 380, 220),
            item_list=self.groups_list,
            manager=ui_manager,
            container=self,
            object_id="#thicker_panel",
        )

        register_ui_callback(self.groups_ui_list, pygame_gui.UI_SELECTION_LIST_NEW_SELECTION,
                             lambda e: self.on_group_list_item_select(e))

        self.group_add_btn = UIButton(pygame.Rect(530, 250, 380*0.5, 30), "Add Group", ui_manager, container=self)
        self.group_remove_btn = UIButton(pygame.Rect(530+380*0.5, 250, 380*0.5, 30), "Remove Group", ui_manager, container=self)

        register_ui_callback(self.group_add_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_group_add_btn_click())
        register_ui_callback(self.group_remove_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: self.on_group_remove_btn_click())

        UILabel(pygame.Rect(530, 290, 120, 30), "Group Settings", ui_manager, container=self)

        group_settings_panel = UIPanel(
            pygame.Rect(530, 320, 380, 210),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=self
        )

        UILabel(pygame.Rect(5, 10, 100, 30), "Spawn After", ui_manager, container=group_settings_panel)

        self.group_spawn_mode_dropdown = UIDropDownMenu(
            ["End Of Previous Group Spawn","Previous Group Destruction"],
            "End Of Previous Group Spawn",
            pygame.Rect(105, 15, 250, 20),
            ui_manager,
            container=group_settings_panel
        )


        # spawn delay

        UILabel(pygame.Rect(5, 45, 100, 30), "Spawn Delay", ui_manager, container=group_settings_panel)
        self.spawn_delay_entry_line = UITextEntryLine(pygame.Rect(105, 45, 40, 20), manager=ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(150, 45, 60, 30), "seconds", ui_manager, container=group_settings_panel)

        register_ui_callback(self.spawn_delay_entry_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_group_spawn_delay_changed(e))

        # interval

        UILabel(pygame.Rect(-2, 80, 100, 30), "Interval:", ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(2, 115, 50, 30), "From", ui_manager, container=group_settings_panel)
        self.interval_from_entry_line = UITextEntryLine(pygame.Rect(50, 115, 40, 20), manager=ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(95, 115, 20, 30), "To", ui_manager, container=group_settings_panel)
        self.interval_to_entry_line = UITextEntryLine(pygame.Rect(120, 115, 40, 20), manager=ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(165, 115, 60, 30), "seconds", ui_manager, container=group_settings_panel)

        register_ui_callback(self.interval_from_entry_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_group_spawn_interval_left_changed(e))

        register_ui_callback(self.interval_to_entry_line, pygame_gui.UI_TEXT_ENTRY_CHANGED,
                             lambda e: self.on_group_spawn_interval_right_changed(e))

        # ---------------------------- enemies

        self.enemies_label = UILabel(pygame.Rect(910, 0, 80, 30), "Enemies", ui_manager, container=self)

        self.enemies_view_panel = UIPanel(
            relative_rect=pygame.Rect(920, 30, 385, 505),
            starting_layer_height=4,
            object_id="#thicker_panel",
            manager=ui_manager,
            container=self
        )
        #self.enemies_view_panel.hide()
        #self.enemies_label.hide()

        #250, 600 - 100
        self.enemy_container = UIScrollingContainer(
            pygame.Rect(0, 0, 380, 500),
            ui_manager,
            container=self.enemies_view_panel,
            object_id="#enemy_scrolling_container",
            starting_height=4
        )

        item_height = 165
        self.enemy_container.set_scrollable_area_dimensions((360, 5 + len(enemy.enemies_definitions) * item_height + 10))

        """
        for n in range(0, 24):
            UIButton(
                pygame.Rect(5, 5 + 50 * n, 370, 45),
                "hi",
                ui_manager,
                self.enemy_container
            )
        """

        self.enemies_counts_entry_lines = []
        for n in range(0, len(enemy.enemies_definitions)):
            enemy_panel = UIPanel(
                relative_rect=pygame.Rect(5, 5 + item_height * n, 350, item_height),
                starting_layer_height=4,
                manager=ui_manager,
                container=self.enemy_container,
                object_id="#thicker_panel"
            )
            enemy_stats_panel = UIPanel(
                relative_rect=pygame.Rect(10, 35, 325, 80),
                starting_layer_height=4,
                manager=ui_manager,
                container=enemy_panel
            )

            UITextBox(
                "<b>" + enemy.enemies_definitions[n].name + "</b>",
                pygame.Rect(5, 5, 340, 30),
                ui_manager,
                container=enemy_panel,
                object_id="#no_border_textbox",
            )
            definition = enemy.enemies_definitions[n]
            preview_sprite_path = ENEMIES_PATH + definition.sprites_directory + "/" + definition.preview_sprite + ".png"
            image_size = (720 * 0.15, 480 * 0.15)
            UIImage(
                relative_rect=pygame.Rect(5, 5, image_size[0], image_size[1]),
                image_surface=resource_cache.get_resource(preview_sprite_path,
                                                          resource_cache.SurfaceType, alpha=True),
                manager=ui_manager,
                container=enemy_stats_panel
            )
            UITextBox(
                "<font color=#00FF00><b>Health: </b></font>" + str(definition.health) +
                "<br><br>"
                "<font color=#BB0000><b>Damage: </b></font>" + str(definition.damages) +
                "</br></br>" +
                "<font color=#4488FF><b>Speed: </b></font>" + str(definition.speed)
                ,
                pygame.Rect(5 + image_size[0] + 5, 5, 120, 140),
                ui_manager,
                container=enemy_stats_panel,
                object_id="#no_border_textbox"
            )
            UITextBox(
                "Count: ",
                pygame.Rect(5, item_height - 45, 80, 30),
                ui_manager,
                container=enemy_panel,
                object_id="#no_border_textbox"
            )
            self.enemies_counts_entry_lines.append(UITextEntryLine(
                pygame.Rect(65, item_height - 45, 50, 25),
                manager=ui_manager,
                container=enemy_panel,
            ))

            register_ui_callback(self.enemies_counts_entry_lines[n], pygame_gui.UI_TEXT_ENTRY_CHANGED,
                                 lambda e, i=n: self.on_change_enemy_count(e, i))

        self.set_blocking(True)
        self.update_settings()


    def update_falls_list(self):
        self.falls_list = []
        for i in range(0, len(map_settings.settings.falls)):
            self.falls_list.append("Fall " + str(i+1))
        self.falls_ui_list.set_item_list(self.falls_list)

        if len(self.falls_list) > 0:
            # self.falls_ui_list.item_list[self.current_selected_fall]['selected'] = True
            curr_fall = map_settings.settings.falls[self.current_selected_fall]
            self.fall_gold_reward.set_text(str(curr_fall.gold_reward))


    def update_groups_list(self):
        if len(self.falls_list) > 0:
            curr_fall = map_settings.settings.falls[self.current_selected_fall]

            # there is always at least 1 group per fall
            self.groups_list = []
            for i in range(0, len(curr_fall.groups)):
                self.groups_list.append("Group " + str(i + 1))
            self.groups_ui_list.set_item_list(self.groups_list)


    def update_group_panel(self):
        curr_fall = map_settings.settings.falls[self.current_selected_fall]
        if len(self.falls_list) > 0 and len(curr_fall.groups) > 0:
            curr_group = curr_fall.groups[self.current_selected_group]
            self.group_spawn_mode_dropdown.selected_option = curr_group.spawn_mode
            self.spawn_delay_entry_line.set_text(str(curr_group.spawn_delay))
            self.interval_from_entry_line.set_text(str(curr_group.interval[0]))
            self.interval_to_entry_line.set_text(str(curr_group.interval[1]))


    def update_fall_panel(self):
        self.fall_gold_reward.set_text(str(map_settings.settings.falls[self.current_selected_fall].gold_reward))


    def update_general_panel(self):
        self.start_gold_text_line.set_text(str(map_settings.settings.start_gold))
        self.start_mana_text_line.set_text(str(map_settings.settings.start_mana))
        self.max_tower_text_line.set_text(str(map_settings.settings.max_tower))
        self.max_spell_text_line.set_text(str(map_settings.settings.max_spell))


    def update_enemies_panel(self):
        curr_group = map_settings.settings.falls[self.current_selected_fall].groups[self.current_selected_group]
        for n in range(0, len(self.enemies_counts_entry_lines)):
            self.enemies_counts_entry_lines[n].set_text(str(curr_group.enemies_counts[n]))

    def update_settings(self):
        self.update_general_panel()
        self.update_falls_list()
        self.update_groups_list()








