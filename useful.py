from os import walk
import pygame


def import_animation(path):
    lst = []
    for info in walk(path):
        for img in info[2]:
            lst.append(pygame.image.load(path + '/' + img).convert_alpha())
    return lst