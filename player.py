import pygame
from settings import player_size, getInput, screen_width
from useful import import_animation

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
walk_sound = pygame.mixer.Sound('assets/sounds/walk.wav')

def render_text(message, x, y, font_color=(0, 0, 0), font_type='assets/fonts/OpenSans-Bold.ttf', font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

def pause():
    paused = True
    while paused:
        getInput.update()
        if getInput.terminate:
            pygame.quit()
            sys.exit()

        render_text('Paused. Press Enter to continue', 50, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = False

        pygame.display.update()
        clock.tick(15)

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

        self.gun = None
        self.bullets = pygame.sprite.Group()

    def getInput(self):
        if getInput.isHolding(pygame.K_d):
            walk_sound.play()  # звук ходьбы
            self.direction.x = 1
        elif getInput.isHolding(pygame.K_a):
            walk_sound.play() # звук ходьбы
            self.direction.x = -1
        else:
            self.direction.x = 0

        if getInput.isKeyDown(pygame.K_SPACE):
            self.jump()
        if getInput.isKeyDown(pygame.K_ESCAPE):
            pause()
        if getInput.isKeyDown(pygame.K_q):
            self.shoot()

    def shoot(self):
        if self.look_left:
            x_border = self.rect.left
        else:
            x_border = self.rect.right
        Bullet(x_border, self.rect.bottom - (self.rect.height // 2), 16, 1, self.look_left, self.bullets)

    def jump(self):
        if 0 <= self.direction.y < self.gravity + 0.15:
            jump_sound.play() # звук прыжка
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


class Bullet(pygame.sprite.Sprite):
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
        if self.rect.x > screen_width + 500 or self.rect.x < -500:
            self.kill()


class Effect(pygame.sprite.Sprite):
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

    def update(self, shift=0):
        self.rect.x += shift
        self.animation_index += self.speed
        if self.animation_index > len(self.animation):
            self.animation_index = 0
            self.repetition += 1
        if self.repetition >= self.repeat:
            self.kill()
        self.image = self.animation[int(self.animation_index)]