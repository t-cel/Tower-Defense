from game_object import *

MODE_MENU         = 0
MODE_SELECT_LEVEL = 1
MODE_GAME         = 2
MODE_EDITOR       = 3

modes = []
current_mode = -1

def switch_mode(mode, **kwargs):
    global current_mode

    if current_mode != -1:
         modes[current_mode].deinit_mode()

    for game_object in game_objects:
        game_object.mark_to_destroy = True

    import ui.ui
    ui.ui.ui_manager.clear_and_reset()
    ui.ui.ui_callbacks.clear()

    current_mode = mode
    modes[current_mode].init_mode(**kwargs)

"""
    Base class for switching game functionalities
"""
class Mode:

    def init_mode(self, **kwargs):
        pass

    def deinit_mode(self):
        pass