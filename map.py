from definitions import *
from game_object import GameObject
from static_sprite import StaticSprite

# map
TILE_SIZE = 76
TILE_MARGIN = 0
MAP_W_HALF = 10
MAP_H_HALF = 5
MAP_CENTER_X = int(SCREEN_WIDTH / 2)
MAP_CENTER_Y = int(SCREEN_HEIGHT / 2) - TILE_SIZE / 2

# path
enemies_path = []
enemies_path_coords = []

def get_tile_coords(x, y):
    return MAP_CENTER_X - (MAP_W_HALF * (TILE_SIZE + TILE_MARGIN)) + x * (TILE_SIZE + TILE_MARGIN),\
           MAP_CENTER_Y - (MAP_H_HALF * (TILE_SIZE + TILE_MARGIN)) + y * (TILE_SIZE + TILE_MARGIN)

def get_tile_pos(coord_x, coord_y):
    return int((coord_x - (MAP_CENTER_X - MAP_W_HALF * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)), \
           int((coord_y - (MAP_CENTER_Y - MAP_H_HALF * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)),

# update path graphics, remove old and make new
def update_path():
    # remove old
    global enemies_path
    for point in enemies_path:
        point.mark_to_destroy = True
    enemies_path = []

    global enemies_path_coords

    # make horizontal path
    new_path_part = GameObject(get_tile_coords(enemies_path_coords[0][0], enemies_path_coords[0][1]), (1, 1), 0)
    new_path_part.add_component(StaticSprite).init_component(
        pos=(0, 0),
        size=(TILE_SIZE, TILE_SIZE),
        angle=0,
        image_path=MAP_PATH + 'road_straight.png',
        alpha=True,
    )
    enemies_path.append(new_path_part)

    if len(enemies_path_coords) > 1:
        for i in range(1, len(enemies_path_coords)):
            curr_pos = enemies_path_coords[i]
            curr_coords = get_tile_coords(curr_pos[0], curr_pos[1])
            if i < len(enemies_path_coords) - 1:
                prev_pos = enemies_path_coords[i-1]
                next_pos = enemies_path_coords[i+1]

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
                if enemies_path_coords[i - 1][0] == enemies_path_coords[i][0]:
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
