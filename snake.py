import pygame
import random

# -*- coding: utf-8 -*-

pygame.init()
WIDTH = 500
HEIGHT = 500

COLS = 25
ROWS = 20

FRUIT = 0
PAUSE = False

HEAD = pygame.image.load("image/head.png")
TAIL = pygame.image.load("image/tail.png")
BODY = pygame.image.load("image/body.png")
CLOUD = pygame.image.load("image/cloud.jpg")
RET = pygame.image.load("image/cloud.png")
SKY = pygame.image.load("image/sky.jpg")
BUTTONS = pygame.image.load("image/buttons.png")

FRUITS = [pygame.image.load("image/apple.png"),
          pygame.image.load("image/banana.png"),
          pygame.image.load("image/berry.png"),
          pygame.image.load("image/orange.png"),
          pygame.image.load("image/watermelon.png")]

pygame.display.set_caption('ЗМЕЙКА')
programIcon = pygame.image.load('image/head.png')

pygame.display.set_icon(programIcon)


class GameElement:

    def __init__(self, sr, fruit=0, dirnx=1, dirny=0):
        global FRUIT
        self.pos = sr
        self.x = dirnx
        self.y = dirny
        self.fruit = fruit
        FRUIT = self.fruit

    def move(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)

    def draw(self, screen, obj):
        dis = 500 // 20
        i = self.pos[0]
        j = self.pos[1]
        if obj == "h":
            screen.blit(HEAD, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        elif obj == "t":
            screen.blit(TAIL, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        elif obj == "f":
            screen.blit(self.fruit, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        else:
            screen.blit(BODY, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class Snake:
    body = []
    turns = {}

    def __init__(self, pos):
        self.head = GameElement(pos)
        self.body.append(self.head)
        self.x, self.y = 0, 1

    def move(self):
        global PAUSE
        heh = pygame.font.SysFont('Comic Sans MS', 30)
        one = heh.render('Приготовьтесь..', False, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.x, self.y = -1, 0
                    self.turns[self.head.pos] = [self.x, self.y]
                elif keys[pygame.K_RIGHT]:
                    self.x, self.y = 1, 0
                    self.turns[self.head.pos] = [self.x, self.y]
                elif keys[pygame.K_UP]:
                    self.y, self.x = -1, 0
                    self.turns[self.head.pos] = [self.x, self.y]
                elif keys[pygame.K_DOWN]:
                    self.y, self.x = 1, 0
                    self.turns[self.head.pos] = [self.x, self.y]
                elif keys[pygame.K_o]:
                    PAUSE = True
                elif keys[pygame.K_p]:
                    win.blit(one, (100, 150))
                    pygame.display.update()
                    pygame.time.delay(2)
                    PAUSE = False

        for i, c in enumerate(self.body):
            p = c.pos
            if PAUSE:
                break
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.x, c.y)

    def reset(self):
        global snack, straw
        snack = GameElement(random_snack(ROWS, s), fruit=random.choice(FRUITS))
        self.head = GameElement((6, 8))
        self.body.clear()
        self.body.append(self.head)
        self.turns.clear()
        self.x, self.y = 0, 1
        straw = False
        start(False)

    def add_body(self):
        tail = self.body[-1]
        dx, dy = tail.x, tail.y

        if dx == 1 and dy == 0:
            self.body.append(GameElement((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(GameElement((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(GameElement((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(GameElement((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].x = dx
        self.body[-1].y = dy

    def draw(self, screen):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(screen, "h")
            elif i == len(self.body) - 1 and len(self.body) > 1:
                c.draw(screen, "t")
            else:
                c.draw(screen, "b")


def start(s):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    my = pygame.font.SysFont('Comic Sans MS', 17)
    text = font.render('Приветсвую в сей', False, (0, 0, 0))
    text1 = font.render(' прекрасной игре!', False, (0, 0, 0))
    help1 = my.render("Управление осуществляется", False, (0, 0, 0))
    help2 = my.render("при помощи стрелочек ->", False, (0, 0, 0))
    text_surface1 = font.render('Ещё раз?', False, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return game()

        if s:
            win.blit(SKY, (0, 0))
            win.blit(text, (20, 40))
            win.blit(text1, (120, 75))
            win.blit(help1, (15, 250))
            win.blit(help2, (15, 265))
            win.blit(BUTTONS, (260, 255))
        else:
            win.blit(CLOUD, (0, 0))
            pygame.draw.rect(win, "white", (25, 25, WIDTH - 49, HEIGHT - 49))
            win.blit(RET, (150, 200))
            win.blit(text_surface1, (110, 120))
        pygame.display.flip()


def redraw_window():
    global win
    win.fill((0, 0, 0))
    win.blit(CLOUD, (0, 0))
    pygame.draw.rect(win, "white", (25, 25, WIDTH - 49, HEIGHT - 49))
    s.draw(win)
    snack.draw(win, "f")
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


def main():
    global s, snack, win, straw
    straw = False
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    s = Snake((10, 10))
    snack = GameElement(random_snack(ROWS, s), fruit=random.choice(FRUITS))
    start(True)


def game():
    global s, snack, win, straw
    while True:
        pygame.time.Clock().tick(10)
        s.move()
        head_pos = s.head.pos
        if head_pos[0] >= 19 or head_pos[0] < 1 or head_pos[1] >= 19 or head_pos[1] < 1:
            if len(s.body) != 1:
                print("Стена - главный враг", file=log)
                print(f"Счет: {len(s.body)}", file=log)
                print("- - - - - - - - - -\n", file=log)
            s.reset()

        if s.body[0].pos == snack.pos:
            if FRUIT == FRUITS[2]:
                if not straw:
                    straw = True
                else:
                    straw = False
                    s.add_body()
            elif FRUIT == FRUITS[4]:
                s.add_body()
                s.add_body()
            else:
                s.add_body()
            snack = GameElement(random_snack(ROWS, s), fruit=random.choice(FRUITS))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print("Съесть самого себя - идея не лучшая", file=log)
                print(f"Счет: {len(s.body)}", file=log)
                print("- - - - - - - - - -\n", file=log)
                s.reset()
                break

        redraw_window()


log = open("logs.txt", 'w')
main()
log.close()
