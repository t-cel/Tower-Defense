from map import *
from static_sprite import *
from enemy import *
from circle import Circle
from game_object import *
from arrow import Arrow

import math

towers = []

class Tower(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.dragging_mode = True
        self.enemies_paths = None
        self.last_valid_map_pos = (-5, 0)
        self.map_pos = self.last_valid_map_pos

        self.circle = game_object.get_components(Circle)[0]
        self.start_circle_color = self.circle.get_color()
        self.t = 0.0

        self.cool_down = False
        self.timer = 0.0
        self.cool_down_duration = 0.4

    def init_component(self, **kwargs):
        self.enemies_paths = kwargs.get("enemies_paths")
        towers.append(self)

    def get_final_pos(self, map_pos):
        target_pos = get_tile_coords(map_pos[0], map_pos[1])
        for enemy_path in self.enemies_paths:
            if enemy_path.is_horizontal:
                for coord in enemy_path.coords:
                    if coord[0] == map_pos[0] and coord[1] == map_pos[1]:
                        return target_pos[0], target_pos[1] - TILE_SIZE * 0.5

        return target_pos

    def valid_map_pos(self, map_pos):

        # map bounds
        if map_pos[0] <= 0 or map_pos[1] <= 0 or map_pos[0] >= MAP_W_HALF*2 or map_pos[1] >= MAP_H_HALF*2:
            return False

        # vertical paths
        for enemy_path in self.enemies_paths:
            if not enemy_path.is_horizontal:
                for coord in enemy_path.coords:
                    if coord[0] == map_pos[0] and coord[1] == map_pos[1]:
                        return False

        # don't allow towers to be placed 1 tile higher than horizontal paths to avoid towers intersecting and keep them
        # aligned
        for enemy_path in self.enemies_paths:
            if enemy_path.is_horizontal:
                for coord in enemy_path.coords:
                    if coord[0] == map_pos[0] and coord[1] - 1 == map_pos[1]:
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

        target_pos = self.get_final_pos(self.map_pos)  # convert back to screen coords
        self.last_valid_map_pos = self.map_pos

        self.game_object.set_pos(target_pos)
        mult = math.sin(self.t * 5.0) * 0.5 + 1.0

        self.circle.set_color((
            self.start_circle_color[0] * mult,
            self.start_circle_color[1] * mult,
            self.start_circle_color[2] * mult
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
                sqr_mag = sqr_magnitude(self.game_object.pos, enemy.game_object.pos)
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
            for tower in towers:
                tower.game_object.get_components(Circle)[0].enabled = False