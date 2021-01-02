from component import Component

import tower
import session_data
import map_settings
import definitions

class GameGUIUpdater(Component):

    def __init__(self, game_object):
        super().__init__(game_object)

        self.fall_label = None
        self.fall_reward_label = None
        self.gold_label = None
        self.tower_build_buttons = []

        self.enemies_spawner = None
        self.player_hp_bar = None
        self.enemies_fall_bar = None


    def init_component(self, **kwargs):
        self.fall_label = kwargs.get("fall_label")
        self.fall_reward_label = kwargs.get("fall_reward_label")
        self.gold_label = kwargs.get("gold_label")
        self.tower_build_buttons = kwargs.get("tower_build_buttons")
        self.enemies_spawner = kwargs.get("enemies_spawner")
        self.player_hp_bar = kwargs.get("player_hp_bar")
        self.enemies_fall_bar = kwargs.get("enemies_fall_bar")


    def update_stats_gui(self):
        self.gold_label.html_text = "<b><font color=#DEAF21>Gold: </font>" + str(session_data.player_gold) + "</b>";
        self.gold_label.rebuild()

        i = 0
        for btn in self.tower_build_buttons:
            if tower.tower_definitions[i].cost > session_data.player_gold:
                btn.disable()
            else:
                btn.enable()
            i += 1

        self.fall_label.html_text = "<b>Falls Finished:</b> " + \
                                    str(self.enemies_spawner.current_fall + 1) + " / " + \
                                    str(len(map_settings.settings.falls))
        self.fall_label.rebuild()

        fall_index_of_reward = self.enemies_spawner.current_fall if self.enemies_spawner.current_fall != -1 else 0
        self.fall_reward_label.html_text = "<b>Next Fall Reward:</b> " + \
                                           str(map_settings.settings.falls[
                                                   fall_index_of_reward].gold_reward) + \
                                           " Gold"
        self.fall_reward_label.rebuild()


    def update(self, dt):
        # session_data.player_hp -= dt * 2.0
        self.player_hp_bar.set_dimensions(
            ((definitions.SCREEN_WIDTH / 2 - 15) * (session_data.player_hp / 100.0),
            15)
        )
        self.player_hp_bar.set_relative_position((
            definitions.SCREEN_WIDTH / 2 + (definitions.SCREEN_WIDTH / 2 - 15) * (1.0 - (session_data.player_hp / 100.0)),
            5
        ))

        if session_data.enemies_in_level != 0:
            self.enemies_fall_bar.set_dimensions(
                ((definitions.SCREEN_WIDTH / 2 - 15) * (session_data.enemies_left / float(session_data.enemies_in_level)),
                15)
            )
        else:
            self.enemies_fall_bar.set_dimensions((definitions.SCREEN_WIDTH / 2 - 15, 15))

