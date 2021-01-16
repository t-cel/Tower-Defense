import pygame
from os import walk
import os

def load_image(path, alpha = False):
    return pygame.image.load(path).convert_alpha() if alpha else \
           pygame.image.load(path).convert()


def get_all_files_in_path(path, extension=None):
    f = []
    for (dir_path, dir_names, file_names) in walk(path):

        file_names.sort()

        if extension:
            for file_name in file_names:
                if os.path.splitext(file_name)[1] != extension:
                    file_names.remove(file_name)

        f.extend(file_names)

        for i in range(0, len(f)):
            f[i] = path + ("/" if path[-1] != "/" else "") + f[i]
        return f