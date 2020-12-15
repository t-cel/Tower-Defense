from map import *
from static_sprite import *
from circle import Circle
from game_object import *
from arrow import Arrow

import enemy
import math_utils
import json
import math

towers = []
tower_definitions = []

class TowerDefinition:
    def __init__(self, name, image, range, projectile_speed, reload_time, damages, cost):
        self.name = name
        self.image = image
        self.range = range
        self.projectile_speed = projectile_speed
        self.reload_time = reload_time
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
                tower_definition["projectileSpeed"],
                tower_definition["reloadTime"],
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
        self.current_pos_is_valid = False
        self.definition = None
        self.map_pos = self.last_valid_map_pos
        self.on_build_callback = None

        self.circle = game_object.get_components(Circle)[0]
        self.start_circle_color = self.circle.get_color()
        self.t = 0.0

        self.cool_down = False
        self.timer = 0.0
        self.cool_down_duration = 0.4
        self.range = 0.0


    def init_component(self, **kwargs):
        self.enemies_path_coords = kwargs.get("enemies_path_coords")
        self.definition = kwargs.get("definition")
        self.on_build_callback = kwargs.get("on_build_callback")

        self.cool_down_duration = self.definition.reload_time
        self.circle.radius = self.definition.range * TILE_SIZE

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
            self.current_pos_is_valid = False
        else:
            self.current_pos_is_valid = True

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


    def get_intercept_pos(self, e):
        """
            Calculates where to shot projectile to hit moving enemy.

            Source: https://stackoverflow.com/questions/2248876/2d-game-fire-at-a-moving-target-by-predicting-intersection-of-projectile-and-u
        :param e: enemy component
        :return: position of intersection
        """
        src_pos   = self.game_object.pos
        enemy_pos = e.get_target_pos()
        p_s       = self.definition.projectile_speed  # projectile speed

        tx = enemy_pos[0] - src_pos[0]
        ty = enemy_pos[1] - src_pos[1]
        enemy_v = e.get_velocity()

        # get quadratic equation components
        a = enemy_v[0] * enemy_v[0] + enemy_v[1] * enemy_v[1] - p_s * p_s
        b = 2 * (enemy_v[0] * tx + enemy_v[1] * ty)
        c = tx * tx + ty * ty

        # solve
        ts = math_utils.quad(a, b, c)
        sol = None
        if ts:
            t0 = ts[0]
            t1 = ts[1]

            t = min(t0, t1)
            if t < 0:
                t = max(t0, t1)
            if t > 0:
                sol = ( enemy_pos[0] + enemy_v[0] * t, enemy_pos[1] + enemy_v[1] * t )

        return sol


    def spawn_projectile(self, target_pos):

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
            target_pos=target_pos,
            speed=self.definition.projectile_speed,
            damages=self.definition.damages
        )


    def update(self, dt):
        self.t += dt

        if self.dragging_mode:
            self.update_drag()

        elif not self.cool_down:
            for e in enemy.enemies:
                sqr_mag = math_utils.sqr_magnitude(self.game_object.pos, (e.get_target_pos()))
                sqr_r = self.circle.radius * self.circle.radius
                if sqr_mag <= sqr_r:
                    target_pos = self.get_intercept_pos(e)
                    if target_pos is not None:
                        self.spawn_projectile(target_pos)
                        self.cool_down = True
                    break
        else:
            self.timer += dt
            if self.timer >= self.cool_down_duration:
                self.timer = 0
                self.cool_down = False


    def process_event(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN and self.dragging_mode and self.current_pos_is_valid:
            self.dragging_mode = False
            self.circle.set_color(self.start_circle_color)
            if self.on_build_callback:
                self.on_build_callback()
            for tower in towers:
                tower.game_object.get_components(Circle)[0].enabled = False