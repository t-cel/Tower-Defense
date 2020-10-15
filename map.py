from definitions import *

# map
TILE_SIZE = 64
TILE_MARGIN = 0
MAP_W_HALF = 10
MAP_H_HALF = 5
MAP_CENTER_X = int(SCREEN_WIDTH / 2)
MAP_CENTER_Y = int(SCREEN_HEIGHT / 2) - TILE_SIZE / 2

def get_tile_coords(x, y):
    return MAP_CENTER_X - (MAP_W_HALF * (TILE_SIZE + TILE_MARGIN)) + x * (TILE_SIZE + TILE_MARGIN),\
           MAP_CENTER_Y - (MAP_H_HALF * (TILE_SIZE + TILE_MARGIN)) + y * (TILE_SIZE + TILE_MARGIN)

def get_tile_pos(coord_x, coord_y):
    return int((coord_x - (MAP_CENTER_X - MAP_W_HALF * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)), \
           int((coord_y - (MAP_CENTER_Y - MAP_H_HALF * (TILE_SIZE + TILE_MARGIN))) / (TILE_SIZE + TILE_MARGIN)),