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
# эта функция отвечает за печать текста на кнопках и не только
def print_text(message, x, y, font_color=(0, 0, 0), font_type='assets/fonts/OpenSans-Bold.ttf', font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))
# кнопочки
class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (255, 255, 0)
        self.active_color = (0, 0, 255)

    def draw(self, x, y, text, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_sound = pygame.mixer.Sound('assets/sounds/button.wav')

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

                if click[0] == 1:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)
                    if action is not None:
                        if action == quit:
                            pygame.quit()
                            sys.exit()
                        action()

        else:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

        print_text(text, x + 10, y + 10)

#Главное меню
def show_menu():
    menu_background = pygame.transform.scale(pygame.image.load('assets/mainmenu/watchmops.jpg'), (screen_width, screen_height))
    screen.blit(menu_background, (0, 0))

    start_button = Button(220, 100) # высота и ширина кнопки
    settings_button = Button(220, 100)
    quit_button = Button(220, 100)
    font = pygame.font.Font(None, 30)


    while True:
        getInput.update()
        if getInput.terminate:
            pygame.quit()
            sys.exit()

        screen.blit(menu_background, (0, 0))
        start_button.draw(50, 250, 'Start', level.run()) # позиция кнопки, название и запуск уровня
        settings_button.draw(50, 375, 'Settings')
        quit_button.draw(50, 500, 'Quit', quit) # выход из игры
        pygame.display.update()
        clock.tick(FPS)

show_menu()