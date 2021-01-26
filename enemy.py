from map import *
from dynamic_sprite import DynamicSprite
from component import Component
from static_sprite import StaticSprite
from auto_destroy import AutoDestroy

from circle import Circle

import session_data

import math_utils
import json
import pygame

enemies = []
enemies_definitions = []

class EnemyDefinition:
    def __init__(self, name, sprites_directory, speed, health, damages, preview_sprite, corpses_image, hit_sounds):
        self.name = name
        self.sprites_directory = sprites_directory
        self.speed = speed
        self.health = health
        self.damages = damages
        self.preview_sprite = preview_sprite
        self.corpses_image = corpses_image
        self.hit_sounds = hit_sounds


def load_enemies_definitions():
    f = open(DEFINITIONS_PATH + "enemies.json")
    data = json.load(f)
    for enemy_definition in data["enemies"]:
        enemies_definitions.append(
            EnemyDefinition(
                enemy_definition["name"],
                enemy_definition["spritesDirectory"],
                enemy_definition["speed"],
                enemy_definition["health"],
                enemy_definition["damages"],
                enemy_definition["previewSprite"],
                enemy_definition["corpsesImage"],
                enemy_definition["hitSounds"]
            )
        )


class Enemy(Component):
    def __init__(self, game_object):
        super().__init__(game_object)

        self.path_coords = None
        self.coord_index = 0
        self.game_object = game_object
        self.t = 0.0
        self.speed = 1.5
        self.start_coords = game_object.pos

        self.hp = 100.0
        self.damages = 0
        self.hp_bar = None

        self.dynamic_sprite = None
        self.last_x = 0.0
        self.moving_reversed = False

        self.last_pos = (0, 0)

        self.definition = None
        self.game_mode = None
        self.dead = False

        self.slow_down_timer = 0.0

        enemies.append(self)
        # print("append")

        self.hit_sounds = []

        for hit_sound in self.hit_sounds:
            hit_sound.set_volume(0.25)


    def get_target_pos(self):
        return self.game_object.pos[0], \
               self.game_object.pos[1]


    def init_component(self, **kwargs):
        self.path_coords = kwargs.get("path_coords")
        self.definition = kwargs.get("definition")
        self.game_mode = kwargs.get("game_mode")

        self.speed = self.definition.speed
        self.hp = self.definition.health
        self.damages = self.definition.damages

        self.hp_bar = self.game_object.get_components(StaticSprite)[-1]
        self.hp_bar.change_activity(False)

        self.dynamic_sprite = self.game_object.get_components(DynamicSprite)[0]

        for hit_sound in self.definition.hit_sounds:
            self.hit_sounds.append(
                pygame.mixer.Sound(SOUNDS_PATH + hit_sound + ".ogg")
            )

        # tests

        #self.game_object.add_component(Circle).init_component(
        #    pos=(0, 0),
        #    radius=5,
        #    color=(25, 225, 25, 200),
        #    thickness=1,
        #    z_pos=900
        #)


    def take_damage(self, damage):
        # print(self.hp)
        self.hp -= damage

        if not self.dead:
            if self.hp <= 0:
                self.dead = True
                if random.random() > 0.4:
                    self.hit_sounds[random.randrange(0, len(self.hit_sounds))].play()

                self.hp = 0

                # spawn corpses
                corpses_go = GameObject((self.game_object.pos[0], self.game_object.pos[1] - 10 + random.random() * 5.0), (1, 1), 0)
                corpses_go.add_component(StaticSprite).init_component(
                    pos=(0,0),
                    size=(TILE_SIZE, TILE_SIZE),
                    angle=0,
                    image_path=CORPSES_PATH + self.definition.corpses_image + ".png",
                    z_pos=101 + corpses_go.pos[1],
                    alpha=True
                )
                corpses_go.add_component(AutoDestroy).init_component(
                    time_to_destroy=random.random()*4.0+7.0
                )

            # update hp bar
            new_width = int(TILE_SIZE * (self.hp / 100.0))
            self.hp_bar.set_size((new_width, TILE_SIZE))
            self.hp_bar.set_pos((TILE_SIZE / 2 - new_width / 2, -TILE_SIZE * 0.65))
            self.hp_bar.change_activity(True)


    def slow_down(self, time, percent):
        if self.slow_down_timer <= 0.0:
            self.speed = self.speed * percent

        # if hit while already being slowdown, just reset timer
        self.slow_down_timer = time


    def get_velocity(self):
        return self.game_object.pos[0] - self.last_pos[0], self.game_object.pos[1] - self.last_pos[1]


    def update_sprite(self):
        delta_x = self.game_object.pos[0] - self.last_x

        if delta_x < 0 and not self.moving_reversed:
            self.dynamic_sprite.change_activity(False)
            self.dynamic_sprite = self.game_object.get_components(DynamicSprite)[1]
            self.dynamic_sprite.change_activity(True)
            self.moving_reversed = True
        elif delta_x > 0 and self.moving_reversed:
            self.dynamic_sprite.change_activity(False)
            self.dynamic_sprite = self.game_object.get_components(DynamicSprite)[0]
            self.dynamic_sprite.change_activity(True)
            self.moving_reversed = False

        self.last_x = self.game_object.pos[0]


    def update(self, dt):

        if self.hp <= 0:
            session_data.player_mana += 10
            self.game_object.mark_to_destroy = True
            enemies.remove(self)
            self.game_mode.on_enemy_destruction()

        self.last_pos = self.game_object.pos
        self.t += self.speed * dt

        if self.t > 0.99:
            if self.coord_index == len(self.path_coords) - 1:
                session_data.player_hp -= self.damages
                self.game_mode.on_add_damages_to_player()
                enemies.remove(self)

                self.game_object.mark_to_destroy = True
                #pass
                #print("end")
            else:
                self.t = 0.0
                start_pos = self.path_coords[self.coord_index]
                self.start_coords = get_tile_coords(start_pos[0], start_pos[1])
                self.coord_index += 1
        else:
            target_pos = self.path_coords[self.coord_index]
            target_coords = get_tile_coords(target_pos[0], target_pos[1])
            self.game_object.set_pos(math_utils.lerp(
                self.start_coords,
                target_coords,
                self.t
            ))
            self.dynamic_sprite.z_pos = self.game_object.pos[1] + 100

        if self.slow_down_timer > 0.0:
            self.slow_down_timer -= dt
        elif self.speed != self.definition.speed:
            self.speed = self.definition.speed

        self.update_sprite()