
SWAWN_MODE_END_OF_PREVIOUS_GROUP_SPAWN = "End Of Previous Group Spawn"
SPAWN_MODE_PREVIOUS_GROUP_DESTRUCTION = "Previous Group Destruction"

class EnemiesGroup:
    def __init__(self):
        self.enemies_counts = []                                   # list (index of enemy -> count)

        self.spawn_mode = SWAWN_MODE_END_OF_PREVIOUS_GROUP_SPAWN   # when to start spawn process ?

        self.spawn_delay = 0.0                                     # delay before start spawn process

        self.interval = (0.0, 0.0)                                 # tuple (min_interval, max_interval), game will chose
                                                                   # random number from this range

class EnemiesFall:
    def __init__(self):
        self.groups = []
        self.gold_reward = 0


class MapSettings:
    def __init__(self):
        self.start_gold = 0
        self.falls = []
        self.enemies_path_coords = []

settings = MapSettings()

def get_settings():
    return settings