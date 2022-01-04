import pygame
from tiles import *
from settings import tile_size, screen_height, screen_width
from player import Player


class Level:
    def __init__(self, level_map, surface):
        self.surface = surface
        self.setupLevel(level_map)
        self.shift = 0

    def setupLevel(self, level_map):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for y, row in enumerate(level_map):
            for x, cell in enumerate(row):
                if cell == 'X':
                    Tile((x * tile_size[0], y * tile_size[1]), tile_size, self.tiles)
                elif cell == '@':
                    Player((x * tile_size[0], y * tile_size[1]), self.player)

    def scroll_x(self):
        if self.player.sprite.rect.centerx < screen_width // 5 and self.player.sprite.direction.x < 0:
            self.shift = 8
            self.player.sprite.speed = 0
        elif self.player.sprite.rect.centerx > screen_width - screen_width // 5 and self.player.sprite.direction.x > 0:
            self.shift = -8
            self.player.sprite.speed = 0
        else:
            self.shift = 0
            self.player.sprite.speed = 8

    def horizontalCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left

    def verticalCollision(self):
        player = self.player.sprite
        player.acceptGravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0

    def run(self):
        self.tiles.draw(self.surface)
        self.tiles.update(self.shift)
        self.scroll_x()
        self.player.draw(self.surface)
        self.horizontalCollision()
        self.verticalCollision()
        self.player.update()