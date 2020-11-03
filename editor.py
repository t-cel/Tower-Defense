from map import *
from game_object import GameObject
from ui.ui import *

from pygame_gui.elements.ui_button import UIButton

import pygame
import pygame_gui

path_indicators = []
remove_btn = None

PATH_INDICATOR_DIR_LEFT  = 0
PATH_INDICATOR_DIR_RIGHT = 1
PATH_INDICATOR_DIR_UP    = 2
PATH_INDICATOR_DIR_DOWN  = 3

gui_manager = None

def init_editor(_gui_manager):
    global gui_manager
    gui_manager = _gui_manager

def add_enemy_path_indicator(x, y, indicator_dir):
    pos = get_tile_coords(x, y)
    pos = list(pos)
    pos[0] = pos[0] + TILE_SIZE / 4 if indicator_dir == PATH_INDICATOR_DIR_UP or indicator_dir == PATH_INDICATOR_DIR_DOWN else \
             pos[0] + TILE_SIZE if indicator_dir == PATH_INDICATOR_DIR_RIGHT else \
             pos[0] - TILE_SIZE / 2

    pos[1] = pos[1] + TILE_SIZE / 4 if indicator_dir == PATH_INDICATOR_DIR_LEFT or indicator_dir == PATH_INDICATOR_DIR_RIGHT else \
             pos[1] + TILE_SIZE if indicator_dir == PATH_INDICATOR_DIR_DOWN else \
             pos[1] - TILE_SIZE / 2

    new_path_part_offsets = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    indicators_ids = [
        "#path_indicator_left",
        "#path_indicator_right",
        "#path_indicator_up",
        "#path_indicator_down",
    ]

    new_indicator = UIButton(
        pygame.Rect(pos[0], pos[1], TILE_SIZE/2, TILE_SIZE/2),
        "",
        ui_manager,
        object_id=indicators_ids[indicator_dir]
    )
    register_ui_callback(
        new_indicator,
        pygame_gui.UI_BUTTON_PRESSED,
        lambda _pos=(x, y): add_enemy_path_part(_pos[0] + new_path_part_offsets[indicator_dir][0],
                                                _pos[1] + new_path_part_offsets[indicator_dir][1]),
    )

    """
    new_indicator = GameObject(pos, (1, 1), 0)
    new_indicator.add_component(Button).init_component(
        size=(TILE_SIZE / 2, TILE_SIZE / 2),
        callback=lambda _pos=(x, y): add_enemy_path_part(_pos[0] + new_path_part_offsets[indicator_dir][0],
                                                         _pos[1] + new_path_part_offsets[indicator_dir][1]),
        gui_manager=gui_manager,
        object_id=indicators_ids[indicator_dir]
    )
    """
    path_indicators.append(new_indicator)

def add_remove_button(x, y):
    pos = get_tile_coords(x, y)
    pos = list(pos)

    pos[0] += TILE_SIZE / 4
    pos[1] += TILE_SIZE / 4

    """
    remove_btn = GameObject(pos, (1, 1), 0)
    remove_btn.add_component(Button).init_component(
        size=(TILE_SIZE / 2, TILE_SIZE / 2),
        callback=lambda: remove_enemy_path_last_point(),
        gui_manager=gui_manager,
        object_id="#remove_btn"

    )
    """
    remove_btn = UIButton(
        pygame.Rect(pos[0], pos[1], TILE_SIZE / 2, TILE_SIZE / 2),
        "",
        ui_manager,
        object_id="#remove_btn"
    )

    register_ui_callback(
        remove_btn,
        pygame_gui.UI_BUTTON_PRESSED,
        lambda: remove_enemy_path_last_point()
    )

    path_indicators.append(remove_btn)

def add_enemy_path_part(x, y):
    enemies_path_coords = get_path_coords()
    enemies_path_coords.append((x, y))

    update_indicators()
    update_path()

def update_indicators():
    enemies_path_coords = get_path_coords()

    # remove old and make new path indicators
    # for indicator in path_indicators:
    #     indicator.mark_to_destroy = True
    for indicator in path_indicators:
        indicator.kill()
        unregister_ui_callback(indicator, pygame_gui.UI_BUTTON_PRESSED)
    path_indicators.clear()

    x, y = enemies_path_coords[-1]

    if len(enemies_path_coords) > 1:
        if enemies_path_coords[-1][0] + 1 != enemies_path_coords[-2][0] and x < MAP_W-1:
            add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_RIGHT)

        if enemies_path_coords[-1][0] - 1 != enemies_path_coords[-2][0] and x > 0:
            add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_LEFT)

        if enemies_path_coords[-1][1] - 1 != enemies_path_coords[-2][1] and y > 0:
            add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_UP)

        if enemies_path_coords[-1][1] + 1 != enemies_path_coords[-2][1] and y < MAP_H-1:
            add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_DOWN)

        add_remove_button(x, y)
    else:
        add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_RIGHT)
        add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_DOWN)
        add_enemy_path_indicator(x, y, PATH_INDICATOR_DIR_UP)

def remove_enemy_path_last_point():

    enemies_path = get_path()
    enemies_path_coords = get_path_coords()

    enemies_path[-1].mark_to_destroy = True
    enemies_path.remove(enemies_path[-1])
    enemies_path_coords.remove(enemies_path_coords[-1])

    update_indicators()
    update_path()