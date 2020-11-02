import sys
from pygame.locals import *
import pygame_gui
import random
import resource_cache

from game_object import *
from enemy import *
from dynamic_sprite import *
from button import *
from tower import Tower
from circle import Circle
from tile import Tile

import file_utils
import editor

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gra Fakultet')

#gui_resource_loader = pygame_gui.core.IncrementalThreadedResourceLoader()
gui_manager = pygame_gui.UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame_gui.PackageResource(package="sources.themes", resource="ui_theme.json")
)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(gui_manager.ui_theme.get_colour('dark_bg'))

def spawn_enemy():
    # create test enemy
    enemy_object = GameObject(
        get_tile_coords(enemies_path_coords[0][0] - 1, enemies_path_coords[0][1]),
        (1, 1),
        0
    )

    rand_enemy = 1 + random.randrange(3)
    enemy_object.add_component(DynamicSprite).init_component(
        pos = (0, -TILE_SIZE/4),
        size = (TILE_SIZE, TILE_SIZE),
        angle = 0,
        images_paths = file_utils.get_all_files_in_path(ENEMIES_PATH + str(rand_enemy)),
        alpha = True
    )

    enemy_object.add_component(DynamicSprite).init_component(
        pos = (0, -TILE_SIZE/4),
        size = (TILE_SIZE, TILE_SIZE),
        angle = 0,
        images_paths = file_utils.get_all_files_in_path(ENEMIES_PATH + str(rand_enemy) + "/reversed"),
        alpha = True
    )
    enemy_object.get_components(DynamicSprite)[1].change_activity(False)

    '''
    hp_bar = enemy_object.add_component(StaticSprite)
    hp_bar.init_component(
        pos = (250, -20),
        size = (50, 5),
        angle = 0,
        image_path = ENEMIES_PATH + "hp_bar.jpg",
        z_pos = 800
    )
    '''

    enemy_object.add_component(StaticSprite).init_component(
        pos=(250, -20),
        size=(TILE_SIZE, TILE_SIZE),
        angle=0,
        image_path=ENEMIES_PATH + "hp_bar.png",
        z_pos=800,
        alpha=True
    )

    enemy_object.add_component(Enemy).init_component(
        path_coords = enemies_path_coords,
    )

def spawn_tower():
    # test tower
    tower_object = GameObject(
        get_tile_coords(3, 0),
        (1, 1),
        0
    )

    tower_object.add_component(StaticSprite).init_component(
        pos=(0, 0),
        size = (TILE_SIZE, TILE_SIZE),
        angle = 0,
        image_path = TOWERS_PATH + '1.png',
        alpha = True
    )

    tower_object.add_component(Circle).init_component(
        pos=(0, 0),
        radius=TILE_SIZE * 2,
        color=(25, 25, 225, 200),
        thickness=1
    )

    tower_object.add_component(Tower).init_component(
        enemies_path_coords = enemies_path_coords
    )

def preload_assets():

    # preload enemies sprites
    for i in range(1, 4):
        resource_cache.add_resource(
            file_utils.get_all_files_in_path(ENEMIES_PATH + str(i)),
            resource_cache.ImagesPack,
            alpha=True
        )

        resource_cache.add_resource(
            file_utils.get_all_files_in_path(ENEMIES_PATH + str(i) + "/reversed"),
            resource_cache.ImagesPack,
            alpha=True
        )

def init_gui():
    # fall label
    label = pygame_gui.elements.ui_label.UILabel(
        pygame.Rect(int(SCREEN_WIDTH / 2), 10, 100, 25),
        "Fala: 1",
        manager = gui_manager
    )

    # test spawn enemy button
    button_object = GameObject(
        (25, SCREEN_HEIGHT - 100),
        (1, 1),
        0
    )

    button_object.add_component(Button).init_component(
        size = (150, 40),
        text = 'Spawn Enemy',
        callback = lambda: spawn_enemy(),
        gui_manager = gui_manager
    )

    # test tower button
    button_object2 = GameObject(
        (25 + 150 + 25, SCREEN_HEIGHT - 100),
        (1, 1),
        0
    )

    button_object2.add_component(Button).init_component(
        size = (150, 40),
        text = 'Tower 1',
        callback = lambda: spawn_tower(),
        gui_manager = gui_manager,
        #tool_tip_text = "<font face=Montserrat color=#000000 size=2>"
        #                    "<font color=#FFFFFF>Adds tower</font>"
        #                "</font>",
        #object_id = "#test_btn"
    )

def main():
    preload_assets()

    # ui
    #gui_manager.add_font_paths("Montserrat", FONTS_PATH)
    #gui_manager.preload_fonts([
    #    {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
    #    {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
    #    {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
    #    {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
    #])

    '''
    gui_resource_loader.start()
    finished_loading = False
    while not finished_loading:
        finished_loading = gui_resource_loader.update()
    #print("loaded fonts")
    '''
    init_gui()

    # create tiles
    for x in range(0, MAP_W_HALF*2):
        for y in range(0, MAP_H_HALF*2):
            tile_object = GameObject(
                get_tile_coords(x, y),
                (1, 1),
                90 * random.randrange(4)
            )

            tile_object.add_component(StaticSprite).init_component(
                pos=(0, 0),
                size=(TILE_SIZE, TILE_SIZE),
                angle=0,
                image_path= MAP_PATH + 'grass4.png',
                alpha=False,
                clone=True
            )

            tile_object.add_component(Tile).init_component(
                available = x == 0
            )

            #debug
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

    editor.init_editor(gui_manager)
    # start path indicators
    for y in range(0, MAP_H_HALF*2):
        editor.add_enemy_path_indicator(-1, y, editor.PATH_INDICATOR_DIR_RIGHT)

    # main loop
    last_frame_ticks = 0
    running = True
    while running:
        t = pygame.time.get_ticks()
        delta_time = (t - last_frame_ticks) / 1000.0

        for event in pygame.event.get():
            # print("event in main")
            if event.type is QUIT:
                running = False
            gui_manager.process_events(event)
            for game_object in game_objects:
                for component in game_object.components:
                    component.process_event(event)

        gui_manager.update(delta_time)

        screen.blit(background, (0, 0))
        # update and render all items
        renderables = []
        for game_object in game_objects:

            if game_object.mark_to_destroy:
                game_object.destroy()
                game_objects.remove(game_object)
                continue

            for component in game_object.components:
                if component.enabled:
                    component.update(delta_time)

            for renderable in game_object.get_components(Renderable):
                if renderable.enabled:
                    renderables.append(renderable)

        renderables.sort(key = lambda renderable: renderable.z_pos)
        for renderable in renderables:
            renderable.render(screen)

        gui_manager.draw_ui(screen)
        # pygame.time.delay(int(1000.0 / 60.0))
        pygame.display.update()
        last_frame_ticks = t

    pygame.quit()

    # todo:
    #  - przenieść funkcje edytora / mapy do osobnej klasy / pliku
    #  - zmienić sposób wystrzeliwania pocisków: niech wieże "przewidują"
    #    w czasie "cooldown" gdzie będzie przeciwnik, i strzelały tam pocisk

if __name__ == "__main__":
    main()