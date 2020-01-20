import pygame
import os
import random

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")

BLOCK_SIZE = 50  # размер одного блока
FALLING_SPEED = 1  # скорость падения на сколько меняется
FALLING_MAX = -5  # макс скорость падения


clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = FALLING_MAX
        self.rect = pygame.Rect(x - 1, y - 1, self.width + 2, self.height + 2)
        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE * 2])
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE * 2))


def draw_main_screen():
    screen.fill((0, 0, 0))
    all_entities.draw(screen)
    all_blocks.draw(screen)
    pygame.display.update()


def block_collision(item):  # проверка врезания
    # 0 - free falling | 1 - up | 3 - down | 2 - right | 4 - left|
    directions = []
    for blocc in pygame.sprite.spritecollide(item, all_blocks, 0):
        x = blocc.rect.x
        y = blocc.rect.y
        if y <= item.rect.y and x - item.rect.width + item.vel < item.rect.x < x + blocc.rect.width:
            directions.append(1)
            item.rect.y = y + blocc.rect.height
        elif y >= item.rect.y and x - item.rect.width + item.vel < item.rect.x < x + blocc.rect.width:
            directions.append(3)
            item.rect.y = y - item.rect.height + 1
        else:
            if item.rect.x < x:
                directions.append(2)
                item.rect.x = x - item.rect.width
            elif item.rect.x >= x:
                directions.append(4)
                item.rect.x = x + blocc.rect.width
    if 1 not in directions and 3 not in directions:
        directions.append(0)
        item.isJump = True
    return directions


def gravitation(item):  # движение предметов по игрику
    directions = block_collision(item)
    for dire in directions:
        if dire == 0:
            item.rect.y -= item.jumpCount
            if item.jumpCount > FALLING_MAX:
                item.jumpCount -= FALLING_SPEED
        elif dire == 1:
            item.jumpCount = -1
            item.rect.y -= item.jumpCount
        elif dire == 3 and item.isJump is True:
            item.isJump = False
            item.jumpCount = FALLING_MAX


running = True
hero = Player(0, 200, BLOCK_SIZE, BLOCK_SIZE * 2)

all_blocks = pygame.sprite.Group()
block = pygame.sprite.Sprite(all_blocks)
block.image = pygame.Surface([400, 50])
block.rect = pygame.Rect(0, 450, 400, 50)
pygame.draw.rect(block.image, pygame.Color("white"), (0, 0, 400, 50))

block2 = pygame.sprite.Sprite(all_blocks)
block2.image = pygame.Surface([100, 50])
block2.rect = pygame.Rect(400, 250, 100, 50)
pygame.draw.rect(block2.image, pygame.Color("white"), (0, 0, 100, 50))

all_entities = pygame.sprite.Group()

all_entities.add(hero)

hero_collision_direction = block_collision(hero)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and hero.rect.x > 0 and 4 not in hero_collision_direction:  # налево
        hero.rect.x -= hero.vel
        if hero.rect.x < 0:
            hero.rect.x = 0
    if keys[pygame.K_RIGHT] and hero.rect.x < size[0] - hero.width and 2 not in hero_collision_direction:  # направо
        hero.rect.x += hero.vel
        if hero.rect.x > size[0] - hero.width:
            hero.rect.x = size[0] - hero.width
    if not hero.isJump:  # прыжок
        if keys[pygame.K_SPACE]:
            hero.isJump = True
            hero.jumpCount = 20
            hero.rect.y -= 2
    for entity in all_entities:  # движение всех предметов по игрику
        gravitation(entity)
    draw_main_screen()



pygame.quit()