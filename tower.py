from map import *
from static_sprite import *
from circle import Circle
from rectangle import Rectangle
from game_object import *
from arrow import Arrow

import enemy
import math_utils
import json
import math
import pygame

towers = []
tower_definitions = []

RECTANGULAR_RANGE_TYPE = "Rectangular"
CIRCULAR_RANGE_TYPE = "Circular"

# arrow_num = 0

class TowerDefinition:
    def __init__(self, name, image, projectile_image, range, range_type, projectile_speed, reload_time, damages, cost):
        self.name = name
        self.image = image
        self.projectile_image = projectile_image
        self.range = range
        self.range_type = range_type
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
                tower_definition["projectileImage"],
                tower_definition["range"],
                tower_definition["rangeType"],
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

        # self.circle = None
        # self.rectangles = []
        self.range_indicators = []

        self.start_color = None
        self.t = 0.0

        self.cool_down = False
        self.timer = 0.0
        self.cool_down_duration = 0.4

        self.shot_sound = pygame.mixer.Sound(SOUNDS_PATH + "shot.ogg")
        self.shot_sound.set_volume(0.5)



    def init_component(self, **kwargs):
        super().init_component(**kwargs)

        self.enemies_path_coords = kwargs.get("enemies_path_coords")
        self.definition = kwargs.get("definition")
        self.on_build_callback = kwargs.get("on_build_callback")

        self.cool_down_duration = self.definition.reload_time

        if self.definition.range_type == CIRCULAR_RANGE_TYPE:
            circle = self.game_object.get_components(Circle)[0]
            circle.radius = self.definition.range * TILE_SIZE
            self.start_color = circle.get_color()
            self.range_indicators = [circle]
        else:
            rectangles = self.game_object.get_components(Rectangle)

            rectangles[0].pos = (-self.definition.range * (TILE_SIZE * 0.5) + TILE_SIZE * 0.5, 0)
            rectangles[0].w = self.definition.range * TILE_SIZE
            rectangles[0].h = TILE_SIZE

            rectangles[1].pos = (0, -self.definition.range * (TILE_SIZE * 0.5) + TILE_SIZE * 0.5)
            rectangles[1].w = TILE_SIZE
            rectangles[1].h = self.definition.range * TILE_SIZE

            self.start_color = rectangles[0].get_color()
            self.range_indicators = rectangles

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



    def change_range_indicators_activity(self, show):
        for indicator in self.range_indicators:
            indicator.enabled = show



    def update_drag(self):
        for tower in towers:
            tower.change_range_indicators_activity(True)

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

        for indicator in self.range_indicators:
            indicator.set_color((
                self.start_color[0] * mult,
                self.start_color[1] * mult,
                self.start_color[2] * mult,
                self.start_color[3]
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

        self.shot_sound.play()
        # global arrow_num
        # arrow_num+=1

        arrow_object = GameObject(
            self.game_object.pos,
            (1, 1),
            0
            # "arrow" + str(arrow_num)
        )

        arrow_object.add_component(StaticSprite).init_component(
            pos=(0, 0),
            size=(int(TILE_SIZE/2), int(TILE_SIZE/2)),
            angle=0,
            image_path=PROJECTILES_PATH + self.definition.projectile_image + '.png',
            alpha=True,
            #clone=True
        )

        arrow_object.add_component(Arrow).init_component(
            target_pos=target_pos,
            speed=self.definition.projectile_speed,
            damages=self.definition.damages
        )



    def detect_and_shot(self):
        for e in enemy.enemies:
            sqr_mag = math_utils.sqr_magnitude(self.game_object.pos, (e.get_target_pos()))
            if self.definition.range_type == CIRCULAR_RANGE_TYPE:
                sqr_r = self.range_indicators[0].radius * self.range_indicators[0].radius
                if sqr_mag <= sqr_r:
                    target_pos = self.get_intercept_pos(e)
                    if target_pos is not None:
                        # print("circular")
                        self.spawn_projectile(target_pos)
                        self.cool_down = True
                    return
            else:
                # todo: zrobić rectangle range na podstawie koordynatów na mapie oraz dystansu
                #       oraz przy trybie przeciągania dać możliwość wyboru zasięgu horyzontalnego
                #       lub wertykalnego

                enemy_tile_pos = get_tile_pos(e.game_object.pos[0], e.game_object.pos[1])
                #print(math.fabs(enemy_tile_pos[0] - self.map_pos[0]))

                if (math.fabs(enemy_tile_pos[0] - self.map_pos[0]) <= self.definition.range * 0.5 and
                    enemy_tile_pos[1] == self.map_pos[1]) or \
                    (math.fabs(enemy_tile_pos[1] - self.map_pos[1]) <= self.definition.range * 0.5 and
                     enemy_tile_pos[0] == self.map_pos[0]):

                    target_pos = self.get_intercept_pos(e)
                    if target_pos is not None:
                        # print("rectangle")
                        # print(f"spawn projectile: {arrow_num + 1}")
                        self.spawn_projectile(target_pos)
                        self.cool_down = True
                    return
                #for rectangle in self.range_indicators:
                #     if rectangle.pos[0] + self.game_object.pos[0] <= e.game_object.pos[0] <= rectangle.pos[0] + \
                #             self.game_object.pos[0] + rectangle.w and \
                #             rectangle.pos[1] + self.game_object.pos[1] <= e.game_object.pos[1] <= rectangle.pos[1] + \
                #             self.game_object.pos[1] + rectangle.h:
                #         target_pos = self.get_intercept_pos(e)
                #         if target_pos is not None:
                #             # print("rectangle")
                #             # print(f"spawn projectile: {arrow_num + 1}")
                #             self.spawn_projectile(target_pos)
                #             self.cool_down = True
                #         return



    def update(self, dt):
        self.t += dt

        if self.dragging_mode:
            self.update_drag()
        else:
            if not self.cool_down:
                self.detect_and_shot()
            else:
                self.timer += dt
                if self.timer >= self.cool_down_duration:
                    self.timer = 0
                    self.cool_down = False

            target_pos = pygame.mouse.get_pos()  # get mouse pos on window
            map_pos = get_tile_pos(target_pos[0], target_pos[1])
            self.change_range_indicators_activity(map_pos == self.map_pos)


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.dragging_mode and self.current_pos_is_valid:
            self.dragging_mode = False

            for indicator in self.range_indicators:
                indicator.set_color(self.start_color)

            if self.on_build_callback:
                self.on_build_callback()

            for tower in towers:
                tower.change_range_indicators_activity(False)