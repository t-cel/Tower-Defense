
SWAWN_MODE_END_OF_PREVIOUS_GROUP_SPAWN = "End Of Previous Group Spawn"
SPAWN_MODE_PREVIOUS_GROUP_DESTRUCTION = "Previous Group Destruction"

class EnemiesGroup:
    def __init__(self, enemies_counts, spawn_delay, interval):
        self.enemies_counts = enemies_counts                                   # list (index of enemy -> count)

        self.spawn_mode = SWAWN_MODE_END_OF_PREVIOUS_GROUP_SPAWN   # when to start spawn process ?

        self.spawn_delay = spawn_delay                                   # delay before start spawn process

        self.interval = interval                                 # tuple (min_interval, max_interval), game will chose
                                                                   # random number from this range

class EnemiesFall:
    def __init__(self, groups, gold_reward):
        self.groups = groups
        self.gold_reward = gold_reward


class MapSettings:
    def __init__(self):
        self.start_gold = 0
        self.falls = []
        self.enemies_path_coords = []

settings = MapSettings()

def get_settings():
    return settings