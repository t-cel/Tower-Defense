import sys
from pygame.locals import *
import pygame_gui
import random
import resource_cache

from game_object import *
from enemy_path import *
from enemy import *
from dynamic_sprite import *
from button import *
from tower import Tower
from circle import Circle

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gra Fakultet')

gui_resource_loader = pygame_gui.core.IncrementalThreadedResourceLoader()
gui_manager = pygame_gui.UIManager(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    THEMES_PATH + "quick_theme.json",
    resource_loader = gui_resource_loader
)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(gui_manager.ui_theme.get_colour('dark_bg'))

# path
enemies_paths = [
    EnemyPath(True, [(0, 7), (1, 7), (2, 7), (3, 7)]),
    EnemyPath(False, [(4, 7), (4, 6), (4, 5), (4, 4), (4, 3)]),
    EnemyPath(True, [(4, 2), (5, 2), (6, 2), (7, 2)]),
    EnemyPath(False, [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)]),
    EnemyPath(True, [(8, 8)]),
    EnemyPath(False, [(9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2)]),
    EnemyPath(True, [(9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1)]),
    EnemyPath(False, [(14, 2), (14, 3), (14, 4), (14, 5), (14, 6)]),
    EnemyPath(True, [(15, 6), (16, 6), (17, 6), (18, 6), (19, 6)])
]

def spawn_enemy():
    # create test enemy
    enemy_object = GameObject(
        get_tile_coords(-2, 7),
        (1, 1),
        0
    )

    enemy_object.add_component(DynamicSprite).init_component(
        pos = (0, 0),
        size = (TILE_SIZE, TILE_SIZE),
        angle = 0,
        images_paths = get_all_files_in_path(ENEMIES_PATH + str(1 + random.randrange(3))),
        alpha = True
    )

    hp_bar = enemy_object.add_component(StaticSprite)
    hp_bar.init_component(
        pos = (TILE_SIZE / 2 - 25, -6),
        size = (50, 5),
        angle = 0,
        image_path = ENEMIES_PATH + "hp_bar.jpg",
        z_pos = 800
    )

    enemy_object.add_component(Enemy).init_component(
        enemies_paths = enemies_paths,
        hp_bar = hp_bar
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
        color=(100, 0, 0),
        thickness=2
    )

    tower_object.add_component(Tower).init_component(
        enemies_paths = enemies_paths
    )

def preload_assets():

    # preload enemies sprites
    for i in range(1, 4):
        resource_cache.add_resource(
            get_all_files_in_path(ENEMIES_PATH + str(i)),
            resource_cache.ImagesPack,
            alpha = True
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
        gui_manager = gui_manager
    )

def main():
    preload_assets()
    init_gui()

    # ui
    gui_manager.add_font_paths("Montserrat", FONTS_PATH)
    gui_manager.preload_fonts([
        {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
        {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
        {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
        {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
        {'name': 'fira_code', 'html_size': 2, 'style': 'regular'},
    ])

    # load enemies sprites
    for i in range(1, 3):
        all_frames = get_all_files_in_path(ENEMIES_PATH + str(i))
        frame_index = 0
        for frame in all_frames:
            gui_resource_loader.add_resource(pygame_gui.core.utility.ImageResource(
                'enemy_' + str(i) + '_' + str(frame_index),
                frame
            ))
            frame_index += 1

    #some threads seem to still work after loading
    #gui_resource_loader.start()
    #finished_loading = False
    #while not finished_loading:
    #    finished_loading = gui_resource_loader.update()
    #print("loaded fonts")

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
                image_path= MAP_PATH + 'grass1.jpg',
                alpha=False,
                clone=True
            )

    # create paths
    for path in enemies_paths:
        for coord in path.coords:
            tile_coords = list(get_tile_coords(coord[0], coord[1]))
            if path.is_horizontal:
                tile_coords[1] = tile_coords[1] + int(TILE_SIZE / 2)

            tile_object = GameObject(
                tile_coords,
                (1, 1),
                0
            )

            tile_object.add_component(StaticSprite).init_component(
                pos=(0, 0),
                size=(TILE_SIZE, int(TILE_SIZE / 2) if path.is_horizontal else TILE_SIZE),
                angle=0,
                image_path= MAP_PATH + 'grass2.jpg',
                alpha=False
            )

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

            if game_object.destroy:
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

        #pygame.draw.circle(screen, (100, 0, 0), (300, 300), 60, 2)
        # todo: klasa bazowa dla obiektow rysowalnych (Renderable), aby móc rysować np okręgi i dodawać je
        # todo: jako komponenty, wtedy pętla obiektów musi wybierac komponenty dziedziczące po Renderable.

        # todo: priorytet / pozycja z rysowanych obiektów, obiekty powinny być sortowane co klatkę względem
        # todo: tej wartości, dla jednostek musi ona być liczona uwzględniając ich bazową pozycję która powinna
        # todo: być nad wszystkim, oraz, jeśli są na ścieżce wertykalnej, ich aktualny postęp w niej.

        gui_manager.draw_ui(screen)
        # pygame.time.delay(int(1000.0 / 60.0))
        pygame.display.update()
        last_frame_ticks = t

    pygame.quit()

if __name__ == "__main__":
    main()