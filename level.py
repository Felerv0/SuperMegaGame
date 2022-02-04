import pygame
from tiles import *
from settings import tile_size, screen_height, screen_width
from player import Player, Effect, GameObject
from enemy import *
from useful import render_text


class Level:
    def __init__(self, level_map, surface, data, bg):
        self.surface = surface
        self.data = data
        self.setupLevel(level_map, bg)
        self.shift = 0
        self.current_pos = (0, 0)

    def setupLevel(self, level_map, bg):  # создание уровня
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.effects = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.bg = pygame.sprite.GroupSingle(Background(bg))
        self.ui = pygame.sprite.Group(UIObject((40, 50), (50, 50), 'assets/sprites/gear.png'),
                                      UIObject((40, 110), (50, 50), 'assets/sprites/hp.png'))

        for y, row in enumerate(level_map):
            for x, cell in enumerate(row):
                if cell == 'X':
                    Tile((x * tile_size[0], y * tile_size[1]), tile_size, '', self.tiles)
                elif cell == '@':
                    Player((x * tile_size[0], y * tile_size[1]), self.data, self.player)
                elif cell == 'T':
                    Enemy((x * tile_size[0], y * tile_size[1]), self.enemies)
        self.setupMusic()

    def setupMusic(self):  # настройка музыки
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.music.load('assets/music/robotiklove.mp3')
        pygame.mixer.music.set_volume(0.07)
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

    def objectCollision(self):
        for game_obj in self.objects.sprites():
            if game_obj.rect.colliderect(self.player.sprite.rect):
                if game_obj.type == 'gear':
                    self.data['gear'] += 1
                game_obj.kill()

    def bulletCollision(self):  # коллизия пуль
        bullets = self.player.sprite.bullets
        enemy_collisions = pygame.sprite.groupcollide(bullets, self.enemies, True, False)
        tile_collisions = pygame.sprite.groupcollide(bullets, self.tiles, True, False)
        for tile in tile_collisions.keys():
            Effect(tile.rect.x - 8, tile.rect.y - 8, 'assets/animations/boom', 0.15, 1, self.effects)
        for enemy in enemy_collisions.keys():
            Effect(enemy.rect.x - 8, enemy.rect.y - 8, 'assets/animations/boom', 0.15, 1, self.effects)
            for dm in enemy_collisions[enemy]:
                dm.damage(self.player.sprite.gun.damage)
                if dm.hp <= 0:
                    GameObject(enemy.rect.x - 8, enemy.rect.y - 8, 'gear', self.objects)
                    dm.kill()

    def showUI(self):
        render_text(str(self.data['gear']), 100, 40, self.surface)
        render_text(str(self.player.sprite.hp), 100, 100, self.surface, (255, 0, 0))
        self.ui.draw(self.surface)


    def run(self):
        self.bg.draw(self.surface)
        self.showUI()

        self.tiles.draw(self.surface)
        self.tiles.update(self.shift)
        self.scroll_x()
        self.player.draw(self.surface)

        self.horizontalCollision()
        self.verticalCollision()
        self.bulletCollision()
        self.objectCollision()

        self.player.update()
        self.player.sprite.bullets.update(self.shift)
        self.player.sprite.bullets.draw(self.surface)

        self.effects.update(self.shift)
        self.effects.draw(self.surface)
        self.enemies.update(self.shift)
        self.enemies.draw(self.surface)
        self.objects.draw(self.surface)
        self.objects.update(self.shift)


class Background(pygame.sprite.Sprite):
    def __init__(self, img, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(img), (screen_width, screen_height))
        self.rect = self.image.get_rect()


class UIObject(pygame.sprite.Sprite):
    def __init__(self, pos, size, img, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(img), size)
        self.rect = self.image.get_rect(topleft=pos)