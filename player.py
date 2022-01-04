import pygame
from settings import player_size, getInput


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(player_size)
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 1
        self.jump_power = -20

    def getInput(self):
        if getInput.isHolding(pygame.K_d):
            self.direction.x = 1
        elif getInput.isHolding(pygame.K_a):
            self.direction.x = -1
        else:
            self.direction.x = 0

        if getInput.isKeyDown(pygame.K_SPACE):
            self.jump()

    def jump(self):
        self.direction.y = self.jump_power

    def acceptGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.getInput()