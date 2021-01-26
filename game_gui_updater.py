from component import Component

import tower
import spell
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
        self.spell_research_buttons = []
        self.spell_use_buttons = []

        self.enemies_spawner = None
        self.player_hp_bar = None
        self.enemies_fall_bar = None
        self.game_mode = None


    def init_component(self, **kwargs):
        self.fall_label = kwargs.get("fall_label")
        self.fall_reward_label = kwargs.get("fall_reward_label")
        self.gold_label = kwargs.get("gold_label")
        self.game_mode = kwargs.get("game_mode")

        self.tower_build_buttons = kwargs.get("tower_build_buttons")
        self.spell_research_buttons = kwargs.get("spell_research_buttons")
        self.spell_use_buttons = kwargs.get("spell_use_buttons")

        self.enemies_spawner = kwargs.get("enemies_spawner")
        self.player_hp_bar = kwargs.get("player_hp_bar")
        self.enemies_fall_bar = kwargs.get("enemies_fall_bar")


    def update_stats_gui(self):
        self.gold_label.html_text = f"<b><font color=#DEAF21>Gold: </font>{session_data.player_gold}</b>, " +\
                                    f"<b><font color=#4488FF>Mana: </font>{session_data.player_mana}</b>"
        self.gold_label.rebuild()

        for i in range(0, len(tower.tower_definitions)):
            if i+1 > map_settings.settings.max_tower:
                break
            if tower.tower_definitions[i].cost > session_data.player_gold:
                self.tower_build_buttons[i].disable()
            else:
                self.tower_build_buttons[i].enable()


        for i in range(0, len(spell.spells_definitions)):
            if i+1 > map_settings.settings.max_spell:
                break
            if session_data.spells_researched[i] or spell.spells_definitions[i].research_cost > session_data.player_gold:
                self.spell_research_buttons[i].disable()
            else:
                self.spell_research_buttons[i].enable()

            if not self.game_mode.build_mode_active and \
                    session_data.spells_researched[i] and \
                    spell.spells_definitions[i].use_cost <= session_data.player_mana:
                self.spell_use_buttons[i].enable()
            else:
                self.spell_use_buttons[i].disable()


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

