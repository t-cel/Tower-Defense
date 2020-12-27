from component import Component

import tower
import player_stats
import map_settings

class GameGUIUpdater(Component):

    def __init__(self, game_object):
        super().__init__(game_object)

        self.fall_label = None
        self.fall_reward_label = None
        self.gold_label = None
        self.tower_build_buttons = []

        self.enemies_spawner = None


    def init_component(self, **kwargs):
        self.fall_label = kwargs.get("fall_label")
        self.fall_reward_label = kwargs.get("fall_reward_label")
        self.gold_label = kwargs.get("gold_label")
        self.tower_build_buttons = kwargs.get("tower_build_buttons")
        self.enemies_spawner = kwargs.get("enemies_spawner")


    def update_stats_gui(self):
        self.gold_label.html_text = "<b><font color=#DEAF21>Gold: </font>" + str(player_stats.player_gold) + "</b>";
        self.gold_label.rebuild()

        i = 0
        for btn in self.tower_build_buttons:
            if tower.tower_definitions[i].cost > player_stats.player_gold:
                btn.disable()
            else:
                btn.enable()
            i += 1

        self.fall_label.html_text = "<b>Fall:</b> " + \
                                    str(self.enemies_spawner.current_fall + 1) + " / " + \
                                    str(len(map_settings.settings.falls))
        self.fall_label.rebuild()

        self.fall_reward_label.html_text = "<b>Reward:</b> " + \
                                           str(map_settings.settings.falls[
                                                   self.enemies_spawner.current_fall].gold_reward) + \
                                           " Gold"
        self.fall_reward_label.rebuild()


    def update(self, dt):
        pass