from definitions import *

from component import Component

import pygame

class SoundTest(Component):

    def __init__(self, game_object):
        super().__init__(game_object)

        self.sound_obj = pygame.mixer.Sound(SOUNDS_PATH + "shot.ogg")


    def init_component(self, **kwargs):
        pass



    def update(self, dt):
        pass



    def process_event(self, event):
        if event.type == pygame.KEYDOWN and chr(event.key) == 'a':
            self.sound_obj.play()
            print("play sound")

