import pygame
from os import walk

def load_image(path, alpha = False):
    return pygame.image.load(path).convert_alpha() if alpha else \
           pygame.image.load(path).convert()

def get_all_files_in_path(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        for i in range(0, len(f)):
            f[i] = path + "/" + f[i]
        return f