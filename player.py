import pygame
from settings import player_size, getInput
from useful import import_animation


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
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
        self.on_ground, self.on_ceiling = False, False
        self.on_left, self.on_right = False, False


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
        if 0 <= self.direction.y < self.gravity + 0.15:
            self.direction.y = self.jump_power

    def acceptGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.getInput()
        self.animate()

    def loadAnimations(self):
        self.animations = {'idle': [], 'run': [], 'fall': [], 'jump': [], 'gun_run': []}
        for anim in self.animations.keys():
            self.animations[anim] = import_animation('assets/animations/player_' + anim)

    def getCurrentAnimation(self):
        if self.direction.y > self.gravity + 0.15:
            self.current_animation = 'fall'
        elif self.direction.y < 0:
            self.current_animation = 'jump'
        else:
            if self.direction.x != 0:
                self.current_animation = 'run'
            else:
                self.current_animation = 'idle'

    def animate(self):
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