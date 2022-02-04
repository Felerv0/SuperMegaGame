import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, texture, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill(pygame.Color('grey'))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift):
        self.rect.x += shift