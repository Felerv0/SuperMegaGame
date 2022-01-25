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
pygame.display.set_caption('Watch Mops')

level = Level(load_level('data/levels/1.txt'), screen)


# эта функция отвечает за печать текста на кнопках и не только
def render_text(message, x, y, font_color=(0, 0, 0), font_type=DEFAULT_FONT, font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:  # кнопочки
    def __init__(self, x, y, width, height, text, color=(255, 255, 0), hover=(0, 0, 255),
                 font=DEFAULT_FONT, font_size=50, text_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.inactive_color = color
        self.active_color = hover
        self.button_sound = pygame.mixer.Sound('assets/sounds/button.wav')
        self.font = font
        self.font_size = font_size
        self.text_color = text_color

    def draw(self, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))
            if click[0] == 1:
                pygame.mixer.Sound.play(self.button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        sys.exit()
                    action()
        else:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
        render_text(self.text, self.x + 10, self.y + 10, self.text_color, self.font, self.font_size)


def start_game():
    while True:
        getInput.update()
        if getInput.terminate:
            pygame.quit()
            sys.exit()
        screen.fill(pygame.Color('black'))
        level.run()
        pygame.display.update()
        clock.tick(FPS)


def show_menu():  # Главное меню
    menu_background = pygame.transform.scale(pygame.image.load(MAIN_BACKGROUND), (screen_width, screen_height))
    screen.blit(menu_background, (0, 0))

    start_button = Button(50, 250, 220, 100, 'Start')
    settings_button = Button(50, 375, 220, 100, 'Settings')
    quit_button = Button(50, 500, 220, 100, 'Quit')

    while True:
        getInput.update()
        if getInput.terminate:
            pygame.quit()
            sys.exit()

        screen.blit(menu_background, (0, 0))
        start_button.draw(start_game)  # позиция кнопки, название и запуск уровня
        settings_button.draw()
        quit_button.draw(quit)  # выход из игры
        pygame.display.update()
        clock.tick(FPS)

show_menu()
