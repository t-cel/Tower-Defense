from ui.ui import *
from modes.mode import *

class LevelEndWindow(UIWindow):

    def __init__(self, player_won : bool, game_mode):
        w = 400
        h = 500

        super().__init__(
            pygame.Rect(
                SCREEN_WIDTH * 0.5 - w * 0.5,
                SCREEN_HEIGHT * 0.5 - h * 0.5,
                w,
                h,
            ),
            ui_manager,
            resizable=False
        )

        header_panel = UIPanel(
            pygame.Rect(-5, -5, w, 50),
            starting_layer_height=4,
            manager=ui_manager,
            container=self,
            object_id="#thicker_panel"
        )

        UITextBox(
            "<b><font size=5>You Won!</font></b>" if player_won else "<b><font size=5>You Lose...</font></b>",
            pygame.Rect(w/3.0, 5, 300, 50),
            ui_manager,
            container=header_panel,
            object_id="#no_border_textbox",
        )

        anchors = {
            'left': 'left',
            'right': 'right',
            'top': 'bottom',
            'bottom': 'bottom'
        }

        self.game_mode = game_mode

        replay_btn = UIButton(pygame.Rect(0,              -30, w / 3.25, 30), "Replay",       ui_manager, container=self, anchors=anchors)
        back_btn = UIButton(pygame.Rect(w / 3.25,         -30, w / 3.25, 30), "Back to Menu", ui_manager, container=self, anchors=anchors)
        next_btn = UIButton(pygame.Rect((w / 3.25) * 2.0, -30, w / 3.25, 30), "Next",         ui_manager, container=self, anchors=anchors)

        register_ui_callback(replay_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: game_mode.replay_map())
        register_ui_callback(back_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: switch_mode(MODE_MENU))
        register_ui_callback(next_btn, pygame_gui.UI_BUTTON_PRESSED, lambda e: game_mode.play_next_map())

        self.set_blocking(True)