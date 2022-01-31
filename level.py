import pygame
from tiles import *
from settings import tile_size, screen_height, screen_width
from player import Player, Effect
from enemy import *


class Level:
    def __init__(self, level_map, surface):
        self.surface = surface
        self.setupLevel(level_map)
        self.shift = 0
        self.current_pos = (0, 0)

    def setupLevel(self, level_map):  # создание уровня
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.effects = pygame.sprite.Group()
        for y, row in enumerate(level_map):
            for x, cell in enumerate(row):
                if cell == 'X':
                    Tile((x * tile_size[0], y * tile_size[1]), tile_size, self.tiles)
                elif cell == '@':
                    Player((x * tile_size[0], y * tile_size[1]), self.player)
                elif cell == 'T':
                    Enemy((x * tile_size[0], y * tile_size[1]), self.enemies)
        self.setupMusic()

    def setupMusic(self):  # настройка музыки
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.music.load('assets/music/robotiklove.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def scroll_x(self):  # скролл уровня по горизонтали
        if self.player.sprite.rect.centerx < screen_width // 3 and self.player.sprite.direction.x < 0:
            self.shift = 8
            self.player.sprite.speed = 0
        elif self.player.sprite.rect.centerx > screen_width - screen_width // 3 and self.player.sprite.direction.x > 0:
            self.shift = -8
            self.player.sprite.speed = 0
        else:
            self.shift = 0
            self.player.sprite.speed = 8

    def scroll_y(self):
        pass

    def horizontalCollision(self):  # горизонтальная коллизия с объектами
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_pos = (player.rect.left, self.current_pos[1])
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_pos = (player.rect.right, self.current_pos[1])
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = enemy.rect.right
                    player.on_left = True
                    self.current_pos = (player.rect.left, self.current_pos[1])
                elif player.direction.x > 0:
                    player.rect.right = enemy.rect.left
                    player.on_right = True
                    self.current_pos = (player.rect.right, self.current_pos[1])

        if player.on_left and (player.rect.left < self.current_pos[0] or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_pos[0] or player.direction.x <= 0):
            player.on_right = False

    def verticalCollision(self):  # вертикальная коллизия
        player = self.player.sprite
        player.acceptGravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ceiling = True

            for enemy in self.enemies:
                if tile.rect.colliderect(enemy.rect):
                    if enemy.direction.y < 0:
                        enemy.rect.top = tile.rect.bottom
                        enemy.direction.y = 0
                    elif player.direction.y > 0:
                        enemy.rect.bottom = tile.rect.top
                        enemy.direction.y = 0
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = enemy.rect.bottom
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y > 0:
                    player.rect.bottom = enemy.rect.top
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def bulletCollision(self):  # коллизия пуль
        bullets = self.player.sprite.bullets
        enemy_collisions = pygame.sprite.groupcollide(bullets, self.enemies, True, False)
        tile_collisions = pygame.sprite.groupcollide(bullets, self.tiles, True, False)
        for tile in tile_collisions.keys():
            Effect(tile.rect.x - 8, tile.rect.y - 8, 'assets/animations/boom', 0.15, 1, self.effects)
        for enemy in enemy_collisions.keys():
            Effect(enemy.rect.x - 8, enemy.rect.y - 8, 'assets/animations/boom', 0.15, 1, self.effects)


    def run(self):
        self.tiles.draw(self.surface)
        self.tiles.update(self.shift)
        self.scroll_x()
        self.player.draw(self.surface)

        self.horizontalCollision()
        self.verticalCollision()
        self.bulletCollision()

        self.player.update()
        self.player.sprite.bullets.update(self.shift)
        self.player.sprite.bullets.draw(self.surface)

        self.effects.update(self.shift)
        self.effects.draw(self.surface)
        self.enemies.update(self.shift)
        self.enemies.draw(self.surface)
