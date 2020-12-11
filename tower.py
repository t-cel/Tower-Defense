from map import *
from static_sprite import *
from enemy import *
from circle import Circle
from game_object import *
from arrow import Arrow
import math_utils

import math

towers = []
tower_definitions = []

class TowerDefinition:
    def __init__(self, name, image, range, speed, damages, cost):
        self.name = name
        self.image = image
        self.range = range
        self.speed = speed
        self.damages = damages
        self.cost = cost

def load_towers_definitions():
    f = open(DEFINITIONS_PATH + "towers.json")
    data = json.load(f)
    for tower_definition in data["towers"]:
        tower_definitions.append(
            TowerDefinition(
                tower_definition["name"],
                tower_definition["image"],
                tower_definition["range"],
                tower_definition["speed"],
                tower_definition["damages"],
                tower_definition["cost"]
            )
        )

class Tower(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.dragging_mode = True
        self.enemies_path_coords = None
        self.last_valid_map_pos = (-5, 0)
        self.map_pos = self.last_valid_map_pos

        self.circle = game_object.get_components(Circle)[0]
        self.start_circle_color = self.circle.get_color()
        self.t = 0.0

        self.cool_down = False
        self.timer = 0.0
        self.cool_down_duration = 0.4

    def init_component(self, **kwargs):
        self.enemies_path_coords = kwargs.get("enemies_path_coords")
        towers.append(self)

    def valid_map_pos(self, map_pos):

        # map bounds
        if map_pos[0] < 0 or map_pos[1] < 0 or map_pos[0] >= MAP_W or map_pos[1] >= MAP_H:
            return False

        # paths
        for coord in self.enemies_path_coords:
            if coord[0] == map_pos[0] and coord[1] == map_pos[1]:
                return False

        # other towers
        for tower in towers:
            if tower is not self:
                if tower.map_pos[0] == map_pos[0] and tower.map_pos[1] == map_pos[1]:
                    return False

        return True

    def update_drag(self):
        for tower in towers:
            tower.game_object.get_components(Circle)[0].enabled = True

        target_pos = pygame.mouse.get_pos()  # get mouse pos on window
        self.map_pos = get_tile_pos(target_pos[0], target_pos[1])  # convert to map pos

        if not self.valid_map_pos(self.map_pos):
            self.map_pos = self.last_valid_map_pos

        target_pos = get_tile_coords(self.map_pos[0], self.map_pos[1])  # convert back to screen coords
        self.last_valid_map_pos = self.map_pos

        self.game_object.set_pos(target_pos)
        mult = math.sin(self.t * 5.0) * 0.5 + 1.0

        self.circle.set_color((
            self.start_circle_color[0] * mult,
            self.start_circle_color[1] * mult,
            self.start_circle_color[2] * mult,
            self.start_circle_color[3]
        ))

    def spawn_projectile(self, target):
        arrow_object = GameObject(
            self.game_object.pos,
            (1, 1),
            0
        )

        arrow_object.add_component(StaticSprite).init_component(
            pos=(0, 0),
            size=(int(TILE_SIZE/2), int(TILE_SIZE/2)),
            angle=0,
            image_path=PROJECTILES_PATH + 'arrow.png',
            alpha=True,
            #clone=True
        )

        arrow_object.add_component(Arrow).init_component(
            target_enemy=target
        )

    def update(self, dt):
        self.t += dt

        if self.dragging_mode:
            self.update_drag()

        elif not self.cool_down:
            for enemy in enemies:
                sqr_mag = math_utils.sqr_magnitude(self.game_object.pos, enemy.game_object.pos)
                sqr_r = self.circle.radius * self.circle.radius
                if sqr_mag <= sqr_r:
                    self.spawn_projectile(enemy)
                    self.cool_down = True
                    break
        else:
            self.timer += dt
            if self.timer >= self.cool_down_duration:
                self.timer = 0
                self.cool_down = False

    def process_event(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN and self.dragging_mode:
            self.dragging_mode = False
            self.circle.set_color(self.start_circle_color)
            for tower in towers:
                tower.game_object.get_components(Circle)[0].enabled = False