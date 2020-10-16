from map import *
from dynamic_sprite import DynamicSprite
from component import Component
from utils import *

enemies = []

class Enemy(Component):
    def __init__(self, game_object):
        super().__init__(game_object)

        self.enemies_paths = None
        self.path_index = 0
        self.coord_index = 0
        self.game_object = game_object
        self.t = 0.0
        self.speed = 1.5
        self.start_coords = game_object.pos

        self.hp = 100.0
        self.hp_bar = None

        self.dynamic_sprite = None

        enemies.append(self)

    def init_component(self, **kwargs):
        self.enemies_paths = kwargs.get("enemies_paths")
        self.hp_bar = kwargs.get("hp_bar")

        self.hp_bar.enabled = False
        self.dynamic_sprite = self.game_object.get_components(DynamicSprite)[0]

    def take_damage(self, damage):
        self.hp -= damage

        if not self.game_object.destroy:
            if self.hp <= 0:
                self.hp = 0
                enemies.remove(self)
                self.game_object.destroy = True

            # update hp bar
            new_width = int(50 * (self.hp / 100.0))
            self.hp_bar.set_size((new_width, 5))
            self.hp_bar.set_pos((TILE_SIZE / 2 - new_width / 2, -6))
            self.hp_bar.enabled = True

    # todo: fix that mess
    def update(self, dt):
        # print(dt)
        self.t += self.speed * dt
        # move_t = pow(math.sin(self.t*3.14159265359*0.5), 2.0)
        move_t = self.t

        if move_t > 0.99:
            if self.coord_index == len(self.enemies_paths[self.path_index].coords) - 1:
                if self.path_index == len(self.enemies_paths) - 1:
                    print("end")
                else:
                    self.t = 0.0
                    start_pos = self.enemies_paths[self.path_index].coords[self.coord_index]
                    self.start_coords = get_tile_coords(start_pos[0], start_pos[1])
                    self.coord_index = 0
                    self.path_index += 1
            else:
                self.t = 0.0
                start_pos = self.enemies_paths[self.path_index].coords[self.coord_index]
                self.start_coords = get_tile_coords(start_pos[0], start_pos[1])
                self.coord_index += 1
        else:
            current_path = self.enemies_paths[self.path_index]
            target_pos = self.enemies_paths[self.path_index].coords[self.coord_index]
            target_coords = get_tile_coords(target_pos[0], target_pos[1])
            self.game_object.set_pos(lerp(
                self.start_coords,
                target_coords,
                move_t
            ))

            self.dynamic_sprite.z_pos = self.game_object.pos[1]

            #last_coord = current_path.coords[-1]
            #first_coord = current_path.coords[0]
            #self.dynamic_sprite.z_pos = int(
            #    99 -
            #    (
            #    magnitude(self.game_object.pos, get_tile_coords(last_coord[0], last_coord[1])) /
            #    magnitude(get_tile_coords(first_coord[0], first_coord[1]), get_tile_coords(last_coord[0], last_coord[1]))
            #    )
            #    * 99
            #)
            #print(self.dynamic_sprite.z_pos)