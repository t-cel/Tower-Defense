from ui.ui import *
from component import Component
from game_object import GameObject
from dynamic_sprite import DynamicSprite
from static_sprite import StaticSprite
from definitions import *
from enemy import Enemy

import map
import file_utils
import enemy
import map_settings
import session_data

import random

from pygame_gui.elements.ui_text_box import UITextBox
import pygame

class EnemiesSpawner(Component):
    """
        Spawns enemies depending from current map settings.
    """

    def __init__(self, game_object):
        super().__init__(game_object)
        self.current_fall = -1
        self.current_group = 0
        self.current_group_enemies_to_spawn = [0] * len(enemy.enemies_definitions)
        self.random_interval = 0.0

        self.t = 0.0
        self.spawning = False
        self.game_mode = None

        self.wait_for_fall_end = False

        """
        self.fall_label_opacity = 0
        self.label_animation_speed = 0.5
        self.label_animation_t = 0.0
        self.fall_label = UITextBox(
                "<font size=7><b><font color=#00000000>Starting Fall 0</font></b></font>",
                pygame.Rect(SCREEN_WIDTH/4, SCREEN_HEIGHT/4, SCREEN_WIDTH, SCREEN_HEIGHT),
                ui_manager,
                object_id="#no_border_textbox"
        )
        """

    def spawn_enemy(self, index):
        definition = enemy.enemies_definitions[index]

        enemy_object = GameObject(
            map.get_tile_coords(map_settings.settings.enemies_path_coords[0][0] - 1, map_settings.settings.enemies_path_coords[0][1]),
            (1, 1),
            0
        )

        # for f in file_utils.get_all_files_in_path(ENEMIES_PATH + definition.sprites_directory):
        #     print(f)

        enemy_object.add_component(DynamicSprite).init_component(
            pos=(0, -map.TILE_SIZE / 4),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            images_paths=file_utils.get_all_files_in_path(ENEMIES_PATH + definition.sprites_directory),
            alpha=True
        )

        enemy_object.add_component(DynamicSprite).init_component(
            pos=(0, -map.TILE_SIZE / 4),
            size=(map.TILE_SIZE, map.TILE_SIZE),
            angle=0,
            images_paths=file_utils.get_all_files_in_path(ENEMIES_PATH + definition.sprites_directory + "/reversed"),
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
            path_coords=map_settings.settings.enemies_path_coords,
            definition=definition,
            game_mode=self.game_mode
        )

        session_data.enemies_left -= 1


    def start_spawn(self):
        self.spawning = True
        self.current_group = 0
        self.current_fall += 1
        self.current_group_enemies_to_spawn = map_settings.settings.falls[self.current_fall].groups[self.current_group].enemies_counts.copy()

        # print(self.current_group_enemies_to_spawn)
        session_data.enemies_left = session_data.enemies_in_level = 0
        for group in map_settings.settings.falls[self.current_fall].groups:
            session_data.enemies_in_level += sum(group.enemies_counts)
        session_data.enemies_left = session_data.enemies_in_level
        # print(f"enemies left: {enemies_left}")

        self.update_interval()


    def update_interval(self):
        self.random_interval = random.uniform(
            map_settings.settings.falls[self.current_fall].groups[self.current_group].interval[0],
            map_settings.settings.falls[self.current_fall].groups[self.current_group].interval[1]
        )


    def on_end_spawn_group(self):
        fall = map_settings.settings.falls[self.current_fall]
        group = fall.groups[self.current_group]
        if group.spawn_mode == map_settings.SWAWN_MODE_END_OF_PREVIOUS_GROUP_SPAWN:
            if self.current_group == len(fall.groups) - 1:
                # print("end of fall")
                self.wait_for_fall_end = True
                self.spawning = False
            else:
                # print("next group")
                self.current_group += 1
                self.current_group_enemies_to_spawn = fall.groups[self.current_group].enemies_counts.copy()
                self.t = 0.0
                self.random_interval = fall.groups[self.current_group].spawn_delay


    def on_spawn(self):
        # print(self.current_group_enemies_to_spawn)

        available_enemies = {}
        for i in range(0, len(self.current_group_enemies_to_spawn)):
            if self.current_group_enemies_to_spawn[i] != 0:
                available_enemies[str(i)] = self.current_group_enemies_to_spawn[i]

        if len(available_enemies) == 0:
            self.on_end_spawn_group()
            return

        rand = random.randint(0, len(available_enemies) - 1)
        index = int(list(available_enemies.keys())[rand])
        self.current_group_enemies_to_spawn[index] -= 1

        self.spawn_enemy(index)
        self.update_interval()


    def init_component(self, **kwargs):
        self.game_mode = kwargs.get("game_mode")


    def update(self, dt):
        if self.spawning:
            self.t += dt
            if self.t > self.random_interval:
                self.on_spawn()
                self.t = 0.0

        if session_data.player_hp > 0:
            if self.wait_for_fall_end and len(enemy.enemies) == 0 and session_data.enemies_left == 0:
                if self.current_fall == len(map_settings.settings.falls)-1:
                    self.game_mode.on_map_end()
                else:
                    self.game_mode.on_fall_end()
                self.wait_for_fall_end = False

        """
        if self.wait_for_fall_end:
            if len(enemy.enemies) == 0:
                self.on_fall_end_callback()
                self.wait_for_fall_end = False
        """

        #print(session_data.enemies_left, session_data.enemies_in_level)

        """
        if dt < 1.0 and self.label_animation_t < 1.0:
            self.label_animation_t += self.label_animation_speed * dt
            self.fall_label_opacity = int(255.0 * self.label_animation_t)
            if self.fall_label_opacity > 255:
                self.fall_label_opacity = 255
            as_str = list(str(hex(self.fall_label_opacity))[-2:])
            if as_str[0] == "x":
                as_str[0] = "0"
            self.fall_label.html_text = "<font size=7><b><font color=#000000" + ("".join(as_str)) +">Starting Fall 0</font></b></font>"
            self.fall_label.rebuild()
        """