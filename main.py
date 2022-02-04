import pygame
import sys

from settings import *
from tiles import *
from level import *
from useful import *

data = load_data()

pygame.init()

pygame.mixer.music.load('assets/music/MainMenu.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Watch Mops')


class Button:  # кнопочки
    def __init__(self, x, y, width, height, text, surface, color=(255, 255, 0), hover=(0, 0, 255),
                 font=DEFAULT_FONT, font_size=50, text_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.surface = surface
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
                        termination(data)
                    action()
        else:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
        render_text(self.text, self.x + 10, self.y + 10, self.surface, self.text_color, self.font, self.font_size)


def start_game():
    level = Level(load_level('data/levels/demo.txt'), screen, data, 'assets/images/bg.jpg')
    while True:
        getInput.update()
        if getInput.terminate:
            termination(data)
        elif getInput.isKeyDown(pygame.K_ESCAPE):
            pause()
        level.run()
        pygame.display.update()
        clock.tick(FPS)


def pause():
    paused = True
    while paused:
        getInput.update()
        if getInput.terminate:
            termination(data)
        render_text('Paused. Press ESC to continue', 50, 300, screen, (255, 255, 255))
        if getInput.isKeyDown(pygame.K_ESCAPE):
            paused = False

        pygame.display.update()
        clock.tick(15)


def show_menu():  # Главное меню
    menu_background = pygame.transform.scale(pygame.image.load(MAIN_BACKGROUND), (screen_width, screen_height))
    screen.blit(menu_background, (0, 0))

    start_button = Button(50, 250, 220, 100, 'Start', screen)
    settings_button = Button(50, 375, 220, 100, 'Settings', screen)
    quit_button = Button(50, 500, 220, 100, 'Quit', screen)

    while True:
        getInput.update()
        if getInput.terminate:
            termination(data)

        screen.blit(menu_background, (0, 0))
        start_button.draw(start_game)  # позиция кнопки, название и запуск уровня
        settings_button.draw()
        quit_button.draw(quit)  # выход из игры
        pygame.display.update()
        clock.tick(FPS)

show_menu()
