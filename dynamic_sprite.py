from static_sprite import *

class AnimationState:
    def __init__(self, transition_type, frame_start, frame_end):
        self.transition_type = transition_type
        self.frame_start = frame_start
        self.frame_end = frame_end


# sprite consisted from > 1 images
class DynamicSprite(StaticSprite):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.timer = 0.0
        self.max_time = 0.02
        self.speed = 1.0
        self.looping = True

        self.animation_states = []
        self.current_animation_state = 0


    def init_component(self, **kwargs):
        super().init_component(**kwargs)
        if "speed" in kwargs:
            self.speed = kwargs.get("speed")

        if "looping" in kwargs:
            self.looping = kwargs.get("looping")

        if "animation_states" in kwargs and len(kwargs.get("animation_states")) > 0:
            self.animation_states = kwargs.get("animation_states")
        else:
            self.animation_states.append(
                AnimationState(
                    "simple",
                    0,
                    len(self.images)
                )
            )


    def on_next_frame(self):
        self.current_image += 1
        anim_state = self.animation_states[self.current_animation_state]

        if self.current_image >= anim_state.frame_end:

            # last frame
            if self.current_animation_state == len(self.animation_states) - 1:
                if self.looping:
                    self.current_image = anim_state.frame_start
                else:
                    self.change_activity(False)
            else:
                # simple states switch between themselves, conditional states needs to be switched
                # externally
                if anim_state.transition_type == "simple":
                    self.current_animation_state += 1
                else:
                    self.current_image = anim_state.frame_start


    def switch_state(self, state):
        self.current_animation_state = state


    def update(self, dt):
        # print(self.timer)
        self.timer += dt * self.speed
        if self.timer >= self.max_time:
            self.on_next_frame()
            self.timer = 0.0