import os.path
from os import walk, path
import pygame


def import_animation(path):
    lst = []
    for info in walk(path):
        for img in info[2]:
            lst.append(pygame.image.load(path + '/' + img).convert_alpha())
    return lst


def load_level(name):
    if not os.path.isfile(name):
        print(f"Файл {name} не найден")
        return ['', '@', 'XXXX']
    return [i.rstrip('\n') for i in open(name, 'r', encoding='utf-8').readlines()]