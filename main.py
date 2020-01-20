import pygame
import os
import random

pygame.init()
size = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")

BLOCK_SIZE = 50  # размер одного блока
MAX_VEL_Y = 10
GRAVITY = 10
FPS = 60
clock = pygame.time.Clock()
tick = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_main_screen():
    screen.fill(pygame.Color("black"))
    all_blocks.draw(screen)
    all_enemies.draw(screen)
    all_hero.draw(screen)


class Player(pygame.sprite.Sprite):
    image = pygame.Surface([50, 100])
    image.fill(pygame.Color("red"))

    def __init__(self, x, y):
        super().__init__()
        self.vel_x = 5
        self.vel_y = 0
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.is_jump = False

    def gravity(self):
        if self.vel_y < MAX_VEL_Y:
            self.vel_y += 1
        self.rect.y += (-(self.vel_y ** 2) // GRAVITY if self.vel_y < 0 else (self.vel_y ** 2) // GRAVITY)

    def update(self, down, jump, left, right):
        def horizontal_collision():
            return 0 if pygame.sprite.spritecollideany(self, block_horizontal_borders) is None else 1

        def vertical_collision():
            return 0 if pygame.sprite.spritecollideany(self, block_vertical_borders) is None else 1

        if left:
            self.rect.x -= self.vel_x
            while vertical_collision():
                self.rect.x += 1
        if right:
            self.rect.x += self.vel_x
            while vertical_collision():
                self.rect.x -= 1
        if jump and not self.is_jump:
            self.vel_y = -MAX_VEL_Y * 2
            self.is_jump = True
        self.rect.y += 1
        if not self.is_jump and horizontal_collision():
            self.rect.y -= 1
            self.vel_y = 0
        self.gravity()
        if self.vel_y <= 0:
            while horizontal_collision():
                self.rect.y += 1
                self.is_jump = True
        else:
            while horizontal_collision():
                self.rect.y -= 1
                self.is_jump = False
        if down:
            pass

    def get_update(self, down=False, jump=False, left=False, right=False):
        self.update(down, jump, left, right)


class Block(pygame.sprite.Sprite):
    image = pygame.Surface([80, 40])
    image.fill(pygame.Color("white"))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Block.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        w, h = self.rect.w, self.rect.h
        border1 = Border(x, y, x, y + h)
        border2 = Border(x + w, y, x + w, y + h)
        border3 = Border(x, y, x + w, y)
        border4 = Border(x, y + h, x + w, y + h)
        block_vertical_borders.add(border1)
        block_vertical_borders.add(border2)
        block_horizontal_borders.add(border3)
        block_horizontal_borders.add(border4)
        # x, y, w, h = self.rect.x, self.rect.y, self.rect.w, self.rect.h


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        if x1 == x2:
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


running = True
all_hero = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
block_vertical_borders = pygame.sprite.Group()
block_horizontal_borders = pygame.sprite.Group()
hero = Player(0, 360)
all_hero.add(hero)
temp_x = 0
for i in range(5):
    block = Block(temp_x, 460)
    all_blocks.add(block)
    temp_x += 80
temp_x = 500
for i in range(4):
    block = Block(temp_x, 250)
    all_blocks.add(block)
    temp_x += 80

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    hero_left, hero_right, hero_jump = False, False, False
    if keys[pygame.K_LEFT]:
        hero_left = True
    if keys[pygame.K_RIGHT]:
        hero_right = True
    if keys[pygame.K_UP] and not hero.is_jump:
        hero_jump = True
    hero.get_update(left=hero_left, right=hero_right, jump=hero_jump)
    draw_main_screen()
    clock.tick(FPS)
    pygame.display.flip()
    tick += 1

pygame.quit()
