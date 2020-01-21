import pygame
import os
import random

pygame.init()
size = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")

ATTACK_TIME = 1000  # in milliseconds
ATTACK_COOLDOWN = 1000  # in milliseconds
BLOCK_SIZE = 50  # размер одного блока
FALLING_MAX = -10
FALLING_SPEED = 1
FPS = 60
clock = pygame.time.Clock()
tick = 0
"""
# - block
_ - platform (coming soon...)
. - nothing
@ - player
@ - player
one block - 40x40
"""


def horizontal_up_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_up_horizontal_borders) is None else 1


def horizontal_down_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_down_horizontal_borders) is None else 1


def vertical_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_vertical_borders) is None else 1


def load_and_generate_map(filename):  # return hero
    filename = os.path.join("data", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    player_flag = 0
    player_x, player_y = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Block(x, y)
            if level[y][x] == '@' and not player_flag:
                player_x, player_y = x, y
                player_flag = 1
    hero = Player(player_x, player_y)
    return hero


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


def gravitation(entity):
    if horizontal_down_collision(entity):
        while horizontal_down_collision(entity):
            entity.rect.y += 1
        entity.vel_y = -1
        entity.rect.y -= entity.vel_y
    elif horizontal_up_collision(entity) and entity.is_jump is True and entity.standing is False:
        entity.is_jump = False
        entity.vel_y = FALLING_MAX
        while horizontal_up_collision(entity):
            entity.rect.y -= 1
            entity.standing = True
        entity.rect.y += 1
    elif not horizontal_down_collision(entity) and not horizontal_up_collision(entity):
        entity.standing = False
        entity.is_jump = True
        entity.rect.y -= entity.vel_y
        if entity.vel_y > FALLING_MAX:
            entity.vel_y -= FALLING_SPEED

        if horizontal_up_collision(entity):
            while horizontal_up_collision(entity):
                entity.rect.y -= 1
            entity.rect.y += 1
        elif horizontal_down_collision(entity):
            while horizontal_down_collision(entity):
                entity.rect.y += 1
            entity.vel_y = -1



def draw_main_screen():
    screen.fill(pygame.Color("black"))
    if hero.is_attack:
        hero.def_attack()
        hero.attack.draw(screen)
    all_blocks.draw(screen)
    all_enemies.draw(screen)
    all_hero.draw(screen)


class Player(pygame.sprite.Sprite):
    image = pygame.Surface([BLOCK_SIZE - 3, 2 * BLOCK_SIZE - 3])
    image.fill(pygame.Color("red"))

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_hero)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 5
        self.vel_y = FALLING_MAX
        self.rect = pygame.Rect(x, y, BLOCK_SIZE - 1, 2 * BLOCK_SIZE - 1)
        self.image = pygame.Surface([BLOCK_SIZE - 1, 2 * BLOCK_SIZE - 1])
        pygame.draw.rect(self.image, (255, 0, 0), (1, 1, BLOCK_SIZE - 2, BLOCK_SIZE * 2 - 2))
        self.is_jump = False
        self.right = True
        self.left = False
        self.standing = True
        self.attack = self.attack = pygame.sprite.Group()
        self.is_attack = False

    def def_attack(self):
        attack_sprite = pygame.sprite.Sprite()
        attack_sprite.image = pygame.Surface([BLOCK_SIZE - 2, 2 * BLOCK_SIZE - 2])
        pygame.draw.rect(attack_sprite.image, (0, 0, 255), (0, 0, BLOCK_SIZE - 2, BLOCK_SIZE * 2 - 2))
        if self.right:
            attack_sprite.rect = pygame.Rect(self.rect.x + self.rect.w - 1, self.rect.y + 1, BLOCK_SIZE - 2,
                                             2 * BLOCK_SIZE - 2)
        else:
            attack_sprite.rect = pygame.Rect(self.rect.x - self.rect.w + 2, self.rect.y + 1, BLOCK_SIZE - 2,
                                             2 * BLOCK_SIZE - 2)
        self.attack.empty()
        self.attack.add(attack_sprite)

    def update(self, down=False):
        if down:
            pass


class Block(pygame.sprite.Sprite):
    image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
    image.fill(pygame.Color("white"))

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_blocks)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.image = Block.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        w, h = self.rect.w, self.rect.h
        block_vertical_borders.add(Border(x, y + 1, x, y + h - 2))
        block_vertical_borders.add(Border(x + w, y + 1, x + w, y + h - 2))
        block_up_horizontal_borders.add(Border(x + 1, y, x + w - 2, 1))
        block_down_horizontal_borders.add(Border(x + 1, y + h, x + w - 2, 1))
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
block_down_horizontal_borders = pygame.sprite.Group()
block_up_horizontal_borders = pygame.sprite.Group()
hero = load_and_generate_map("map.txt")
can_attack = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == 1:
            if hero.is_attack:
                hero.is_attack = False
                can_attack = False
                pygame.event.clear(1)
                pygame.time.set_timer(1, ATTACK_COOLDOWN)
            else:
                can_attack = True
                pygame.event.clear(1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not hero.is_jump and pygame.sprite.spritecollideany(hero, block_up_horizontal_borders):
        hero.is_jump = True
        hero.vel_y = -(FALLING_MAX * 2)
        hero.rect.y -= 2
        hero.standing = False
    if keys[pygame.K_LEFT]:
        hero.left = True
        hero.right = False
        hero.rect.x -= hero.vel_x
        while vertical_collision(hero):
            hero.rect.x += 1
    if keys[pygame.K_RIGHT]:
        hero.left = False
        hero.right = True
        hero.rect.x += hero.vel_x
        while vertical_collision(hero):
            hero.rect.x -= 1
    if keys[pygame.K_j] and can_attack and not hero.is_attack:
        hero.is_attack = True
        pygame.time.set_timer(1, ATTACK_TIME)
    hero.update()
    gravitation(hero)
    draw_main_screen()
    clock.tick(FPS)
    pygame.display.flip()
    tick += 1

pygame.quit()