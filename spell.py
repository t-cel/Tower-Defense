from component import Component
from circle import Circle
from dynamic_sprite import DynamicSprite
from dynamic_sprite import AnimationState
from map import *

import json
import pygame
import file_utils
import math_utils
import enemy
import math

spells_definitions = []

class SpellDefinition:
    def __init__(self, name, sprites_dir, animation_states, icon_image, effect_type,
                 sound, param, lifetime, duration, range, research_cost, use_cost):
        self.name = name
        self.sprites_dir = sprites_dir
        self.animation_states = animation_states
        self.icon_image = icon_image
        self.effect_type = effect_type
        self.sound = sound
        self.param = param
        self.lifetime = lifetime
        self.duration = duration
        self.range = range
        self.research_cost = research_cost
        self.use_cost = use_cost


def load_spells_definitions():
    f = open(DEFINITIONS_PATH + "spells.json")
    data = json.load(f)
    for spell_definition in data["spells"]:

        animation_states = []
        if "animationStates" in spell_definition:
            for animation_state in spell_definition["animationStates"]:
                animation_states.append(
                    AnimationState(
                        animation_state["transitionType"],
                        animation_state["frameStart"],
                        animation_state["frameEnd"]
                    )
                )

        spells_definitions.append(
            SpellDefinition(
                spell_definition["name"],
                spell_definition["spritesDirectory"],
                animation_states,
                spell_definition["iconImage"],
                spell_definition["effectType"],
                spell_definition["sound"],
                spell_definition["param"],
                spell_definition["lifetime"],
                spell_definition["duration"],
                spell_definition["range"],
                spell_definition["researchCost"],
                spell_definition["useCost"]
            )
        )


def make_description(spell_definition):

    dmg_color_start = "<font color=#BB0000><b>"
    range_color_start = "<font color=#9141D1><b>"
    duration_color_start = "<font color=#00FF00><b>"
    gold_color_start = "<font color=#DEAF21><b>"
    use_cost_color_start = "<font color=#4488FF><b>"

    color_end = "</b></font>"

    description = {
        "damage" : f"Deals {dmg_color_start}{spell_definition.param} damages{color_end} to enemies "
                   f"in range of: {range_color_start}{spell_definition.range} units{color_end}.<br>"
                   f"Damage decreases with distance.",

        "slowdown" : f"Slows down enemies by {dmg_color_start}{spell_definition.param}%{color_end} "
                     f"in range of: {range_color_start}{spell_definition.range} units{color_end} "
                     f"for {duration_color_start}{spell_definition.duration} seconds{color_end}"

    }[spell_definition.effect_type]

    if spell_definition.lifetime > 1.0:
        description += f"<br>Lasts {duration_color_start}{spell_definition.lifetime} seconds{color_end}"

    description += "<br><br>"

    description += f"{gold_color_start}Research cost: {color_end}{spell_definition.research_cost} Gold<br><br>"
    description += f"{use_cost_color_start}Use cost: {color_end}{spell_definition.use_cost} Mana"

    return description


class Spell(Component):
    def __init__(self, game_object):

        super().__init__(game_object)

        self.definition = None
        self.game_mode = None
        self.range_circle = None
        self.sprite = None

        self.t = 0.0

        self.effect_timer = 0.0

        self.select_target_mode = True
        self.current_pos_is_valid = False

        self.last_valid_map_pos = (-5, 0)
        self.map_pos = self.last_valid_map_pos
        self.enemies_path_coords = None

        self.effect_sound = None


    def init_component(self, **kwargs):

        super().init_component(**kwargs)

        self.definition = kwargs.get("definition")
        self.game_mode = kwargs.get("game_mode")
        self.enemies_path_coords = kwargs.get("enemies_path_coords")

        self.range_circle = self.game_object.get_components(Circle)[0]
        self.range_circle.radius = self.definition.range * TILE_SIZE

        """
        self.game_object.add_component(DynamicSprite).init_component(
            pos=(   -(TILE_SIZE * self.definition.range)*0.75,  -(TILE_SIZE * self.definition.range)*0.75),
            size=(int(TILE_SIZE * self.definition.range * 2), int(TILE_SIZE * self.definition.range * 2)),
            angle=0,
            images_paths=file_utils.get_all_files_in_path(EFFECTS_PATH + self.definition.sprites_dir),
            alpha=True,
            speed=0.3
        )
        """

        self.effect_sound = pygame.mixer.Sound(SOUNDS_PATH + self.definition.sound + ".ogg")
        self.effect_sound.set_volume(0.5)


    def valid_map_pos(self, map_pos):

        # paths
        for coord in self.enemies_path_coords:
            if coord[0] == map_pos[0] and coord[1] == map_pos[1]:
                return True

        return False


    def update_drag(self):

        target_pos = pygame.mouse.get_pos()
        self.map_pos = get_tile_pos(target_pos[0], target_pos[1])

        if not self.valid_map_pos(self.map_pos):
            self.map_pos = self.last_valid_map_pos
            self.current_pos_is_valid = False
        else:
            self.current_pos_is_valid = True

        target_pos = get_tile_coords(self.map_pos[0], self.map_pos[1])
        self.last_valid_map_pos = self.map_pos

        self.game_object.set_pos(target_pos)


    def update(self, dt):

        if not self.select_target_mode:
            self.t += dt

            if self.t >= self.definition.lifetime:
                self.game_object.mark_to_destroy = True
            else:
                # switch state to finish one for effects that have them
                if len(self.definition.animation_states) >= 0 and self.t >= self.definition.lifetime - 0.5:
                    self.sprite.switch_state(2)

                if self.effect_timer <= 0.0:
                    self.effect_timer = 1.0
                    self.play_effects()

                self.effect_timer -= dt
        else:
            self.update_drag()


    def process_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and self.select_target_mode and self.current_pos_is_valid:
            self.game_object.add_component(DynamicSprite).init_component(
                pos=(-(TILE_SIZE * self.definition.range) * 0.75, -(TILE_SIZE * self.definition.range) * 0.75),
                size=(int(TILE_SIZE * self.definition.range * 2), int(TILE_SIZE * self.definition.range * 2)),
                angle=0,
                images_paths=file_utils.get_all_files_in_path(EFFECTS_PATH + self.definition.sprites_dir),
                alpha=True,
                speed=0.3,
                looping=False,
                z_pos=900,
                animation_states=self.definition.animation_states
            )

            self.sprite = self.game_object.get_components(DynamicSprite)[0]

            self.range_circle.change_activity(False)
            self.select_target_mode = False
            self.game_mode.on_cast_spell_end()
            self.effect_sound.play()


    def play_effects(self):

        sqr_r = self.range_circle.radius * self.range_circle.radius
        for e in enemy.enemies:
            sqr_dist = math_utils.sqr_magnitude(self.game_object.pos, e.get_target_pos())

            if sqr_dist <= sqr_r:
                if self.definition.effect_type == "damage":
                    e.take_damage(self.definition.param * (1.0 - (sqr_dist / sqr_r)))
                elif self.definition.effect_type == "slowdown":
                    e.slow_down(self.definition.duration, 1.0 - self.definition.param / 100.0)

