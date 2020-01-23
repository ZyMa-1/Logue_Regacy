import os
import sys
import pygame

pygame.init()
size = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")
overlapping_screen = pygame.Surface([800, 500], pygame.SRCALPHA)
overlapping_screen = overlapping_screen.convert_alpha()
ATTACK_TIME = 1000  # in milliseconds
ATTACK_COOLDOWN = 1000  # in milliseconds
BLOCK_SIZE = 50  # размер одного блока
FALLING_MAX = -10
FALLING_SPEED = 1
FPS = 60
clock = pygame.time.Clock()
"""
# - block
_ - platform
. - nothing
@ - player
@ - player
* - prujinka
one block - 50x50
"""

IMAGES = dict()


def draw_main_screen():
    the_big_screen.fill(pygame.Color("black"))
    if hero.is_attack:
        hero.def_attack()
        hero.attack.draw(the_big_screen)
    all_blocks.draw(the_big_screen)
    all_enemies.draw(the_big_screen)
    all_hero.draw(the_big_screen)
    all_prujinks.draw(the_big_screen)
    cutout_x, cutout_y = camera_adjustment()
    cutout = pygame.Rect(cutout_x, cutout_y, size[0], size[1])
    screen.blit(the_big_screen, (0, 0), cutout)
    screen.blit(overlapping_screen, (0, 0))
    pygame.display.flip()


def draw_overlapping_screen():
    overlapping_screen.blit(IMAGES["pause-icon"], (10, 10))
    overlapping_screen.blit(IMAGES[f"health_bar_{hero.hp}"], (80, 20))


def dist(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5


def camera_adjustment():
    x = round(hero.rect.x + 0.5 * hero.rect.w - size[0] * 0.5)
    y = round(hero.rect.y + 0.5 * hero.rect.h - size[1] * 0.5)
    if x < 0:
        x = 0
    elif x + size[0] > the_big_screen.get_width():
        x = the_big_screen.get_width() - size[0]
    if y < 0:
        y = 0
    elif y + size[1] > the_big_screen.get_height():
        y = the_big_screen.get_height() - size[1]
    return x, y


def start_menu():
    main_surface = pygame.Surface([800, 500])
    tick = 0
    ITALIC_FONT = "data\\CenturyGothic-Italic.ttf"
    intro_text = "Press any key to continue"
    fon = pygame.transform.scale(load_image('fon.jpg'), (800, 500))
    main_surface.blit(fon, (0, 0))
    font = pygame.font.Font(ITALIC_FONT, 20)
    intro_text_obj = font.render(intro_text, 1, pygame.Color("red"))
    main_surface.blit(intro_text_obj, (400 - intro_text_obj.get_width() // 2, 400 - intro_text_obj.get_height() // 2))
    main_surface.blit(IMAGES["settings"], (725, 425))
    main_surface.blit(IMAGES["leader_board"], (610, 410))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if dist(757, 457, x, y) <= 32:  # launch settings screen
                        return
                    if pygame.Rect.collidepoint(pygame.Rect(610, 410, 100, 100), x, y):  # launch leader_boards screen
                        return
        main_surface.set_alpha((tick ** 2) / 300)
        screen.blit(main_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        tick += 1


def pause():
    main_surface = pygame.Surface([400, 250])
    main_surface_dx = 200
    main_surface_dy = 125
    main_surface.fill(pygame.Color("blue"))
    for x in range(800):
        for y in range(500):
            r, g, b, a = screen.get_at((x, y))
            screen.set_at((x, y), pygame.Color(r // 3, g // 3, b // 3, a))
    resume_icon = load_image("continue-icon.png")
    resume_icon.convert_alpha()
    main_surface.blit(resume_icon, (168, 155))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x -= main_surface_dx
                y -= main_surface_dy
                if dist(x, y, 200, 189) <= 32:
                    return
        screen.blit(main_surface, (main_surface_dx, main_surface_dy))
        pygame.display.flip()
        clock.tick(FPS)


def horizontal_up_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_up_horizontal_borders) is None else 1


def horizontal_down_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_down_horizontal_borders) is None else 1


def vertical_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, block_vertical_borders) is None else 1


def platform_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, platform_horizontal_borders) is None else 1


def prujinka_collision(item):
    return 0 if pygame.sprite.spritecollideany(item, all_prujinks) is None else 1


def load_and_generate_map(filename):  # return hero
    filename = os.path.join("data", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(max(map(len, level_map)), 16)
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    height = max(10, len(level))
    player_flag = 0
    player_x, player_y = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Block(x, y)
            if level[y][x] == '@' and not player_flag:
                player_x, player_y = x, y
                player_flag = 1
            if level[y][x] == '_':
                Platform(x, y)
            if level[y][x] == '*':
                Prujinka(x, y)
    hero = Player(player_x, player_y)
    return hero, max_width, height


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
    if entity.prujinka_jump and entity.vel_y > 0:
        entity.rect.y -= entity.vel_y
        if entity.vel_y > FALLING_MAX:
            entity.vel_y -= FALLING_SPEED
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
    """print(platform_collision(entity.ground_border), platform_collision(entity), entity.ground_border.rect, 
    entity.rect) """
    if not platform_collision(entity.ground_border):
        entity.is_down = False
    if platform_collision(
            entity.ground_border) and entity.is_jump is True and entity.standing is False and not entity.is_down and entity.vel_y < 0:
        entity.is_jump = False
        entity.vel_y = FALLING_MAX
        while platform_collision(entity):
            entity.rect.y -= 1
            entity.standing = True
        entity.rect.y += 1
        return


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
        self.is_down = False
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)
        self.attack = self.attack = pygame.sprite.Group()
        self.is_attack = False
        self.hp = 3
        self.prujinka_jump = False

    def update(self):
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

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


class Invisible_Rect(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.image = pygame.Surface([0, 0])
        self.image.fill(pygame.Color("blue"))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)


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


class Platform(pygame.sprite.Sprite):
    image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE // 5])
    image.fill(pygame.Color("gray"))

    def __init__(self, x, y):
        super().__init__(all_blocks)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        w, h = self.rect.w, self.rect.h
        platform_horizontal_borders.add(Border(x, y, x + w - 2, y))


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_blocks)
        if x1 == x2:
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Prujinka(pygame.sprite.Sprite):
    image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE // 5])
    image.fill(pygame.Color("blue"))

    def __init__(self, x, y):
        super().__init__(all_blocks, all_prujinks)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        x += BLOCK_SIZE // 4
        y += (BLOCK_SIZE * 4 // 5)
        self.image = Prujinka.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


running = True
all_hero = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_prujinks = pygame.sprite.Group()
block_vertical_borders = pygame.sprite.Group()
block_down_horizontal_borders = pygame.sprite.Group()
block_up_horizontal_borders = pygame.sprite.Group()
platform_horizontal_borders = pygame.sprite.Group()
hero, level_width, level_height = load_and_generate_map("map.txt")
the_big_screen = pygame.Surface([level_height * BLOCK_SIZE, level_width * BLOCK_SIZE])
can_attack = True


def init_images():
    pause_icon = load_image("pause-icon.png").convert_alpha()  # 64x64
    settings_icon = load_image("settings.png").convert_alpha()
    leader_board_icon = load_image("leader_board_icon.png", (145, 160, 161)).convert_alpha()
    health_bar_0 = load_image("health_bar_0.png", (255, 255, 255)).convert_alpha()
    health_bar_1 = load_image("health_bar_1.png", (255, 255, 255)).convert_alpha()
    health_bar_2 = load_image("health_bar_2.png", (255, 255, 255)).convert_alpha()
    health_bar_3 = load_image("health_bar_3.png", (255, 255, 255)).convert_alpha()
    IMAGES["pause-icon"] = pause_icon
    IMAGES["health_bar_0"] = health_bar_0
    IMAGES["health_bar_1"] = health_bar_1
    IMAGES["health_bar_2"] = health_bar_2
    IMAGES["health_bar_3"] = health_bar_3
    IMAGES["settings"] = settings_icon
    IMAGES["leader_board"] = leader_board_icon


init_images()
start_menu()

draw_overlapping_screen()

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                if dist(x, y, 42, 42) <= 32:
                    pause()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pause()
    if keys[pygame.K_UP] and not hero.is_jump and (horizontal_up_collision(hero) or platform_collision(hero)):
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
    if keys[pygame.K_DOWN]:
        hero.is_down = True
    if keys[pygame.K_j] and can_attack and not hero.is_attack:
        hero.is_attack = True
        pygame.time.set_timer(1, ATTACK_TIME)
    if prujinka_collision(hero):
        hero.prujinka_jump = True
        hero.is_jump = True
        hero.standing = False
        hero.vel_y = - int(FALLING_MAX * 2.5)
    else:
        hero.prujinka_jump = False
    hero.update()
    gravitation(hero)
    draw_main_screen()
    draw_overlapping_screen()
    clock.tick(FPS)
    # pygame.draw.rect(screen, pygame.Color("green"), (hero.rect.x, hero.rect.y, hero.rect.width, hero.rect.height), 1)
    pygame.display.flip()

pygame.quit()
