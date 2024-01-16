import pygame
import os
import sys
import random


        
pygame.init()
pygame.mixer.init()
music_list = ["./data/Summer.mp3", "./data/Autumn.mp3", "./data/Winter.mp3",
              "./data/zemlya-v-illyuminatore.mp3"]
pygame.mixer.music.load("./data/Summer.mp3")
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
grass = pygame.sprite.Group()
trees = pygame.sprite.Group()
stars = pygame.sprite.Group()
Hero = pygame.sprite.Group()
maps_list = []
f = open("./data/maps_list.txt", mode="rt", encoding="utf-8")
for number, line in enumerate(f):
    maps_list.append(line[:-1])
f.close()
location = 0
screen_rect = (0, 0, width, height)




def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    pygame.mixer.init()
    sys.exit()

def start_screen():
    intro_text = ["Проект Pygame", "",
                  "Разработчики:",
                  "Сенченко Иван",
                  "Дудка Игорь",
                  "",
                  "",
                  "",
                  "",
                  "Нажмите любую клавишу для продолжения"]

    fon = pygame.transform.scale(load_image('main_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def win_screen():
    text = ["ВЫ ПОБЕДИЛИ!!!"]

    fon = pygame.transform.scale(load_image('main_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text[0], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = 250
    intro_rect.top = text_coord
    intro_rect.x = 150
    for i in range(3):
        create_particles((intro_rect.x + i * 50, intro_rect.y - 50))
        
    
    while True:
        
        stars.update()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        for line in text:
            screen.blit(string_rendered, intro_rect)
        stars.draw(screen)    
        pygame.display.flip()
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()


def new_location():
    global location
    location += 1
    pygame.mixer.music.load(music_list[location])
    pygame.mixer.music.play(-1)
    if location != len(maps_list):
        for i in grass:
            i.kill()
        for i in trees:
            i.kill()
        board_2 = Board("./data/" + maps_list[location])
        board_2.render(screen)
        hero.renew(board_2)


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
    
        

class Board:
    def __init__(self, file):
        self.cell_size = 100
        self.map = []
        spr_1 = [pygame.transform.scale(load_image("grass_1.png"), (100, 100)),
                      pygame.transform.scale(load_image("tree_1.png"), (50, 80))]
        spr_2 = [pygame.transform.scale(load_image("grass_2.png"), (100, 100)),
                      pygame.transform.scale(load_image("tree_2.png"), (50, 80))]
        spr_3 = [pygame.transform.scale(load_image("grass_3.png"), (100, 100)),
                      pygame.transform.scale(load_image("tree_3.png"), (50, 80))]
        spr_4 = [pygame.transform.scale(load_image("grass_4.png"), (100, 100)),
                      pygame.transform.scale(load_image("tree_4.png"), (50, 80))]
        sprites = [spr_1, spr_2, spr_3, spr_4]
        self.location = 0
        self.f = open(file, mode="rt", encoding="utf-8")
        for number, line in enumerate(self.f):
            if number == 0:
                self.location = int(line)
            else:
                self.map.append(line.split())
        self.f.close()
        self.screen = screen
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                sprite = pygame.sprite.Sprite()
                sprite.image = sprites[self.location - 1][0]
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = 100 * j
                sprite.rect.y = 100 * i
                grass.add(sprite)
                if self.map[i][j] == "t":
                    sprite = pygame.sprite.Sprite()
                    sprite.image = sprites[self.location - 1][1]
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = 25 + 100 * j
                    sprite.rect.y = 10 + 100 * i
                    trees.add(sprite)

    def can_move(self, x, y):
        if self.map[y][x] == "_":
            return True
        elif self.map[y][x] == "t":
            return False
    
    def render(self, screen):
        grass.draw(self.screen)
        trees.draw(self.screen)        


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.pos_1 = [[2, 2], [2, 3], [2, 4],
                 [3, 2], [3, 3], [3, 4],
                 [4, 2], [4, 3], [4, 4]]
        self.pos_2 = [[1, 2], [1, 3], [1, 4],
                 [5, 2], [5, 3], [5, 4],
                 [2, 1], [3, 1], [4, 1],
                 [2, 5], [3, 5], [4, 5]]
        self.pos_3 = [[0, 2], [0, 3], [0, 4],
                 [6, 2], [6, 3], [6, 4],
                 [2, 0], [3, 0], [4, 0],
                 [2, 6], [3, 6], [4, 6]]
        
    def apply(self, obj, dx, dy):
        self.dx = dx
        self.dy = dy
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def need_move(self, pos, n_pos):
        if pos in self.pos_1 and n_pos in self.pos_1:
            return True
        elif pos in self.pos_2 and n_pos in self.pos_2:
            return True
        elif pos in self.pos_3 and n_pos in self.pos_3:
            return True
        else:
            return False

        

class M_Hero(pygame.sprite.Sprite):
    def __init__(self, b):
        super().__init__(Hero)
        self.r_anim = [pygame.transform.scale(load_image("Hero_Idle_0r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_000r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_001r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_002r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_003r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_004r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_005r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_006r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_007r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_008r.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_009r.png"), (100, 100)),]
        self.l_anim = [pygame.transform.scale(load_image("Hero_Idle_0.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_000.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_001.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_002.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_003.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_004.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_005.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_006.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_007.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_008.png"), (100, 100)),
                       pygame.transform.scale(load_image("Hero_Run_009.png"), (100, 100)),]
        self.anim = self.r_anim
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.coords = [0, 0]
        self.rect.x, self.rect.y = self.coords[0] * 100 - 20, self.coords[1] * 100
        self.cam_x = 0
        self.cam_y = 0
        self.b = b
        self.loc = 1

    def up(self):
        self.n_coords = [self.coords[0], self.coords[1] - 1]
        if self.n_coords[1] >= 0:
            if self.b.can_move(self.n_coords[0], self.n_coords[1]):
                if camera.need_move(self.coords, self.n_coords):
                    for i in range(20):
                        clock.tick(20)
                        for j in grass:
                            camera.apply(j, 0, 5)
                        for j in trees:
                            camera.apply(j, 0, 5)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                    self.cam_y -= 100
                else:
                    for i in range(20):
                        clock.tick(20)
                        self.rect = self.rect.move(0, -5)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                if self.coords == [6, 6]:
                    if location != len(maps_list) - 1:
                        self.loc += 1
                        new_location()
                    else:
                        win_screen()
                                   

    def down(self):
        self.n_coords = [self.coords[0], self.coords[1] + 1]
        if self.n_coords[1] <= 6:
            if self.b.can_move(self.n_coords[0], self.n_coords[1]):
                if camera.need_move(self.coords, self.n_coords):
                    for i in range(20):
                        clock.tick(20)
                        for j in grass:
                            camera.apply(j, 0, -5)
                        for j in trees:
                            camera.apply(j, 0, -5)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                    self.cam_y += 100
                else:
                    for i in range(20):
                        clock.tick(20)
                        self.rect = self.rect.move(0, 5)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                if self.coords == [6, 6]:
                    if location != len(maps_list) - 1:
                        self.loc += 1
                        new_location()
                    else:
                        win_screen()

    def left(self):
        self.anim = self.l_anim
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords[0] * 100 + 20 - self.cam_x, self.coords[1] * 100 - self.cam_y
        self.n_coords = [self.coords[0] - 1, self.coords[1]]
        if self.n_coords[0] >= 0:
            if self.b.can_move(self.n_coords[0], self.n_coords[1]):
                if camera.need_move(self.coords, self.n_coords):
                    for i in range(20):
                        clock.tick(20)
                        for j in grass:
                            camera.apply(j, 5, 0)
                        for j in trees:
                            camera.apply(j, 5, 0)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                    self.cam_x -= 100
                else:
                    for i in range(20):
                        clock.tick(20)
                        self.rect = self.rect.move(-5, 0)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                if self.coords == [6, 6]:
                    if location != len(maps_list) - 1:
                        self.loc += 1
                        new_location()
                    else:
                        win_screen()

    def right(self):
        self.anim = self.r_anim
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords[0] * 100 - 20 - self.cam_x, self.coords[1] * 100 - self.cam_y
        self.n_coords = [self.coords[0] + 1, self.coords[1]]
        if self.n_coords[0] <= 6:
            if self.b.can_move(self.n_coords[0], self.n_coords[1]):
                if camera.need_move(self.coords, self.n_coords):
                    for i in range(20):
                        clock.tick(20)
                        for j in grass:
                            camera.apply(j, -5, 0)
                        for j in trees:
                            camera.apply(j, -5, 0)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                    self.cam_x += 100
                else:
                    for i in range(20):
                        clock.tick(20)
                        self.rect = self.rect.move(5, 0)
                        self.image = self.anim[(i + 1) % len(self.anim)]
                        self.b.render(screen)
                        Hero.draw(screen)
                        pygame.display.flip()
                    self.image = self.anim[0]
                    self.coords = self.n_coords
                if self.coords == [6, 6]:
                    if location != len(maps_list) - 1:
                        self.loc += 1
                        new_location()
                    else:
                        win_screen()

    def renew(self, b_new):
        self.rect.x, self.rect.y = -20, 0
        self.cam_x, self.cam_y = 0, 0
        self.coords = [0, 0]
        self.b = b_new
        Hero.draw(screen)
        
    
                        


if __name__ == '__main__':
    board = Board("./data/" + maps_list[location])
    running = True
    hero = M_Hero(board)
    camera = Camera()
    clock = pygame.time.Clock()
    start_screen()
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.left()
                elif event.key == pygame.K_RIGHT:
                    hero.right()
                elif event.key == pygame.K_UP:
                    hero.up()
                elif event.key == pygame.K_DOWN:
                    hero.down()
        board.render(screen)
        Hero.draw(screen)
        pygame.display.flip()

