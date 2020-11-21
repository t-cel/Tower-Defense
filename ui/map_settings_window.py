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

from pathlib import Path
import enemy

from map_settings import *

class MapSettingsWindow(UIWindow):
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
        self.start_gold_text_line.set_text(str(500))

        """
        UILabel(
            pygame.Rect(3, 40, 80, 30),
            "Next Map",
            ui_manager,
            container=self.general_panel,
            anchors={
                "left": "left",
                "right": "left",
                "top": "top",
                "bottom": "bottom"
            }
        )

        self.next_map_text_line = UITextEntryLine(
            pygame.Rect(100, 10, 60, 20),
            manager=ui_manager,
            container=self.general_panel,
            #object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'left',
                'top': 'top',
                'bottom': 'bottom'
            }
        )
        """

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

        self.fall_add_btn = UIButton(pygame.Rect(270, 250, 125, 30), "Add Fall", ui_manager, container=self)
        self.fall_remove_btn = UIButton(pygame.Rect(395, 250, 125, 30), "Remove Fall", ui_manager, container=self)

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

        # ---------------------------- groups

        UILabel(pygame.Rect(515, 0, 80, 30), "Groups", ui_manager, container=self)

        self.groups_list = ["Dummy", "Dummy", "Dummy"]
        self.current_selected_group = 0
        self.groups_ui_list = UISelectionList(
            pygame.Rect(530, 30, 380, 220),
            item_list=self.groups_list,
            manager=ui_manager,
            container=self,
            object_id="#thicker_panel",
        )

        self.group_add_btn = UIButton(pygame.Rect(530, 250, 380*0.5, 30), "Add Group", ui_manager, container=self)
        self.group_remove_btn = UIButton(pygame.Rect(530+380*0.5, 250, 380*0.5, 30), "Remove Group", ui_manager, container=self)

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

        # interval

        UILabel(pygame.Rect(-2, 80, 100, 30), "Interval:", ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(2, 115, 50, 30), "From", ui_manager, container=group_settings_panel)
        self.interval_from_entry_line = UITextEntryLine(pygame.Rect(50, 115, 40, 20), manager=ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(95, 115, 20, 30), "To", ui_manager, container=group_settings_panel)
        self.interval_to_entry_line = UITextEntryLine(pygame.Rect(120, 115, 40, 20), manager=ui_manager, container=group_settings_panel)
        UILabel(pygame.Rect(165, 115, 60, 30), "seconds", ui_manager, container=group_settings_panel)

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

        self.set_blocking(True)
        self.update_settings()


    def update_settings(self):
        self.start_gold_text_line.set_text(str(settings.start_gold))

        self.falls_list = []
        for i in range(0, len(settings.falls)):
            self.falls_list.append("Fall " + str(i+1))
        self.falls_ui_list.set_item_list(self.falls_list)

        if len(self.falls_list) > 0:
            curr_fall = settings.falls[self.current_selected_fall]
            self.fall_gold_reward.set_text(str(curr_fall.gold_reward))

            # there is always at least 1 group per fall
            self.groups_list = []
            for i in range(0, len(curr_fall.groups)):
                self.groups_list.append("Group " + str(i + 1))
            self.groups_ui_list.set_item_list(self.groups_list)

            curr_group = curr_fall.groups[self.current_selected_group]
            self.group_spawn_mode_dropdown.selected_option = curr_group.spawn_mode # todo: check if works
            self.spawn_delay_entry_line.set_text(str(curr_group.spawn_delay))
            self.interval_from_entry_line.set_text(str(curr_group.interval[0]))
            self.interval_to_entry_line.set_text(str(curr_group.interval[1]))

            for n in range(0, len(self.enemies_counts_entry_lines)):
                self.enemies_counts_entry_lines[n].set_text(str(curr_group.enemies_counts[n]))

        else:
            # todo: hide or reset lists and controls
            self.groups_ui_list.set_item_list([])








