import pygame
import sys

import settings
from settings import *
from tiles import *
from level import *
from useful import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(load_level('data/levels/1.txt'), screen)

while True:
    getInput.update()
    if getInput.terminate:
        pygame.quit()
        sys.exit()

    screen.fill(pygame.Color('black'))
    level.run()

    pygame.display.update()
    clock.tick(FPS)