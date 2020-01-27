import os
import sys
import pygame
import random

pygame.init()
size = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")
overlapping_screen = pygame.Surface([size[0], size[1]], pygame.SRCALPHA)
overlapping_screen = overlapping_screen.convert_alpha()
ATTACK_TIME = 100  # in milliseconds
ATTACK_COOLDOWN = 100  # in milliseconds
ATTACK_SWING = 100  # in milliseconds
BLOCK_SIZE = 50  # размер одного блока
FALLING_MAX = -10
FALLING_SPEED = 1
FPS = 60
CURRENT_MAP = 0
gold = 0
DIRECTIONS = {
    "left": 1,
    "up": 2,
    "right": 3,
    "down": 4
}
clock = pygame.time.Clock()
"""
# block
_ platform
. nothing
* - prujinka
@ player
@ player
- vertical_border
- vertical_border
- - horizontal_border
one block - 50x50
"""

IMAGES = dict()


def draw_main_screen():
    the_big_screen.fill(pygame.Color("black"))
    if hero.attack_type != 0:
        hero.def_attack()
        hero.attack.draw(the_big_screen)
    all_blocks.draw(the_big_screen)
    all_enemies_sprite.draw(the_big_screen)
    all_hero.draw(the_big_screen)
    the_big_screen.blit(hero.attack_image.image, (hero.attack_image.rect.x, hero.attack_image.rect.y))
    all_projectiles_sprite.draw(the_big_screen)
    all_npcs.draw(the_big_screen)
    cutout_x, cutout_y = camera_adjustment()
    cutout = pygame.Rect(cutout_x, cutout_y, size[0], size[1])
    screen.blit(the_big_screen, (0, 0), cutout)
    screen.blit(overlapping_screen, (0, 0))
    pygame.display.flip()


def draw_overlapping_screen():
    overlapping_screen.fill(pygame.SRCALPHA)
    overlapping_screen.blit(IMAGES["pause-icon"], (10, 10))
    overlapping_screen.blit(hero.draw_health(), (80, 26))
    overlapping_screen.blit(gold_display(), (674, 10))
    overlapping_screen.blit(score_text, (674, 26))
    overlapping_screen.blit(tutorial_board, (624, 100))


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


def create_text(text, font, font_size, color, underline=False):
    font = pygame.font.Font(font, font_size)
    font.set_underline(underline)
    text_obj = font.render(text, 1, color)
    return text_obj


def start_menu():
    def draw_main_surface():
        main_surface.fill(pygame.Color("black"))
        main_surface.blit(fon, (0, 0))
        main_surface.blit(IMAGES["settings"], (725, 425))
        main_surface.blit(IMAGES["leader_board"], (610, 410))
        play_button.draw(main_surface, pygame.mouse.get_pos())

    main_surface = pygame.Surface([size[0], size[1]])
    tick = 0
    fon = pygame.transform.scale(load_image('fon.jpg'), (size[0], size[1]))
    intro_text = create_text("Play", "data\\CenturyGothic-Bold.ttf", 30, pygame.Color(18, 196, 30), 5)
    intro_text_cover = create_text("Play", "data\\CenturyGothic-Bold.ttf", 39, pygame.Color(18, 196, 30), 5)
    play_button = Button(400 - intro_text.get_width() // 2, 380 - intro_text.get_height() // 2, intro_text,
                         intro_text_cover)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if dist(757, 457, x, y) <= 32:  # launch settings screen
                        return
                    if pygame.Rect.collidepoint(pygame.Rect(610, 410, 100, 100), x, y):  # launch leader_boards screen
                        leader_board()
                    if play_button.is_cover((x, y)):
                        return
        main_surface.set_alpha((tick ** 2) / 300)
        draw_main_surface()
        screen.blit(main_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        tick += 1


def pause():
    def draw_main_surface():
        main_surface.fill(pygame.Color("blue"))
        cutout_x, cutout_y = camera_adjustment()
        cutout = pygame.Rect(cutout_x, cutout_y, size[0], size[1])
        screen.blit(the_big_screen, (0, 0), cutout)
        x, y = pygame.mouse.get_pos()
        x -= main_surface_dx
        y -= main_surface_dy
        continue_button.draw(main_surface, (x, y))
        restart_button.draw(main_surface, (x, y))
        exit_button.draw(main_surface, (x, y))
        screen.blit(main_surface, (main_surface_dx, main_surface_dy))
        draw_overlapping_screen()

    main_surface = pygame.Surface([400, 250]).convert_alpha()
    main_surface_dx = 200
    main_surface_dy = 125
    main_surface.fill(pygame.Color("blue"))
    continue_text = create_text("Continue", "data\\CenturyGothic-Bold.ttf", 31, pygame.Color(18, 196, 30), 5)
    continue_text_cover = create_text("Continue", "data\\CenturyGothic-Bold.ttf", 35, pygame.Color(18, 196, 30), 5)
    continue_button = Button(200 - continue_text.get_width() // 2, 50 - continue_text.get_height() // 2, continue_text,
                             continue_text_cover)
    restart_text = create_text("Restart", "data\\CenturyGothic-Bold.ttf", 31, pygame.Color(18, 196, 30), 5)
    restart_text_cover = create_text("Restart", "data\\CenturyGothic-Bold.ttf", 35, pygame.Color(18, 196, 30), 5)
    restart_button = Button(200 - restart_text.get_width() // 2, 120 - restart_text.get_height() // 2, restart_text,
                            restart_text_cover)
    exit_text = create_text("Save and exit", "data\\CenturyGothic-Bold.ttf", 31, pygame.Color(18, 196, 30), 5)
    exit_text_cover = create_text("Save and exit", "data\\CenturyGothic-Bold.ttf", 35, pygame.Color(18, 196, 30), 5)
    exit_button = Button(200 - exit_text.get_width() // 2, 190 - exit_text.get_height() // 2, exit_text,
                         exit_text_cover)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x -= main_surface_dx
                y -= main_surface_dy
                if continue_button.is_cover((x, y)):
                    return
        draw_main_surface()
        pygame.display.flip()
        clock.tick(FPS)


def leader_board():
    scroll_y = 0
    tick = 0
    screen.fill(pygame.Color("black"))
    filename = os.path.join("data", "leader_board.txt")
    with open(filename, 'r') as mapFile:
        leaders = [line.strip() for line in mapFile]
    leaders = list(map(lambda x: x.split('-'), leaders))
    leaders.sort(key=lambda x: int(x[1]), reverse=True)
    leaders.insert(0, ['Player', 'Score'])
    font = pygame.font.Font("data\\CenturyGothic.ttf", 30)
    all_text = []
    for i in range(len(leaders)):
        text1 = font.render(leaders[i][0], 1, pygame.Color("white"))
        text2 = font.render(leaders[i][1], 1, pygame.Color("white"))
        all_text.append([text1, text2])
    tile_width, tile_height = max(map(lambda x: max(x[0].get_width(), x[1].get_width()), all_text)), max(
        map(lambda x: max(x[0].get_height(), x[1].get_height()), all_text))
    tile_width += 30
    tile_height += 30
    main_surface = pygame.Surface([tile_width * 2 + 10, tile_height * len(leaders) + 10])
    x = 6
    y = 6
    for i in range(len(leaders)):
        pygame.draw.rect(main_surface, pygame.Color("red"), (x, y, tile_width, tile_height), 5)
        main_surface.blit(all_text[i][0], (x + (tile_width - all_text[i][0].get_width()) // 2, y + 15))
        x += tile_width
        pygame.draw.rect(main_surface, pygame.Color("red"), (x, y, tile_width, tile_height), 5)
        main_surface.blit(all_text[i][1], (x + (tile_width - all_text[i][1].get_width()) // 2, y + 15))
        x -= tile_width
        y += tile_height
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 5 and tile_height * len(leaders) - 395 - scroll_y >= 0:
                    scroll_y += 20
                if event.button == 4 and scroll_y > 0:
                    scroll_y -= 20
                if event.button == 1 and dist(x, y, 52, 52) <= 32:
                    return
        screen.fill(pygame.Color("black"))
        main_surface.set_alpha((tick ** 2))
        IMAGES["back_arrow"].set_alpha((tick ** 2) / 300)
        screen.blit(main_surface, (400 - tile_width, 55 - scroll_y))
        screen.blit(IMAGES["back_arrow"], (20, 20))
        pygame.display.flip()
        clock.tick(FPS)
        tick += 1


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


def ladder_collision(item):
    return 1 if pygame.sprite.spritecollideany(item, all_ladders, pygame.sprite.collide_mask) else 0


def load_and_generate_map(filename, new_pos=None):
    map_x, map_y = 0, 0
    if filename != "map.txt":
        map_x, map_y = int(filename.split('_')[1]), int(filename.split('_')[2].strip('.txt'))
    if map_x == 3 and map_y == 3:
        filename = os.path.join("data", "maps", "boss_room.txt")
    else:
        filename = os.path.join("data", "maps", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    true_width, true_height = max(map(len, level_map)), len(level_map)
    max_width = max(true_width, 17)
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    max_height = max(true_height, 11)
    player_flag = 0
    player_x, player_y = 0, 0
    next_levels_pos = {
        DIRECTIONS["up"]: None,
        DIRECTIONS["down"]: None,
        DIRECTIONS["right"]: None,
        DIRECTIONS["left"]: None
    }
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Block(x, y)
            if level[y][x] == '@' and new_pos is None and not player_flag:
                player_x, player_y = x, y
                player_flag = 1
            if level[y][x] == '_':
                Platform(x, y)
            if level[y][x] == '*':
                Prujinka(x, y)
            if level[y][x] == '/':
                Ladder(x, y, angle=45)
            if level[y][x] == '\\':
                Ladder(x - 1, y, angle=-45)
            if level[y][x] == '-':
                if y == 0 or y == len(level) - 1:
                    if x > 0 and level[y][x - 1] != '-':
                        if filename != "data\\maps\\map.txt" and (y == 0 and map_x == 3) or (
                                y == true_height - 1 and map_x == 1):  # 3 - all_map height (3x3)
                            Block(x, y)
                            Block(x + 1, y)
                            continue
                        Next_level_horizontal_border(x, y)
                        Platform(x, y)
                        Platform(x + 1, y)
                        if y == 0:
                            next_levels_pos[DIRECTIONS["up"]] = (x, y)
                        else:
                            next_levels_pos[DIRECTIONS["down"]] = (x, y)
                else:
                    if y > 0 and level[y - 1][x] != '-':
                        if filename != "map.txt" and (x == 0 and map_y == 1) or (
                                x == true_width - 1 and map_y == 3):  # 3 - all_map height (3x3)
                            if filename.split('\\')[-1] == 'map_1_1.txt' and new_pos == DIRECTIONS["left"]:
                                if x == 0:
                                    next_levels_pos[DIRECTIONS["left"]] = (x, y)
                                else:
                                    next_levels_pos[DIRECTIONS["right"]] = (x, y)
                            Block(x, y)
                            Block(x, y + 1)
                            continue
                        Next_level_vertical_border(x, y)
                        if x == 0:
                            next_levels_pos[DIRECTIONS["left"]] = (x, y)
                        else:
                            next_levels_pos[DIRECTIONS["right"]] = (x, y)
    number_of_enemies = random.randint(max(1, map_x + map_y - 1), max(1, (map_x + map_y - 1)) * 2)
    enemies_pos = set()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if y > 0 and (level[y][x] == ' ' or level[y][x] == '.'):
                enemies_pos.add((x, y))
    for i in enemies_pos:
        if number_of_enemies == 0:
            break
        x, y = i
        all_enemies.append(random.choice(enemy_types)(x, y, BLOCK_SIZE, BLOCK_SIZE))
        number_of_enemies -= 1
    if player_x == 0 and player_y == 0:
        player_x, player_y = next_levels_pos[new_pos]
        if new_pos == DIRECTIONS["left"]:
            player_x += 1
        if new_pos == DIRECTIONS["right"]:
            player_x -= 1
        if new_pos == DIRECTIONS["up"]:
            player_y += 2
        if new_pos == DIRECTIONS["down"]:
            player_y -= 2
    hero = Player(player_x, player_y)
    return hero, max_width, max_height, next_levels_pos, true_width, true_height


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


class Button:
    def __init__(self, x, y, text, text_cover):  # coordinates in pixels
        self.text = text
        self.text_cover = text_cover
        self.text_w, self.text_h = text.get_width(), text.get_height()
        self.text_cover_w, self.text_cover_h = text_cover.get_width(), text_cover.get_height()
        self.rect = pygame.Rect(x, y, text.get_width() + 2, text.get_height() + 2)
        self.rect_cover = pygame.Rect(x - (self.text_cover_w - self.text_w) // 2,
                                      y - (self.text_cover_h - self.text_h) // 2, text_cover.get_width() + 2,
                                      text_cover.get_height() + 2)
        self.cover = False

    def is_cover(self, pos):
        x, y = pos
        if not self.cover:
            temp = self.rect.collidepoint(x, y)
            self.cover = temp
            return temp
        else:
            temp = self.rect_cover.collidepoint(x, y)
            self.cover = temp
            return temp

    def draw(self, surface, pos):  # mouse_pos
        if self.is_cover(pos):
            surface.blit(self.text, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.text_cover, (self.rect_cover.x, self.rect_cover.y))


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


class Next_level_vertical_border(pygame.sprite.Sprite):
    image = pygame.Surface([int(BLOCK_SIZE * 0.6), BLOCK_SIZE * 2])
    image.fill(pygame.Color("yellow"))

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_blocks, next_level_vertical_border_group)

        # relative directions(relative to current level)

        if x == 0:
            self.direction = DIRECTIONS["left"]
        else:
            self.direction = DIRECTIONS["right"]
        self.pos = (x, y)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        x += BLOCK_SIZE // 5
        self.image = Next_level_vertical_border.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Next_level_horizontal_border(pygame.sprite.Sprite):
    image = pygame.Surface([BLOCK_SIZE * 2, int(BLOCK_SIZE * 0.6)])
    image.fill(pygame.Color("yellow"))

    def __init__(self, x, y):
        super().__init__(all_blocks, next_level_horizontal_border_group)

        # relative directions(relative to current level)

        if y == 0:
            self.direction = DIRECTIONS["up"]
        else:
            self.direction = DIRECTIONS["down"]
        self.pos = (x, y)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        y += BLOCK_SIZE // 5
        self.image = Next_level_horizontal_border.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Ladder(pygame.sprite.Sprite):
    side_len = round(BLOCK_SIZE * (2 ** .5))
    image = pygame.Surface([side_len, side_len], pygame.SRCALPHA)
    image.fill(pygame.Color("purple"))

    def __init__(self, x, y, angle):
        super().__init__(all_blocks, all_ladders)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.pos = (x, y)
        self.image = Ladder.image.convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, angle, 1)
        self.rect = self.image.get_rect(center=(x + BLOCK_SIZE + 1, y + BLOCK_SIZE))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)

def gold_display():
    coin_image = load_image(os.path.join("entity_images\\Coin.png")).convert_alpha()
    gold_text = create_text(str(gold), os.path.join("data\\CenturyGothic-Bold.ttf"), 16, pygame.Color("white"))
    gold_surface = pygame.Surface([102, 16])
    gold_surface.fill(pygame.SRCALPHA)
    gold_surface.blit(coin_image, (0, 0))
    gold_surface.blit(gold_text, (22, -3))
    return gold_surface



# ---------------------------------------------ENTITY------------------------------------------------------------------
def damage_check():
    if len(hero.attack.sprites()) > 0:
        for enemy in pygame.sprite.spritecollide(hero.attack.sprites()[0], all_enemies_sprite, False):
            if enemy.i_frames == 0:
                dir = "right"
                if hero.rect.x > enemy.rect.x:
                    dir = "left"
                enemy.take_damage(dir)
    if hero.knocked_back is False and hero.i_frames == 0:
        for enemy in pygame.sprite.spritecollide(hero, all_enemies_sprite, False):
            dir = "right"
            if enemy.rect.x > hero.rect.x:
                dir = "left"
            hero.take_damage(enemy.attack_damage, dir)
        for projectile in pygame.sprite.spritecollide(hero, all_projectiles_sprite, False):
            dir = "right"
            if projectile.rect.x > hero.rect.x:
                dir = "left"
            hero.take_damage(projectile.attack_damage, dir)
            all_projectiles.remove(projectile)
            all_projectiles_sprite.remove(projectile)


class OmniTurret(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\OmniTurret\\idle.png")).convert_alpha()
    image_projectile = load_image(os.path.join("entity_images\\Projectiles\\OmniTurret.png")).convert_alpha()

    def __init__(self, x, y, a, b):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE

        self.rect = pygame.Rect(x, y, 300 - 1, 300 - 1)
        self.image = pygame.Surface([300 - 2, 300 - 2])
        self.image.blit(OmniTurret.image_idle, (0, 1))

        self.score_reward = 1000
        self.gold_reward = 1000

        self.shot_damage = 40
        self.shot_cooldown = 150
        self.shot_speed = 3

        self.attack_damage = 30
        self.i_frames = 0

        self.hp = 150
        self.max_hp = 150

    def shoot(self):
        projectile_list = []
        projl1 = (self.rect.x - 24, self.rect.y + round(self.rect.h / 3), 24, 24, OmniTurret.image_projectile,
                           self.shot_speed, self.shot_damage, ["left"])
        projectile_list.append(projl1)

        projl2 = (self.rect.x - 24, self.rect.y + round(self.rect.h / 3) + 74, 24, 24, OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["left"])
        projectile_list.append(projl2)

        projr1 = (self.rect.x + self.rect.w, self.rect.y + round(self.rect.h / 3), 24, 24, OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["right"])
        projectile_list.append(projr1)

        projr2 = (self.rect.x + self.rect.w, self.rect.y + round(self.rect.h / 3) + 74, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["right"])
        projectile_list.append(projr2)

        proju1 = (self.rect.x + round(self.rect.w / 3), self.rect.y - 24, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["up"])
        projectile_list.append(proju1)

        proju2 = (self.rect.x + round(self.rect.w / 3) + 74, self.rect.y - 24, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["up"])
        projectile_list.append(proju2)

        projd1 = (self.rect.x + round(self.rect.w / 3), self.rect.y + self.rect.h, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["down"])
        projectile_list.append(projd1)

        projd2 = (self.rect.x + round(self.rect.w / 3) + 74, self.rect.y + self.rect.h, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["down"])
        projectile_list.append(projd2)

        proj_leftup1 = (self.rect.x + 20, self.rect.y - 20, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["left", "up"])
        projectile_list.append(proj_leftup1)

        proj_leftup2 = (self.rect.x - 30, self.rect.y + 30, 24, 24,
                            OmniTurret.image_projectile,
                            self.shot_speed, self.shot_damage, ["left", "up"])
        projectile_list.append(proj_leftup2)

        proj_leftdown1 = (self.rect.x + 20 + 15, self.rect.y - 20 + 320, 24, 24,
                                  OmniTurret.image_projectile,
                                  self.shot_speed, self.shot_damage, ["left", "down"])
        projectile_list.append(proj_leftdown1)
        proj_leftdown2 = (self.rect.x - 30 + 15, self.rect.y + 220 + 30, 24, 24,
                                  OmniTurret.image_projectile,
                                  self.shot_speed, self.shot_damage, ["left", "down"])
        projectile_list.append(proj_leftdown2)

        proj_rightup1 = (self.rect.x + 20 + 260, self.rect.y + 30, 24, 24,
                                  OmniTurret.image_projectile,
                                  self.shot_speed, self.shot_damage, ["right", "up"])
        projectile_list.append(proj_rightup1)
        proj_rightup2 = (self.rect.x - 30 + 280, self.rect.y - 10, 24, 24,
                                  OmniTurret.image_projectile,
                                  self.shot_speed, self.shot_damage, ["right", "up"])
        projectile_list.append(proj_rightup2)

        proj_rightdown1 = (self.rect.x + 20 + 260, self.rect.y + 30 + 220, 24, 24,
                                   OmniTurret.image_projectile,
                                   self.shot_speed, self.shot_damage, ["right", "down"])
        projectile_list.append(proj_rightdown1)
        proj_rightdown2 = (self.rect.x - 30 + 280, self.rect.y - 10 + 300, 24, 24,
                                   OmniTurret.image_projectile,
                                   self.shot_speed, self.shot_damage, ["right", "down"])
        projectile_list.append(proj_rightdown2)

        for i in range(8):
            asd = random.choice(projectile_list)
            pro = Projectile(asd[0], asd[1], asd[2], asd[3], asd[4], asd[5], asd[6], asd[7])
            all_projectiles_sprite.add(pro)
            all_projectiles.append(pro)

    def update(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.shot_cooldown == 0:
            self.shoot()
            self.shot_cooldown = 150
        if self.i_frames > 0:
            self.i_frames -= 1

    def take_damage(self, direction):
        self.i_frames = 20
        self.hp -= hero.attack_damage
        if hero.attack_type == 2:
            hero.vel_y = 12
            hero.is_jump = True
            hero.standing = False
            hero.jump_amount -= 1
        if self.hp <= 0:
            self.death()

    def draw_health(self):
        health_surface = pygame.Surface([round(2 * self.max_hp) + 140, 32])
        if self.hp > 0:
            pygame.draw.rect(health_surface, pygame.Color("red"),
                            (140, 0, round(round(2 * self.max_hp) / self.max_hp * self.hp),
                            health_surface.get_height()))
        pygame.draw.rect(health_surface, pygame.Color("green"),
                         (140, 0, round(round(2 * self.max_hp)),
                          health_surface.get_height()), 1)
        hp_text = create_text("{}/{}".format(self.hp, self.max_hp), "data\\CenturyGothic-Bold.ttf", 20,
                            pygame.Color("white"))
        boss_text = create_text("OMNI-TURRET:", "data\\CenturyGothic-Bold.ttf", 20,
                            pygame.Color("white"))
        health_surface.blit(boss_text, (0, 0))
        health_surface.blit(hp_text, (146, 2))
        return health_surface

    def death(self):
        global gold
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)
        self.kill()
        gold += self.gold_reward
        hero.score += self.score_reward


class Trader(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\Trader\\idle.png")).convert_alpha()

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_npcs)

        x *= BLOCK_SIZE
        y *= BLOCK_SIZE

        self.rect = pygame.Rect(x, y, 155, 300)
        self.image = pygame.Surface([155, 300])
        self.image.blit(Trader.image_idle , (0, 0))

    def update(self):
        if pygame.sprite.spritecollideany(self, all_hero):
            if hero.talk:
                pass
                "МЕНЮШКА ТУТ"


class Gopnik(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\Gopnik\\gopnik.png")).convert_alpha()

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_npcs)

        x *= BLOCK_SIZE
        y *= BLOCK_SIZE

        self.rect = pygame.Rect(x, y, 48, 48)
        self.image = pygame.Surface([48, 48])
        self.image.blit(pygame.transform.flip(Gopnik.image_idle, 1, 0) , (0, 0))

    def update(self):
        global gold
        if pygame.sprite.spritecollideany(self, all_hero):
            gold = gold * hero.gop_stop
            all_npcs.remove(self)
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, wi, he, image, vel_x, damage, directions):  # coordinates not in pixels
        super().__init__()
        self.vel_x = vel_x

        self.rect = pygame.Rect(x, y, wi, he)
        self.image = pygame.Surface([wi, he])
        self.image.blit(image, (0, 0))

        self.up = False
        self.down = False
        self.right = False
        self.left = False

        for dir in directions:
            if dir == "right":
                self.right = True
                self.left = False
                self.image.fill(pygame.SRCALPHA)
                self.image.blit(pygame.transform.flip(image, 1, 0), (0, 0))
            elif dir == "left":
                self.right = False
                self.left = True
            elif dir == "up":
                self.up = True
            elif dir == "down":
                self.down = True

        self.attack_damage = damage

    def update(self):
        if self.right:
            self.rect.x += self.vel_x
        if self.left:
            self.rect.x -= self.vel_x
        if self.up:
            self.rect.y -= self.vel_x
        if self.down:
            self.rect.y += self.vel_x
        if vertical_collision(self) or horizontal_up_collision(self) or horizontal_down_collision(self) or platform_collision(self) or pygame.sprite.spritecollideany(self, next_level_vertical_border_group):
            all_projectiles.remove(self)
            all_projectiles_sprite.remove(self)
            self.kill()


class QuadraTurret(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\QuadraTurret\\idle.png")).convert_alpha()
    image_projectile = load_image(os.path.join("entity_images\\Projectiles\\Turret.png")).convert_alpha()

    def __init__(self, x, y, wi, he):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE

        self.rect = pygame.Rect(x, y, wi - 1, he - 1)
        self.image = pygame.Surface([wi - 2, he - 2])
        self.image.blit(QuadraTurret.image_idle, (0, 1))

        self.score_reward = 200
        self.gold_reward = 20

        self.shot_damage = 20
        self.shot_cooldown = 300
        self.shot_speed = 7

        self.attack_damage = 5
        self.i_frames = 0

        self.hp = 2

    def shoot(self):
        projl = Projectile(self.rect.x - 16, self.rect.y + round(self.rect.h / 3), 16, 16, Turret.image_projectile, self.shot_speed, self.shot_damage, ["left"])
        all_projectiles_sprite.add(projl)
        all_projectiles.append(projl)
        projr = Projectile(self.rect.x + self.rect.w + 16, self.rect.y + round(self.rect.h / 3), 16, 16, pygame.transform.flip(Turret.image_projectile, 1, 0),
                          self.shot_speed, self.shot_damage, ["right"])
        all_projectiles_sprite.add(projr)
        all_projectiles.append(projr)
        projd = Projectile(self.rect.x + 16, self.rect.y + self.rect.h, 16, 16, Turret.image_projectile,
                          self.shot_speed, self.shot_damage, ["down"])
        all_projectiles_sprite.add(projd)
        all_projectiles.append(projd)
        proju = Projectile(self.rect.x + 16, self.rect.y, 16, 16, Turret.image_projectile,
                          self.shot_speed, self.shot_damage, ["up"])
        all_projectiles_sprite.add(proju)
        all_projectiles.append(proju)

    def update(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.shot_cooldown == 0:
            self.shoot()
            self.shot_cooldown = 300
        if self.i_frames > 0:
            self.i_frames -= 1

    def take_damage(self, direction):
        self.i_frames = 20
        self.hp -= hero.attack_damage
        if hero.attack_type == 2:
            hero.vel_y = 12
            hero.is_jump = True
            hero.standing = False
            hero.jump_amount -= 1
        if self.hp <= 0:
            self.death()

    def death(self):
        global gold
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)
        self.kill()
        gold += self.gold_reward
        hero.score += self.score_reward


class Turret(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\Turret\\idle.png")).convert_alpha()
    image_projectile = load_image(os.path.join("entity_images\\Projectiles\\Turret.png")).convert_alpha()

    def __init__(self, x, y, wi, he):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, wi - 1, he - 1)
        self.image = pygame.Surface([wi - 2, he - 2])
        self.image.blit(Turret.image_idle, (0, 1))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False

        self.score_reward = 150
        self.gold_reward = 15

        self.is_jump = False
        self.standing = True
        self.is_down = False

        self.shot_damage = 20
        self.shot_cooldown = 150
        self.vel_x = 8

        self.attack = pygame.sprite.Group()
        self.attack_damage = 2
        self.i_frames = 0

        self.hp = 5

    def shoot(self):
        dir = "left"
        image = Turret.image_projectile
        x = self.rect.x - 16
        y = self.rect.y + round(self.rect.h / 3)
        if self.right:
            dir = "right"
            image = pygame.transform.flip(image, 1, 0)
            x = self.rect.x + self.rect.w + 16
        proj = Projectile(x, y, 16, 16, image, self.vel_x, self.shot_damage, [dir])
        all_projectiles_sprite.add(proj)
        all_projectiles.append(proj)

    def update(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.shot_cooldown == 0:
            self.shoot()
            self.shot_cooldown = 150
        if hero.rect.x >= self.rect.x:
            self.right = True
            self.left = False
            self.image.fill(pygame.SRCALPHA)
            self.image.blit(pygame.transform.flip(Turret.image_idle, 1, 0), (0, 1))
        else:
            self.right = False
            self.left = True
            self.image.fill(pygame.SRCALPHA)
            self.image.blit(Turret.image_idle, (0, 1))
        if self.i_frames > 0:
            self.i_frames -= 1


        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        if horizontal_down_collision(self):
            while horizontal_down_collision(self):
                self.rect.y += 1
            self.vel_y = -1
            self.rect.y -= self.vel_y
        elif horizontal_up_collision(self) and self.is_jump is True and self.standing is False:
            self.is_jump = False
            self.vel_y = FALLING_MAX
            while horizontal_up_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        elif not horizontal_down_collision(self) and not horizontal_up_collision(self):
            self.standing = False
            self.is_jump = True
            self.rect.y -= self.vel_y
            if self.vel_y > FALLING_MAX:
                self.vel_y -= FALLING_SPEED

            if horizontal_up_collision(self):
                while horizontal_up_collision(self):
                    self.rect.y -= 1
                self.rect.y += 1
            elif horizontal_down_collision(self):
                while horizontal_down_collision(self):
                    self.rect.y += 1
                self.vel_y = -1
        if platform_collision(
                self.ground_border) and self.is_jump is True and self.standing is False and not self.is_down and self.vel_y < 0:
            self.is_jump = False
            self.vel_y = FALLING_MAX
            while platform_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1

    def take_damage(self, direction):
        self.i_frames = 20
        self.hp -= hero.attack_damage
        if hero.attack_type == 2:
            hero.vel_y = 12
            hero.is_jump = True
            hero.standing = False
            hero.jump_amount -= 1
        if self.hp <= 0:
            self.death()

    def death(self):
        global gold
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)
        self.kill()
        gold += self.gold_reward
        hero.score += self.score_reward


class JumpTurret(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\JumpTurret\\idle.png")).convert_alpha()
    image_move = load_image(os.path.join("entity_images\\JumpTurret\\move.png")).convert_alpha()
    image_projectile = load_image(os.path.join("entity_images\\Projectiles\\Turret.png")).convert_alpha()

    def __init__(self, x, y, wi, he):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 7
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, wi - 1, he - 1)
        self.image = pygame.Surface([wi - 2, he - 2])
        self.image.blit(JumpTurret.image_idle, (0, 1))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False

        self.score_reward = 250
        self.gold_reward = 25

        self.is_jump = False
        self.standing = True
        self.is_down = False
        self.jump_cooldown = 100

        self.attack_type = 0
        self.attack = pygame.sprite.Group()
        self.attack_damage = 10
        self.i_frames = 0
        self.knocked_back = False

        self.shot_damage = 20
        self.shot_cooldown = 250
        self.shot_speed = 10

        self.hp = 6

    def jump(self):
        if self.standing and not self.is_jump:
            self.jump_cooldown = 100
            self.is_jump = True
            self.vel_y = -((hero.rect.y - self.rect.y) // 4)
            if self.vel_y < 0:
                self.vel_y = 10
            elif self.vel_y > -round(FALLING_MAX * 2.2):
                self.vel_y = -round(FALLING_MAX * 2.2)
            self.rect.y -= 2
            self.standing = False

    def logic(self):
        if hero.rect.x >= self.rect.x:
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        if hero.rect.y >= self.rect.y + self.rect.h:
            self.is_down = True
        else:
            self.is_down = False

    def shoot(self):
        dir = "left"
        image = JumpTurret.image_projectile
        x = self.rect.x - 16
        y = self.rect.y + round(self.rect.h / 3)
        if self.right:
            dir = "right"
            image = pygame.transform.flip(image, 1, 0)
            x = self.rect.x + self.rect.w + 16
        proj = Projectile(x, y, 16, 16, image, self.shot_speed, self.shot_damage, [dir])
        all_projectiles_sprite.add(proj)
        all_projectiles.append(proj)

    def update(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.shot_cooldown == 0:
            self.shoot()
            self.shot_cooldown = 250

        if self.standing:
            self.image.fill(pygame.SRCALPHA)
            if self.right:
                self.image.blit(pygame.transform.flip(JumpTurret.image_idle, 1, 0), (0, 1))
            else:
                self.image.blit(JumpTurret.image_idle, (0, 1))
        else:
            self.image.fill(pygame.SRCALPHA)
            if self.right:
                self.image.blit(pygame.transform.flip(JumpTurret.image_move, 1, 0), (0, 1))
            else:
                self.image.blit(JumpTurret.image_move, (0, 1))
        if self.i_frames > 0:
            self.i_frames -= 1
        if self.knocked_back:
            if self.left:
                self.rect.x += 5
                while vertical_collision(self) or pygame.sprite.spritecollideany(self, next_level_vertical_border_group):
                    self.rect.x -= 1
            else:
                self.rect.x -= 5
                while vertical_collision(self) or pygame.sprite.spritecollideany(self, next_level_vertical_border_group):
                    self.rect.x += 1
        if self.jump_cooldown == 0 and not self.knocked_back:
            self.logic()
            self.jump()
        if not self.standing and not self.knocked_back:
            if self.right:
                self.rect.x += self.vel_x
                while vertical_collision(self):
                    self.rect.x -= 1
                    self.right = False
                    self.left = True
            else:
                self.rect.x -= self.vel_x
                while vertical_collision(self):
                    self.rect.x += 1
                    self.right = True
                    self.left = False
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        if horizontal_down_collision(self):
            while horizontal_down_collision(self):
                self.rect.y += 1
            self.vel_y = -1
            self.rect.y -= self.vel_y
        elif horizontal_up_collision(self) and self.is_jump is True and self.standing is False:
            self.is_jump = False
            self.jump_cooldown = 100
            self.knocked_back = False
            self.vel_y = FALLING_MAX
            while horizontal_up_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        elif not horizontal_down_collision(self) and not horizontal_up_collision(self):
            self.standing = False
            self.is_jump = True
            self.rect.y -= self.vel_y
            if self.vel_y > FALLING_MAX:
                self.vel_y -= FALLING_SPEED

            if horizontal_up_collision(self):
                while horizontal_up_collision(self):
                    self.rect.y -= 1
                self.rect.y += 1
            elif horizontal_down_collision(self):
                while horizontal_down_collision(self):
                    self.rect.y += 1
                self.vel_y = -1
        if platform_collision(
                self.ground_border) and self.is_jump is True and self.standing is False and not self.is_down and self.vel_y < 0:
            self.is_jump = False
            self.knocked_back = False
            self.vel_y = FALLING_MAX
            while platform_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def take_damage(self, direction):
        self.i_frames = 20
        self.hp -= hero.attack_damage
        if hero.attack_type == 1:
            self.knock_back(direction)
        else:
            hero.vel_y = 12
            hero.is_jump = True
            hero.standing = False
            hero.jump_amount -= 1
        if self.hp <= 0:
            self.death()

    def knock_back(self, direction):
        self.vel_y = 8
        self.standing = False
        self.is_jump = True
        if direction == "left":
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        self.rect.y -= 2
        self.knocked_back = True

    def death(self):
        global gold
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)
        self.kill()
        gold += self.gold_reward
        hero.score += self.score_reward


class JumpBot(pygame.sprite.Sprite):
    image_idle = load_image(os.path.join("entity_images\\JumpBot\\idle.png")).convert_alpha()
    image_move = load_image(os.path.join("entity_images\\JumpBot\\move.png")).convert_alpha()

    def __init__(self, x, y, wi, he):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 7
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, wi - 1, he - 1)
        self.image = pygame.Surface([wi - 2, he - 2])
        self.image.blit(JumpBot.image_idle, (0, 1))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False

        self.score_reward = 100
        self.gold_reward = 10

        self.is_jump = False
        self.standing = True
        self.is_down = False
        self.jump_cooldown = 100

        self.attack_type = 0
        self.attack = pygame.sprite.Group()
        self.attack_damage = 10
        self.i_frames = 0
        self.knocked_back = False

        self.hp = 4

    def jump(self):
        if self.standing and not self.is_jump:
            self.jump_cooldown = 100
            self.is_jump = True
            self.vel_y = -((hero.rect.y - self.rect.y) // 4)
            if self.vel_y < 0:
                self.vel_y = 10
            elif self.vel_y > -round(FALLING_MAX * 2.2):
                self.vel_y = -round(FALLING_MAX * 2.2)
            self.rect.y -= 2
            self.standing = False

    def logic(self):
        if hero.rect.x >= self.rect.x:
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        if hero.rect.y >= self.rect.y + self.rect.h:
            self.is_down = True
        else:
            self.is_down = False

    def update(self):
        if self.standing:
            self.image.fill(pygame.SRCALPHA)
            if self.right:
                self.image.blit(pygame.transform.flip(JumpBot.image_idle, 1, 0), (0, 1))
            else:
                self.image.blit(JumpBot.image_idle, (0, 1))
        else:
            self.image.fill(pygame.SRCALPHA)
            if self.right:
                self.image.blit(pygame.transform.flip(JumpBot.image_move, 1, 0), (0, 1))
            else:
                self.image.blit(JumpBot.image_move, (0, 1))
        if self.i_frames > 0:
            self.i_frames -= 1
        if self.knocked_back:
            if self.left:
                self.rect.x += 5
                while vertical_collision(self) or pygame.sprite.spritecollideany(self, next_level_vertical_border_group):
                    self.rect.x -= 1
            else:
                self.rect.x -= 5
                while vertical_collision(self) or pygame.sprite.spritecollideany(self, next_level_vertical_border_group):
                    self.rect.x += 1
        if self.jump_cooldown == 0 and not self.knocked_back:
            self.logic()
            self.jump()
        if not self.standing and not self.knocked_back:
            if self.right:
                self.rect.x += self.vel_x
                while vertical_collision(self):
                    self.rect.x -= 1
                    self.right = False
                    self.left = True
            else:
                self.rect.x -= self.vel_x
                while vertical_collision(self):
                    self.rect.x += 1
                    self.right = True
                    self.left = False
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        if horizontal_down_collision(self):
            while horizontal_down_collision(self):
                self.rect.y += 1
            self.vel_y = -1
            self.rect.y -= self.vel_y
        elif horizontal_up_collision(self) and self.is_jump is True and self.standing is False:
            self.is_jump = False
            self.jump_cooldown = 100
            self.knocked_back = False
            self.vel_y = FALLING_MAX
            while horizontal_up_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        elif not horizontal_down_collision(self) and not horizontal_up_collision(self):
            self.standing = False
            self.is_jump = True
            self.rect.y -= self.vel_y
            if self.vel_y > FALLING_MAX:
                self.vel_y -= FALLING_SPEED

            if horizontal_up_collision(self):
                while horizontal_up_collision(self):
                    self.rect.y -= 1
                self.rect.y += 1
            elif horizontal_down_collision(self):
                while horizontal_down_collision(self):
                    self.rect.y += 1
                self.vel_y = -1
        if platform_collision(
                self.ground_border) and self.is_jump is True and self.standing is False and not self.is_down and self.vel_y < 0:
            self.is_jump = False
            self.knocked_back = False
            self.vel_y = FALLING_MAX
            while platform_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def take_damage(self, direction):
        self.i_frames = 20
        self.hp -= hero.attack_damage
        if hero.attack_type == 1:
            self.knock_back(direction)
        else:
            hero.vel_y = 12
            hero.is_jump = True
            hero.standing = False
            hero.jump_amount -= 1
        if self.hp <= 0:
            self.death()

    def knock_back(self, direction):
        self.vel_y = 8
        self.standing = False
        self.is_jump = True
        if direction == "left":
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        self.rect.y -= 2
        self.knocked_back = True

    def death(self):
        global gold
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)
        self.kill()
        gold += self.gold_reward
        hero.score += self.score_reward


class Player(pygame.sprite.Sprite):
    image_body_idle = load_image(os.path.join("entity_images\\Hero\\body-idle.png")).convert_alpha()
    image_move1 = load_image(os.path.join("entity_images\\Hero\\body-move1.png")).convert_alpha()
    image_move2 = load_image(os.path.join("entity_images\\Hero\\body-move2.png")).convert_alpha()
    image_body_move = [image_move1, image_move2]
    image_body_fall = load_image(os.path.join("entity_images\\Hero\\body-fall.png")).convert_alpha()
    image_body_jump = load_image(os.path.join("entity_images\\Hero\\body-jump.png")).convert_alpha()
    image_body_damage = load_image(os.path.join("entity_images\\Hero\\body-damage.png")).convert_alpha()

    image_shield_active = load_image(os.path.join("entity_images\\Hero\\shield-active.png")).convert_alpha()
    image_shield_idle = load_image(os.path.join("entity_images\\Hero\\shield-idle.png")).convert_alpha()
    image_shield_damage = load_image(os.path.join("entity_images\\Hero\\shield-damage.png")).convert_alpha()

    image_sword_idle = load_image(os.path.join("entity_images\\Hero\\sword-idle.png")).convert_alpha()

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_hero)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 7
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, BLOCK_SIZE - 1, 2 * BLOCK_SIZE - 1)
        self.image = pygame.Surface([BLOCK_SIZE - 2, 2 * BLOCK_SIZE - 2])
        self.image.blit(Player.image_body_idle, (0, 1))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False
        self.moving = False
        self.walk_count = 29
        self.score = 0
        self.gop_stop = 0

        self.is_jump = False
        self.standing = True
        self.is_down = False
        self.jump_max = 1
        self.jump_amount = self.jump_max

        self.attack_type = 0
        self.is_blocking = False
        self.attack = pygame.sprite.Group()
        self.attack_damage = 1
        self.i_frames = 0
        self.knocked_back = False
        self.attack_image = pygame.sprite.Sprite()
        self.attack_image.image = pygame.Surface([1.5 * BLOCK_SIZE - 2, 2.5 * BLOCK_SIZE - 3])
        self.attack_image.rect = pygame.Rect(self.rect.x + 1 + BLOCK_SIZE // 2, self.rect.y - BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE - 2,
                                                 2.5 * BLOCK_SIZE - 3)

        self.max_hp = 100
        self.hp = 100
        self.block_amount = 0.2
        self.damage_resistance = 1
        self.talk = False

    def animate(self):
        self.image.fill(pygame.SRCALPHA)
        if self.standing:
            if self.moving:
                if self.right:
                    self.image.blit(pygame.transform.flip(Player.image_body_move[self.walk_count // 15], 1, 0), (0, 1))
                else:
                    self.image.blit(Player.image_body_move[self.walk_count // 15], (0, 1))
            else:
                if self.right:
                    self.image.blit(pygame.transform.flip(Player.image_body_idle, 1, 0), (0, 1))
                else:
                    self.image.blit(Player.image_body_idle, (0, 1))
        else:
            if self.vel_y >= 0:
                if self.right:
                    self.image.blit(pygame.transform.flip(Player.image_body_jump, 1, 0), (0, 1))
                else:
                    self.image.blit(Player.image_body_jump, (0, 1))
            else:
                if self.right:
                    self.image.blit(pygame.transform.flip(Player.image_body_fall, 1, 0), (0, 1))
                else:
                    self.image.blit(Player.image_body_fall, (0, 1))

        if self.is_blocking:
            if self.right:
                self.image.blit(pygame.transform.flip(Player.image_shield_active, 1, 0), (0, 1))
            else:
                self.image.blit(Player.image_shield_active, (0, 1))
        else:
            if self.right:
                self.image.blit(pygame.transform.flip(Player.image_shield_idle, 1, 0), (0, 1))
            else:
                self.image.blit(Player.image_shield_idle, (0, 1))

        if self.right:
            self.attack_image.image.blit(pygame.transform.flip(Player.image_sword_idle, 1, 0), (-15, 1))
            self.attack_image.rect = pygame.Rect(self.rect.x + 1 + BLOCK_SIZE // 2, self.rect.y - BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE - 2, 2.5 * BLOCK_SIZE - 3)
        else:
            self.attack_image.image.blit(Player.image_sword_idle, (15, 1))
            self.attack_image.rect = pygame.Rect(self.rect.x + 1 + BLOCK_SIZE // 2, self.rect.y - BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE - 2, 2.5 * BLOCK_SIZE - 3)


    def update(self):
        if not self.moving:
            self.walk_count = 29
        else:
            if self.walk_count > 0:
                self.walk_count -= 1
            if self.walk_count == 0:
                self.walk_count = 29

        self.animate()


        global jump_tick
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        if self.knocked_back:
            if self.right:
                self.image.fill(pygame.SRCALPHA)
                self.image.blit(pygame.transform.flip(Player.image_body_damage, 1, 0), (0, 1))
                self.image.blit(pygame.transform.flip(Player.image_shield_damage, 1, 0), (0, 1))
                self.rect.x -= 5
                while vertical_collision(hero):
                    hero.rect.x += 1
            else:
                self.image.fill(pygame.SRCALPHA)
                self.image.blit(Player.image_body_damage, (0, 1))
                self.image.blit(Player.image_shield_damage, (0, 1))
                self.rect.x += 5
                while vertical_collision(hero):
                    hero.rect.x -= 1
        elif self.i_frames > 0 and self.knocked_back is False:
            self.i_frames -= 1

        if horizontal_down_collision(self):
            jump_tick = 0
            while horizontal_down_collision(self):
                self.rect.y += 1
            self.vel_y = -1
            self.rect.y -= self.vel_y
        elif horizontal_up_collision(self) and self.is_jump is True and self.standing is False:
            jump_tick = 0
            self.knocked_back = False
            self.is_jump = False
            self.vel_y = FALLING_MAX
            self.jump_amount = self.jump_max
            while horizontal_up_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
        elif not horizontal_down_collision(self) and not horizontal_up_collision(self):
            if self.standing:
                self.jump_amount -= 1
            self.standing = False
            self.is_jump = True
            self.rect.y -= self.vel_y
            if self.vel_y > FALLING_MAX:
                self.vel_y -= FALLING_SPEED

            if horizontal_up_collision(self):
                while horizontal_up_collision(self):
                    self.rect.y -= 1
                self.rect.y += 1
            elif horizontal_down_collision(self):
                while horizontal_down_collision(self):
                    self.rect.y += 1
                self.vel_y = -1
        """print(platform_collision(self.ground_border), platform_collision(self), self.ground_border.rect, 
        self.rect) """
        if platform_collision(
                self.ground_border) and self.is_jump is True and self.standing is False and not self.is_down and self.vel_y < 0:
            self.is_jump = False
            self.knocked_back = False
            self.jump_amount = self.jump_max
            self.vel_y = FALLING_MAX
            while platform_collision(self):
                self.rect.y -= 1
                self.standing = True
            jump_tick = 0
            self.rect.y += 1
            return

    def def_attack(self):
        global can_attack
        if self.attack_type == 0:
            if self.is_down and self.standing is False:
                self.attack_type = 2
            elif self.is_down is False:
                self.attack_type = 1
        elif self.attack_type == 1:
            attack_sprite = pygame.sprite.Sprite()
            attack_sprite.image = pygame.Surface([1.5 * BLOCK_SIZE - 2, 2.5 * BLOCK_SIZE - 3])
            pygame.draw.rect(attack_sprite.image, (0, 0, 255), (0, 0, 1.5 * BLOCK_SIZE - 2, 2.5 * BLOCK_SIZE - 3))
            if self.right:
                attack_sprite.rect = pygame.Rect(self.rect.x + 1 + BLOCK_SIZE // 2, self.rect.y - BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE - 2,
                                                 2.5 * BLOCK_SIZE - 3)
            else:
                attack_sprite.rect = pygame.Rect(self.rect.x + 1 - BLOCK_SIZE, self.rect.y - BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE - 2,
                                                 2.5 * BLOCK_SIZE - 3)
            self.attack.empty()
            self.attack.add(attack_sprite)

        elif self.attack_type == 2:
            attack_sprite = pygame.sprite.Sprite()
            attack_sprite.image = pygame.Surface([round(BLOCK_SIZE // 2) - 1, BLOCK_SIZE - 2])
            pygame.draw.rect(attack_sprite.image, (0, 0, 255), (0, 0, round(BLOCK_SIZE // 2) - 1, BLOCK_SIZE - 2))
            attack_sprite.rect = pygame.Rect(self.rect.x + self.rect.w // 4 + 1, self.rect.y + self.rect.h - 2,
                                             round(BLOCK_SIZE // 2) - 1, BLOCK_SIZE - 2)
            self.attack.empty()
            self.attack.add(attack_sprite)

    def draw_health(self):
        health_surface = pygame.Surface([round(1.5 * self.max_hp), 32])
        pygame.draw.rect(health_surface, pygame.Color("red"),
                         (0, 0, health_surface.get_width(), health_surface.get_height()))
        if self.hp > 0:
            pygame.draw.rect(health_surface, pygame.Color("green"),
                             (0, 0, round(health_surface.get_width() / self.max_hp * self.hp), health_surface.get_height()))
        hp_text = create_text("{}/{}".format(self.hp, self.max_hp), "data\\CenturyGothic-Bold.ttf", 20,
                              pygame.Color("white"))
        health_surface.blit(hp_text, (6, 2))
        return health_surface

    def take_damage(self, damage, direction):
        global can_attack
        if self.is_blocking:
            self.hp -= round(damage * (self.damage_resistance - self.block_amount))
        else:
            self.hp -= round(damage * self.damage_resistance)
            self.knock_back(direction)
            pygame.event.clear(1)
            self.attack_type = 0
            can_attack = True
        if self.hp <= 0:
            self.hp = 0
            self.death()
        self.i_frames = 20

    def knock_back(self, direction):
        self.vel_y = 6
        self.standing = False
        self.is_jump = True
        if direction == "left":
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        self.rect.y -= 2
        self.knocked_back = True
        self.attack.empty()

    def death(self):
        print("you are DED")


# ---------------------------------------CODE--------------------------------------------------------------------------


running = True

all_hero = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
all_enemies_sprite = pygame.sprite.Group()
all_prujinks = pygame.sprite.Group()
all_ladders = pygame.sprite.Group()
all_enemies = []
all_projectiles = []
all_npcs = pygame.sprite.Group()

block_vertical_borders = pygame.sprite.Group()
block_down_horizontal_borders = pygame.sprite.Group()
block_up_horizontal_borders = pygame.sprite.Group()
platform_horizontal_borders = pygame.sprite.Group()
next_level_horizontal_border_group = pygame.sprite.Group()
next_level_vertical_border_group = pygame.sprite.Group()
enemy_types = [JumpBot, Turret, JumpTurret, QuadraTurret]
all_projectiles_sprite = pygame.sprite.Group()

hero, level_width, level_height, next_levels_pos, true_width, true_height = load_and_generate_map("map.txt")
the_big_screen = pygame.Surface([level_width * BLOCK_SIZE, level_height * BLOCK_SIZE])
can_attack = True
jump_tick = 0

gopnik = Gopnik(36, 11)
trader = Trader(15, 10)

score_text = create_text("Score: " + str(hero.score), os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))

tutorial_board = pygame.Surface([160, 120])
pygame.draw.rect(tutorial_board, pygame.Color("brown"), (0, 0, 160, 120), 10)
tutorial_text = create_text("WASD           move", os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))
tutorial_board.blit(tutorial_text, (10, 10))
tutorial_text = create_text("J            attack", os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))
tutorial_board.blit(tutorial_text, (10, 30))
tutorial_text = create_text("K            shield", os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))
tutorial_board.blit(tutorial_text, (10, 50))
tutorial_text = create_text("L talk(with trader)", os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))
tutorial_board.blit(tutorial_text, (10, 70))
tutorial_text = create_text("gopnik steals gold!", os.path.join("data\\CenturyGothic.ttf"), 16, pygame.Color("white"))
tutorial_board.blit(tutorial_text, (10, 90))


def init_images():
    pause_icon = load_image("pause-icon.png").convert_alpha()  # 64x64
    settings_icon = load_image("settings.png").convert_alpha()
    back_arrow_icon = load_image("back_arrow.png").convert_alpha()
    leader_board_icon = load_image("leader_board_icon.png", (145, 160, 161)).convert_alpha()
    IMAGES["pause-icon"] = pause_icon
    IMAGES["settings"] = settings_icon
    IMAGES["leader_board"] = leader_board_icon
    IMAGES["back_arrow"] = back_arrow_icon


def generate_maps():
    maps = []
    for i in range(1, 22):
        filename = os.path.join("data", "all_maps", f"map_{i}.txt")
        file = open(filename, "r")
        level_map = file.read()
        maps.append(level_map)
    for i in range(1, 4):
        for j in range(1, 4):
            if i == j and j == 3:
                break
            filename = os.path.join("data", "maps", f"map_{i}_{j}.txt")
            file = open(filename, "w")
            random_map = random.choice(maps)
            file.write(random_map)


def generate_map_relation(obj):  # directions relating to next_level
    global CURRENT_MAP
    if CURRENT_MAP == 0:
        return "map_1_1.txt", DIRECTIONS["left"]
    map = CURRENT_MAP.strip("map_").rstrip(".txt")
    map = map.split("_")
    x, y = obj.pos
    if x == 0:
        map[1] = int(map[1])
        map[1] -= 1
        return f"map_{str(map[0])}_{str(map[1])}.txt", DIRECTIONS["right"]
    if y == 0:
        map[0] = int(map[0])
        map[0] += 1
        return f"map_{str(map[0])}_{str(map[1])}.txt", DIRECTIONS["down"]
    if x == true_width - 1:
        map[1] = int(map[1])
        map[1] += 1
        return f"map_{str(map[0])}_{str(map[1])}.txt", DIRECTIONS["left"]
    if y == true_height - 1:
        map[0] = int(map[0])
        map[0] -= 1
        return f"map_{str(map[0])}_{str(map[1])}.txt", DIRECTIONS["up"]


init_images()
start_menu()
generate_maps()

draw_overlapping_screen()


def reset_level():
    global all_hero, all_blocks, all_enemies_sprite, all_prujinks, block_vertical_borders, \
        block_down_horizontal_borders, block_up_horizontal_borders, platform_horizontal_borders, \
        next_level_horizontal_border_group, next_level_vertical_border_group, all_ladders
    all_hero = pygame.sprite.Group()
    all_blocks = pygame.sprite.Group()
    all_enemies_sprite = pygame.sprite.Group()
    all_prujinks = pygame.sprite.Group()
    all_ladders = pygame.sprite.Group()

    block_vertical_borders = pygame.sprite.Group()
    block_down_horizontal_borders = pygame.sprite.Group()
    block_up_horizontal_borders = pygame.sprite.Group()
    platform_horizontal_borders = pygame.sprite.Group()
    next_level_horizontal_border_group = pygame.sprite.Group()
    next_level_vertical_border_group = pygame.sprite.Group()


def check_and_change_level(group):  # (y ↑ x →)
    global hero, next_levels_pos, CURRENT_MAP, the_big_screen, true_width, true_height, level_width, level_height
    collide_obj = pygame.sprite.spritecollide(hero, group, 0, 0)
    if collide_obj:
        hero_x, hero_y = hero.vel_x, hero.vel_y
        collide_obj = collide_obj[0]
        for i in next_levels_pos.keys():
            if next_levels_pos[i] == collide_obj.pos:
                reset_level()
                CURRENT_MAP, new_pos = generate_map_relation(collide_obj)
                hp = hero.hp
                score = hero.score
                hero, level_width, level_height, next_levels_pos, true_width, true_height = load_and_generate_map(
                    CURRENT_MAP, new_pos)
                hero.hp = hp
                hero.score = score
                hero.vel_x, hero.vel_y = hero_x, hero_y
                the_big_screen = pygame.Surface([level_width * BLOCK_SIZE, level_height * BLOCK_SIZE])
                return


while running:
    score_text = create_text("Score: " + str(hero.score), os.path.join("data\\CenturyGothic.ttf"), 16,
                             pygame.Color("white"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == 1:
            if hero.attack_type != 0 and can_attack:
                can_attack = False
                pygame.time.set_timer(1, ATTACK_TIME)
            elif hero.attack_type != 0:
                hero.attack_type = 0
                can_attack = False
                pygame.event.clear(1)
                pygame.time.set_timer(1, ATTACK_COOLDOWN)
                hero.attack.empty()
            else:
                can_attack = True
                pygame.event.clear(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                if dist(x, y, 42, 42) <= 32:
                    pause()
    hero.moving = False
    keys = pygame.key.get_pressed()
    check_and_change_level(next_level_horizontal_border_group)
    check_and_change_level(next_level_vertical_border_group)
    if keys[pygame.K_ESCAPE]:
        pause()
    if keys[pygame.K_w] and hero.jump_amount > 0 and not hero.is_blocking and not hero.knocked_back:
        if jump_tick == 0:
            jump_tick = 30
            hero.is_jump = True
            hero.jump_amount -= 1
            if hero.vel_y < 0:
                hero.vel_y = -(FALLING_MAX * 2)
            else:
                hero.vel_y -= (FALLING_MAX * 2)
                if hero.vel_y > -round(FALLING_MAX * 2.5):
                    hero.vel_y = -round(FALLING_MAX * 2.5)
            hero.rect.y -= 2
            hero.standing = False
    if keys[pygame.K_a] and not hero.is_blocking and not hero.knocked_back:
        hero.left = True
        hero.right = False
        if hero.moving:
            hero.moving = False
        else:
            hero.moving = True
        hero.rect.x -= hero.vel_x
        while vertical_collision(hero):
            hero.rect.x += 1
    if keys[pygame.K_d] and not hero.is_blocking and not hero.knocked_back:
        hero.left = False
        hero.right = True
        if hero.moving:
            hero.moving = False
        else:
            hero.moving = True
        hero.rect.x += hero.vel_x
        while vertical_collision(hero):
            hero.rect.x -= 1
    if keys[pygame.K_s] and not hero.is_blocking and not hero.knocked_back:
        hero.is_down = True
    else:
        hero.is_down = False
    if keys[pygame.K_j] and can_attack and hero.attack_type == 0 and not hero.knocked_back:
        if hero.is_down and hero.standing is False:
            pygame.time.set_timer(1, ATTACK_SWING)
            hero.attack_type = 2
        elif hero.is_down is False:
            pygame.time.set_timer(1, ATTACK_SWING)
            hero.attack_type = 1
    if keys[pygame.K_k] and not hero.knocked_back:
        hero.is_blocking = True
    else:
        hero.is_blocking = False
    if keys[pygame.K_l]:
        hero.talk = True
    else:
        hero.talk = False
    if prujinka_collision(hero):
        jump_tick = 0
        hero.jump_amount = hero.jump_max
        hero.jump_amount -= 1
        hero.rect.y -= 2
        hero.is_jump = True
        hero.standing = False
        hero.vel_y = - int(FALLING_MAX * 2.5)
    damage_check()
    all_hero.update()
    all_projectiles_sprite.update()
    all_npcs.update()
    all_enemies_sprite.update()
    draw_main_screen()
    draw_overlapping_screen()
    if jump_tick > 0:
        jump_tick -= 1
    clock.tick(FPS)
    # pygame.draw.rect(screen, pygame.Color("green"), (hero.rect.x, hero.rect.y, hero.rect.width, hero.rect.height), 1)
    pygame.display.flip()

pygame.quit()
