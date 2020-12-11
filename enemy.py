from map import *
from dynamic_sprite import DynamicSprite
from component import Component
from static_sprite import StaticSprite

import math_utils
import json

enemies = []
enemies_definitions = []

class EnemyDefinition:
    def __init__(self, name, sprites_directory, speed, health, damages, preview_sprite):
        self.name = name
        self.sprites_directory = sprites_directory
        self.speed = speed
        self.health = health
        self.damages = damages
        self.preview_sprite = preview_sprite

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
                enemy_definition["previewSprite"]
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
        self.hp_bar = None

        self.dynamic_sprite = None
        self.last_x = 0.0
        self.moving_reversed = False

        enemies.append(self)

    def init_component(self, **kwargs):
        self.path_coords = kwargs.get("path_coords")

        self.hp_bar = self.game_object.get_components(StaticSprite)[-1]
        self.hp_bar.change_activity(False)

        self.dynamic_sprite = self.game_object.get_components(DynamicSprite)[0]

    def take_damage(self, damage):
        print(self.hp)
        self.hp -= damage

        if not self.game_object.mark_to_destroy:
            if self.hp <= 0:
                self.hp = 0
                enemies.remove(self)
                self.game_object.mark_to_destroy = True

            # update hp bar
            new_width = int(TILE_SIZE * (self.hp / 100.0))
            self.hp_bar.set_size((new_width, TILE_SIZE))
            self.hp_bar.set_pos((TILE_SIZE / 2 - new_width / 2, -TILE_SIZE * 0.65))
            self.hp_bar.change_activity(True)

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
        self.t += self.speed * dt

        if self.t > 0.99:
            if self.coord_index == len(self.path_coords) - 1:
                pass
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

        self.update_sprite()