import pygame
from useful import import_animation


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.animations = import_animation('assets/animations/telesos')
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.85

        self.hp = 10
        self.maxhp = 10
        self.speed = 9

        self.anim_index = 0
        self.anim_speed = 0.15

        self.blocks_stepped = 300

    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index > len(self.animations):
            self.anim_index = 0
        self.image = self.animations[int(self.anim_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift
        self.move()

    def damage(self, dm):
        self.hp -= dm
        if self.hp <= 0:
            self.kill()

    def acceptGravity(self):  # применение гравитации к врагу
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def move(self):
        if self.blocks_stepped >= 600:
            self.direction.x -= self.direction.x
            self.blocks_stepped = 0
        self.rect.x += self.direction.x * self.speed
        self.blocks_stepped += 1