import pygame
from useful import import_animation


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.animations = import_animation('assets/animations/telesos')
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(1, 0)
        self.gravity = 0.85

        self.hp = 10
        self.max_hp = 10
        self.speed = 4

        self.anim_index = 0
        self.anim_speed = 0.15
        self.look_left = True

        self.blocks_stepped = 300

    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index > len(self.animations):
            self.anim_index = 0
        if self.direction.x < 0:
            self.look_left = False
        else:
            self.look_left = True
        self.image = pygame.transform.flip(self.animations[int(self.anim_index)], self.look_left, False)

    def update(self, shift):
        self.animate()
        self.rect.x += shift
        self.move()

    def damage(self, dm):
        self.hp -= dm

    def acceptGravity(self):  # применение гравитации к врагу
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def move(self):
        if self.blocks_stepped >= 600:
            self.direction.x = -self.direction.x
            self.blocks_stepped = 0
        self.rect.x += self.direction.x * self.speed
        self.blocks_stepped += self.speed