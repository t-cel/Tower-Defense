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

import random

from pygame_gui.elements.ui_text_box import UITextBox
import pygame


class EnemiesSpawner(Component):
    """
        Spawns enemies depending from current map settings.
    """

    def __init__(self, game_object):
        super().__init__(game_object)
        self.current_fall = 0
        self.current_group = 0
        self.current_group_enemies_to_spawn = [0] * len(enemy.enemies_definitions)
        self.random_interval = 0.0

        self.t = 0.0
        self.spawning = False
        self.on_fall_end_callback = None

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

    @staticmethod
    def spawn_enemy(index):
        definition = enemy.enemies_definitions[index]

        enemy_object = GameObject(
            map.get_tile_coords(map_settings.settings.enemies_path_coords[0][0] - 1, map_settings.settings.enemies_path_coords[0][1]),
            (1, 1),
            0
        )

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
            definition=definition
        )


    def start_spawn(self, on_fall_end_callback):
        self.spawning = True
        self.current_fall = 0
        self.current_group = 0
        self.current_group_enemies_to_spawn = map_settings.settings.falls[self.current_fall].groups[self.current_group].enemies_counts

        self.on_fall_end_callback = on_fall_end_callback

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
                self.current_group_enemies_to_spawn = fall.groups[self.current_group].enemies_counts


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

        #print("items: " + str(list(available_enemies.keys())) + ", random: " + str(rand))

        EnemiesSpawner.spawn_enemy(index)
        self.update_interval()


    def init_component(self, **kwargs):
        pass


    def update(self, dt):
        if self.spawning:
            self.t += dt
            if self.t > self.random_interval:
                self.on_spawn()
                self.t = 0.0

        if self.wait_for_fall_end:
            if len(enemy.enemies) == 0:
                self.on_fall_end_callback()
                self.wait_for_fall_end = False

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