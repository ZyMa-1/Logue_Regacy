import os
import sys
import pygame

pygame.init()
size = 800, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Logue Regacy")
overlapping_screen = pygame.Surface([size[0], size[1]], pygame.SRCALPHA)
overlapping_screen = overlapping_screen.convert_alpha()
ATTACK_TIME = 100  # in milliseconds
ATTACK_COOLDOWN = 100  # in milliseconds
ATTACK_SWING = 100 # in milliseconds
BLOCK_SIZE = 50  # размер одного блока
FALLING_MAX = -10
FALLING_SPEED = 1
FPS = 60
CURRENT_MAP = 1
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
MAP_RELATIONS = dict()


def draw_main_screen():
    the_big_screen.fill(pygame.Color("black"))
    if hero.attack_type != 0 and not can_attack:
        hero.def_attack()
        hero.attack.draw(the_big_screen)
    all_blocks.draw(the_big_screen)
    all_enemies_sprite.draw(the_big_screen)
    all_hero.draw(the_big_screen)
    cutout_x, cutout_y = camera_adjustment()
    cutout = pygame.Rect(cutout_x, cutout_y, size[0], size[1])
    screen.blit(the_big_screen, (0, 0), cutout)
    screen.blit(overlapping_screen, (0, 0))
    pygame.display.flip()


def draw_overlapping_screen():
    overlapping_screen.blit(IMAGES["pause-icon"], (10, 10))
    overlapping_screen.blit(hero.draw_health(), (80, 26))


def dist(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5


def camera_adjustment():
    x = round(hero.rect.x + 0.5 * hero.rect.w - size[0] * 0.5)
    y = round(hero.rect.y + 0.5 * hero.rect.h - size[1] * 0.5)
    #print(the_big_screen.get_width(), the_big_screen.get_height())
    if x < BLOCK_SIZE:
        x = BLOCK_SIZE
    elif x + size[0] > the_big_screen.get_width():
        x = the_big_screen.get_width() - size[0]
    if y < BLOCK_SIZE:
        y = BLOCK_SIZE
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
    main_surface = pygame.Surface([400, 250])
    main_surface_dx = 200
    main_surface_dy = 125
    main_surface.fill(pygame.Color("blue"))
    for x in range(size[0]):
        for y in range(size[1]):
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


def load_and_generate_map(filename, new_pos=None, direction=None):
    filename = os.path.join("data\\maps", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(max(map(len, level_map)), 16)
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    max_height = max(len(level), 17)
    player_flag = 0
    player_x, player_y = 0, 0
    next_levels_pos = []
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
            if level[y][x] == '-':
                if y == 0 or y == len(level) - 1:
                    if x > 0 and level[y][x - 1] != '-':
                        Next_level_horizontal_border(x, y)
                        Platform(x, y)
                        Platform(x + 1, y)
                        next_levels_pos.append((x, y))
                else:
                    if y > 0 and level[y - 1][x] != '-':
                        Next_level_vertical_border(x, y)
                        next_levels_pos.append((x, y))
    if player_x == 0 and player_y == 0:
        player_x, player_y = next_levels_pos[new_pos - 1]
        if direction == DIRECTIONS["left"]:
            player_x -= 1
        if direction == DIRECTIONS["right"]:
            player_x += 1
        if direction == DIRECTIONS["up"]:
            player_y -= 2
        if direction == DIRECTIONS["down"]:
            player_y += 1
    hero = Player(player_x, player_y)
    return hero, max_width, max_height, next_levels_pos


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


class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y, wi, he):  # coordinates not in pixels
        super().__init__(all_enemies_sprite)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 7
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, wi - 1, he - 1)
        self.image = pygame.Surface([wi - 1, he - 2])
        pygame.draw.rect(self.image, (0, 255, 0), (0, 1, wi - 2, he - 3))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False

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
            self.vel_y = -((hero.rect.y - self.rect.y) // 5)
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
        if hero.rect.y >= self.rect.y:
            self.is_down = True
        else:
            self.is_down = False

    def update(self):
        if self.i_frames > 0:
            self.i_frames -= 1
        if self.knocked_back:
            if self.right:
                self.rect.x -= 5
            else:
                self.rect.x += 5
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
            self.jump_cooldown = 100
            self.vel_y = FALLING_MAX
            while platform_collision(self):
                self.rect.y -= 1
                self.standing = True
            self.rect.y += 1
            return
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def take_damage(self, direction):
        self.i_frames = 10
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

    def death(self):
        all_enemies_sprite.remove(self)
        all_enemies.remove(self)


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):  # coordinates not in pixels
        super().__init__(all_hero)
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        self.vel_x = 7
        self.vel_y = FALLING_MAX

        self.rect = pygame.Rect(x, y, BLOCK_SIZE - 1, 2 * BLOCK_SIZE - 1)
        self.image = pygame.Surface([BLOCK_SIZE - 1, 2 * BLOCK_SIZE - 2])
        pygame.draw.rect(self.image, (255, 0, 0), (0, 1, BLOCK_SIZE - 2, BLOCK_SIZE * 2 - 3))
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        self.right = True
        self.left = False

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

        self.max_hp = 100
        self.hp = 100
        self.block_amount = 0.2
        self.damage_resistance = 1

    def update(self):
        global jump_tick
        self.ground_border = Invisible_Rect(self.rect.x, self.rect.y + self.rect.h - 9, self.rect.x + self.rect.w,
                                            self.rect.y + self.rect.h + 1)

        if self.knocked_back:
            if self.right:
                self.rect.x -= 5
            else:
                self.rect.x += 5
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

    def death(self):
        print("you are DED")



# ---------------------------------------CODE--------------------------------------------------------------------------


running = True

all_hero = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
all_enemies_sprite = pygame.sprite.Group()
all_prujinks = pygame.sprite.Group()
all_enemies = []

block_vertical_borders = pygame.sprite.Group()
block_down_horizontal_borders = pygame.sprite.Group()
block_up_horizontal_borders = pygame.sprite.Group()
platform_horizontal_borders = pygame.sprite.Group()
next_level_horizontal_border_group = pygame.sprite.Group()
next_level_vertical_border_group = pygame.sprite.Group()

hero, level_width, level_height, next_levels_pos = load_and_generate_map(f"map_{str(CURRENT_MAP)}.txt")
the_big_screen = pygame.Surface([level_width * BLOCK_SIZE, level_height * BLOCK_SIZE])
can_attack = True
jump_tick = 0
asd = Frog(4, 4, BLOCK_SIZE, BLOCK_SIZE)
all_enemies.append(asd)


def init_images():
    pause_icon = load_image("pause-icon.png").convert_alpha()  # 64x64
    settings_icon = load_image("settings.png").convert_alpha()
    back_arrow_icon = load_image("back_arrow.png").convert_alpha()
    leader_board_icon = load_image("leader_board_icon.png", (145, 160, 161)).convert_alpha()
    IMAGES["pause-icon"] = pause_icon
    IMAGES["settings"] = settings_icon
    IMAGES["leader_board"] = leader_board_icon
    IMAGES["back_arrow"] = back_arrow_icon


def init_map_relations():
    filename = os.path.join("data", "map_relations.txt")
    with open(filename, 'r') as mapFile:
        map_relations = [line.strip() for line in mapFile]
    for line in map_relations:
        line = line.split('-')
        line[0] = line[0].split(',')
        line[1] = line[1].split(',')
        first_tuple = (int(line[0][0]), int(line[0][1]))
        second_tuple = (int(line[1][0]), int(line[1][1]))
        MAP_RELATIONS[first_tuple] = second_tuple
        MAP_RELATIONS[second_tuple] = first_tuple


init_images()
init_map_relations()
start_menu()

draw_overlapping_screen()


def reset_level():
    global all_hero, all_blocks, all_enemies_sprite, all_prujinks, block_vertical_borders, \
        block_down_horizontal_borders, block_up_horizontal_borders, platform_horizontal_borders, \
        next_level_horizontal_border_group, next_level_vertical_border_group
    all_hero = pygame.sprite.Group()
    all_blocks = pygame.sprite.Group()
    all_enemies_sprite = pygame.sprite.Group()
    all_prujinks = pygame.sprite.Group()

    block_vertical_borders = pygame.sprite.Group()
    block_down_horizontal_borders = pygame.sprite.Group()
    block_up_horizontal_borders = pygame.sprite.Group()
    platform_horizontal_borders = pygame.sprite.Group()
    next_level_horizontal_border_group = pygame.sprite.Group()
    next_level_vertical_border_group = pygame.sprite.Group()


def check_and_change_level(group):
    global hero, next_levels_pos, CURRENT_MAP, the_big_screen
    collide_obj = pygame.sprite.spritecollide(hero, group, 0, 0)
    if collide_obj:
        hero_x, hero_y = hero.vel_x, hero.vel_y
        collide_obj = collide_obj[0]
        for i in range(len(next_levels_pos)):
            if next_levels_pos[i] == collide_obj.pos:
                reset_level()
                CURRENT_MAP, new_pos = MAP_RELATIONS[(CURRENT_MAP, i + 1)]
                hero, level_width, level_height, next_levels_pos = load_and_generate_map(f"map_{str(CURRENT_MAP)}.txt",
                                                                                         new_pos, collide_obj.direction)
                hero.vel_x, hero.vel_y = hero_x, hero_y
                the_big_screen = pygame.Surface([level_width * BLOCK_SIZE, level_height * BLOCK_SIZE])
                return


while running:
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
        hero.rect.x -= hero.vel_x
        while vertical_collision(hero):
            hero.rect.x += 1
    if keys[pygame.K_d] and not hero.is_blocking and not hero.knocked_back:
        hero.left = False
        hero.right = True
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
    all_enemies_sprite.update()
    draw_main_screen()
    draw_overlapping_screen()
    if jump_tick > 0:
        jump_tick -= 1
    clock.tick(FPS)
    # pygame.draw.rect(screen, pygame.Color("green"), (hero.rect.x, hero.rect.y, hero.rect.width, hero.rect.height), 1)
    pygame.display.flip()

pygame.quit()