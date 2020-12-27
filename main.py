from pygame.locals import *
from definitions import *
from modes.mode import *

# pygame needs to be init before ui initialization
pygame.init()

# set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tower Defender')

from ui.ui import *
from modes.game_mode import GameMode
from modes.editor_mode import EditorMode
from modes.menu_mode import MenuMode
from modes.select_level_mode import SelectLevelMode
import enemy
import tower

def preload_assets():

    enemy.load_enemies_definitions()
    tower.load_towers_definitions()

    # preload enemies sprites
    for enemy_definition in enemy.enemies_definitions:
        resource_cache.add_resource(
            file_utils.get_all_files_in_path(ENEMIES_PATH + enemy_definition.sprites_directory, ".png"),
            resource_cache.ImagesPack,
            alpha=True
        )

        resource_cache.add_resource(
            file_utils.get_all_files_in_path(ENEMIES_PATH + enemy_definition.sprites_directory + "/reversed", ".png"),
            resource_cache.ImagesPack,
            alpha=True
        )

def main():
    preload_assets()

    # init modes
    modes.append(MenuMode())
    modes.append(SelectLevelMode())
    modes.append(GameMode())
    modes.append(EditorMode())

    # select start mode
    # switch_mode(MODE_EDITOR)
    switch_mode(MODE_GAME, file_name="nowa_mapa.tdmap")

    # main loop
    last_frame_ticks = 0
    running = True
    while running:
        # print(len(ui_callbacks))

        t = pygame.time.get_ticks()
        delta_time = (t - last_frame_ticks) / 1000.0

        # print(delta_time)

        # process events
        for event in pygame.event.get():
            # print("event in main")
            if event.type is QUIT:
                running = False

            ui_manager.process_events(event)

            for game_object in game_objects:
                for component in game_object.components:
                    component.process_event(event)

            # check ui callbacks
            if event.type == pygame.USEREVENT:
                # print(f"checking callbacks: {len(ui_callbacks)}")
                for callback in ui_callbacks:

                    if not callback[0]:
                        # print("cleaning unused event")
                        ui_callbacks.remove(callback)
                        continue

                    if callback[0] == event.ui_element and callback[1] == event.user_type:
                        callback[2](event)

        # update ui manager
        ui_manager.update(delta_time)

        # clear screen
        screen.blit(background, (0, 0))

        # update components and render all items
        renderables = []
        for game_object in game_objects:

            # destroy objects marked to destroy
            if game_object.mark_to_destroy:
                game_object.destroy()
                game_objects.remove(game_object)
                continue

            # update components
            for component in game_object.components:
                if component.enabled:
                    component.update(delta_time)

            # render renderables
            for renderable in game_object.get_components(Renderable):
                if renderable.enabled:
                    renderables.append(renderable)

        # sort renderables by their z position
        renderables.sort(key = lambda renderable: renderable.z_pos)
        for renderable in renderables:
            renderable.render(screen)

        # draw ui last
        ui_manager.draw_ui(screen)
        # pygame.time.delay(int(1000.0 / 60.0))
        pygame.display.update()
        last_frame_ticks = t

    pygame.quit()


if __name__ == "__main__":
    main()