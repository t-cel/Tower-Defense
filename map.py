from definitions import *
from game_object import GameObject
from static_sprite import StaticSprite

import random
import pickle

#from map_settings import *
import map_settings
import player_stats

# map
TILE_SIZE = int(80 * X_RATIO)
TILE_MARGIN = 0
MAP_W = 16
MAP_H = 11
#MAP_CENTER_X = int(SCREEN_WIDTH / 2)
MAP_CENTER_X = (MAP_W / 2.0) * TILE_SIZE
#MAP_CENTER_Y = int(SCREEN_HEIGHT / 2) - (TILE_SIZE / 4)
MAP_CENTER_Y = 30 + (MAP_H / 2.0) * TILE_SIZE

# path
enemies_path = []
#enemies_path_coords = []
#settings = get_settings()

"""
    returns tile screen position based on map coordinates
"""
def get_tile_coords(x, y):
    return MAP_CENTER_X - ((MAP_W / 2.0) * (TILE_SIZE + TILE_MARGIN)) + x * (TILE_SIZE + TILE_MARGIN),\
           MAP_CENTER_Y - ((MAP_H / 2.0) * (TILE_SIZE + TILE_MARGIN)) + y * (TILE_SIZE + TILE_MARGIN)


"""
    returns tile position on map based on screen coordinates
"""
def get_tile_pos(coord_x, coord_y):
    return int((coord_x - (MAP_CENTER_X - (MAP_W / 2.0) * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)), \
           int((coord_y - (MAP_CENTER_Y - (MAP_H / 2.0) * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)),


"""
    returns list of 2-element tuples representing path coordinates (x, y)
"""
def get_path_coords():
    return map_settings.settings.enemies_path_coords


"""
    returns list of game objects that path contains of
"""
def get_path():
    return enemies_path


"""
    update path graphics, remove old and make new
"""
def update_path():

    # remove old
    global enemies_path
    for point in enemies_path:
        point.mark_to_destroy = True
    enemies_path = []

    settings = map_settings.settings
    if len(settings.enemies_path_coords) == 0:
        return

    # temporarly add "offseted" coordinate to properly begin path
    settings.enemies_path_coords = [(-1, settings.enemies_path_coords[0][1])] + settings.enemies_path_coords

    if len(settings.enemies_path_coords) > 1:
        for i in range(1, len(settings.enemies_path_coords)):
            curr_pos = settings.enemies_path_coords[i]
            curr_coords = get_tile_coords(curr_pos[0], curr_pos[1])
            if i < len(settings.enemies_path_coords) - 1:
                prev_pos = settings.enemies_path_coords[i-1]
                next_pos = settings.enemies_path_coords[i+1]

                if prev_pos[1] == curr_pos[1] == next_pos[1]:
                    # make horizontal path
                    new_path_part = GameObject(curr_coords, (1, 1), 0)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_straight.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                elif prev_pos[0] == curr_pos[0] == next_pos[0]:
                    # make vertical path
                    new_path_part = GameObject(curr_coords, (1, 1), 90)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_straight.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                elif (prev_pos[0] < curr_pos[0] and next_pos[0] == curr_pos[0] and next_pos[1] > curr_pos[1]) or \
                     (next_pos[0] < curr_pos[0] and prev_pos[0] == curr_pos[0] and prev_pos[1] > curr_pos[1]):
                    # make left-down path
                    new_path_part = GameObject(curr_coords, (1, 1), 90)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_corner.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                elif (prev_pos[0] < curr_pos[0] and next_pos[0] == curr_pos[0] and next_pos[1] < curr_pos[1]) or \
                     (next_pos[0] < curr_pos[0] and prev_pos[0] == curr_pos[0] and prev_pos[1] < curr_pos[1]):
                    # make left-up path
                    new_path_part = GameObject(curr_coords, (1, 1), 0)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_corner.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                elif (prev_pos[0] > curr_pos[0] and next_pos[0] == curr_pos[0] and next_pos[1] < curr_pos[1]) or \
                     (next_pos[0] > curr_pos[0] and prev_pos[0] == curr_pos[0] and prev_pos[1] < curr_pos[1]):
                    # make right-up path
                    new_path_part = GameObject(curr_coords, (1, 1), 270)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_corner.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                else:
                    # make right-down path
                    new_path_part = GameObject(curr_coords, (1, 1), 180)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_corner.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
            else:
                # continue path according to direction of last point
                if settings.enemies_path_coords[i - 1][0] == settings.enemies_path_coords[i][0]:
                    # make vertical path
                    new_path_part = GameObject(curr_coords, (1, 1), 90)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_straight.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)
                else:
                    # make horizontal path
                    new_path_part = GameObject(curr_coords, (1, 1), 0)
                    new_path_part.add_component(StaticSprite).init_component(
                        pos=(0, 0),
                        size=(TILE_SIZE, TILE_SIZE),
                        angle=0,
                        image_path=MAP_PATH + 'road_straight.png',
                        alpha=True,
                    )
                    enemies_path.append(new_path_part)

    # remove "offseted" coordinate
    settings.enemies_path_coords.pop(0)


"""
    loads .bin save
"""
def load_map(file_name):
    with open(MAPS_PATH + file_name, "rb") as file_handle:
        map_settings.settings = pickle.load(file_handle)

    update_path()

    """
        dummy settings
    """
    group_1_1 = map_settings.EnemiesGroup()
    group_1_1.enemies_counts = [ 0, 0, 1 ]
    group_1_1.spawn_delay = 0.0
    group_1_1.interval = (0.5, 0.5)

    group_1_2 = map_settings.EnemiesGroup()
    group_1_2.enemies_counts = [ 1, 0, 0 ]
    group_1_2.spawn_delay = 2.0
    group_1_2.interval = (0.5, 2.5)

    fall_1 = map_settings.EnemiesFall()
    fall_1.groups = [ group_1_1, group_1_2 ]
    fall_1.gold_reward = 200

    fall_2 = map_settings.EnemiesFall()
    fall_2.groups = [ group_1_1, group_1_1, group_1_2 ]
    fall_2.gold_reward = 500

    map_settings.settings.start_gold = 500
    map_settings.settings.falls = [ fall_1, fall_2 ]

    player_stats.player_gold = map_settings.settings.start_gold


"""
    saves map to .bin file
"""
def save_map(file_name):

    import ui.ui

    settings = map_settings.settings
    if len(settings.enemies_path_coords) < 1 or \
            (settings.enemies_path_coords[-1][0] != MAP_W - 1 and
             settings.enemies_path_coords[-1][1] != MAP_H - 1 and
             settings.enemies_path_coords[-1][1] != 0):
        ui.ui.show_message_box("<b><font face='verdana' color='#FF3333' size=3.5>"
                               "To save level you need to finish your path on right, bottom or top map edge."
                               "</font></b>")
        return

    with open(MAPS_PATH + file_name, "wb+") as file_handle:
        pickle.dump(settings, file_handle)


"""
    creates new empty map
"""
def create_map():
    # create tiles
    for x in range(0, MAP_W):
        for y in range(0, MAP_H):
            tile_object = GameObject(
                get_tile_coords(x, y),
                (1, 1),
                90 * random.randrange(4)
            )

            tile_object.add_component(StaticSprite).init_component(
                pos=(0, 0),
                size=(TILE_SIZE, TILE_SIZE),
                angle=0,
                image_path=MAP_PATH + 'grass4.png',
                alpha=False,
                clone=True
            )

            # debug
            '''
            debug_circle_object = GameObject(
                get_tile_coords(x, y),
                (1, 1),
                0
            )

            debug_circle_object.add_component(Circle).init_component(
                pos=(0, 0),
                radius=5,
                thickness=2
            )
            '''


def remove_enemy_path_last_point():
    settings = map_settings.settings

    enemies_path[-1].mark_to_destroy = True
    enemies_path.remove(enemies_path[-1])
    settings.enemies_path_coords.remove(settings.enemies_path_coords[-1])

    update_path()


def clear_map():
    settings = map_settings.settings

    while len(settings.enemies_path_coords) > 0:
        remove_enemy_path_last_point()
