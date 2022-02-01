import pygame
from settings import player_size, getInput, screen_width, DEFAULT_FONT
from useful import import_animation, render_text, termination
from os import listdir

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
release_sound = pygame.mixer.Sound('assets/sounds/release.wav')
walk_sound = pygame.mixer.Sound('assets/sounds/walk.wav')
shoot_sound = pygame.mixer.Sound('assets/sounds/blaster.wav')
hit_sound = pygame.mixer.Sound('assets/sounds/hit.wav')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, userdata, *groups):
        super().__init__(*groups)
        self.loadAnimations()

        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.85
        self.jump_power = -20

        self.animation_speed = 0.15
        self.animation_index = 0
        self.current_animation = 'idle'
        self.look_left = False
        self.shooting = False
        self.shoot_delay = 0
        self.on_ground, self.on_ceiling = False, False
        self.on_left, self.on_right = False, False
        self.walk_index = 0

        self.gun = Gun(userdata['gun_lvl'])
        self.bullets = pygame.sprite.Group()
        self.holdingGun = False
        self.max_hp = userdata['max_hp']
        self.hp = self.max_hp

    def getInput(self):  # получение клавиш для ввода
        if getInput.isHolding(pygame.K_d):
            self.direction.x = 1
        elif getInput.isHolding(pygame.K_a):
            self.direction.x = -1
        else:
            self.direction.x = 0

        if getInput.isKeyDown(pygame.K_SPACE):
            self.jump()
        if getInput.isKeyDown(pygame.K_q):
            self.shoot()
        if getInput.isKeyDown(pygame.K_1):
            self.switchGun()

    def shoot(self):  # стрельба
        if self.holdingGun and self.shoot_delay == 0:
            if self.look_left:
                x_border = self.rect.left
            else:
                x_border = self.rect.right
            shoot_sound.play()
            self.shoot_delay += 11
            Bullet(x_border, self.rect.bottom - (self.rect.height // 2), 16, 1, self.look_left, self.bullets)

    def switchGun(self):  # взять / убрать оружие
        self.holdingGun = not self.holdingGun

    def jump(self):  # прыжок
        if 0 <= self.direction.y < self.gravity + 0.15:
            self.direction.y = self.jump_power

    def acceptGravity(self):  # применение гравитации к персонажу
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        if self.direction.x != 0 and -0.2 < self.direction.y < 1:
            self.walk_index += 1
            if self.walk_index > 15:
                self.walk_index = 0
                walk_sound.play()
        self.shoot_delay = max(0, self.shoot_delay - 1)
        self.getInput()
        self.animate()

    def loadAnimations(self):  # загрузка анимаций
        self.animations = {}
        for anim in listdir('assets/animations/player'):
            self.animations[anim[7:]] = import_animation('assets/animations/player/' + anim)
        for anim in listdir('assets/animations/player_gun'):
            self.animations[anim[7:]] = import_animation('assets/animations/player_gun/' + anim)

    def getCurrentAnimation(self):  # получение состояния героя
        if self.direction.y > self.gravity + 0.15:
            self.current_animation = 'fall'
        elif self.direction.y < 0:
            self.current_animation = 'jump'
        else:
            if self.direction.x != 0:
                self.current_animation = 'run'
            else:
                self.current_animation = 'idle'
        if self.holdingGun:
            self.current_animation += '_gun'

    def animate(self):  # анимация игрока
        self.getCurrentAnimation()
        if self.direction.x > 0:
            self.look_left = False
        elif self.direction.x < 0:
            self.look_left = True
        self.animation_index += self.animation_speed
        if self.animation_index > len(self.animations[self.current_animation]):
            self.animation_index = 0
        self.image = pygame.transform.flip(self.animations[self.current_animation][int(self.animation_index)],
                                           self.look_left, False)

        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            elif self.on_left:
                self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(topright=self.rect.topright)
            elif self.on_left:
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
            else:
                self.rect = self.image.get_rect(midtop=self.rect.midtop)


class Bullet(pygame.sprite.Sprite):  # пуля
    def __init__(self, x, y, speed, damage, left, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('assets/sprites/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed
        if left:
            self.speed = -self.speed
        self.damage = damage

    def update(self, shift):
        self.rect.x += self.speed + shift
        if self.rect.x > screen_width + 500 or self.rect.x < -500:  # при выходе за отступы от краёв экрана, удаляется
            self.kill()


class Effect(pygame.sprite.Sprite):  # класс для эффектов (анимация взрыва и т.д.)
    def __init__(self, x, y, animation, speed, repeat=1, *groups):
        super().__init__(*groups)
        self.animation = import_animation(animation)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.animation_index = 0
        self.repetition = 0
        self.speed = speed
        self.repeat = repeat
        hit_sound.play()

    def update(self, shift=0):
        self.rect.x += shift
        self.animation_index += self.speed
        if self.animation_index > len(self.animation):
            self.animation_index = 0
            self.repetition += 1
        if self.repetition >= self.repeat:
            self.kill()
        self.image = self.animation[int(self.animation_index)]


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, obj_type, *groups):
        super().__init__(*groups)
        self.type = obj_type
        if obj_type == 'gear':
            self.image = pygame.transform.scale(pygame.image.load('assets/sprites/gear.png'), (64, 64))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

class Gun:
    def __init__(self, lvl):
        self.damage = 1 * lvl
        self.level = lvl