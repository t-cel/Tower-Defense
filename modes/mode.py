from game_object import *
import ui.ui

# MODE_MENU   = 0
MODE_GAME   = 0
MODE_EDITOR = 1

modes = []
current_mode = -1

def switch_mode(mode):
    global current_mode

    # if current_mode != -1:
    #     modes[current_mode].deinit_mode()

    for game_object in game_objects:
        game_object.mark_to_destroy = True

    ui.ui.ui_manager.clear_and_reset()

    current_mode = mode
    modes[current_mode].init_mode()

"""
    Base class for switching game functionalities
"""
class Mode:

    def init_mode(self):
        pass

    def deinit_mode(self):
        pass