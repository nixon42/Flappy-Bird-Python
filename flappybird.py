import pygame
import os
import random
import time

pygame.font.init()

WIDTH = 500
HEIGT = 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGT))
JUMP_HEIGHT = 50
PIPE_GAP = 150
PIPE_INTERVAL = 10000
HARD_OVER_TIME = True
FONT = pygame.font.SysFont("comicsans", 200)
END = pygame.font.SysFont("comicsans",  50)

IMG_BG = pygame.image.load(os.path.join("img", "bg.png"))
IMG_BG_TRANSFORM = pygame.transform.scale(IMG_BG, (int(IMG_BG.get_width()*1.8), int(IMG_BG.get_height()*1.5)))
IMG_GROUND = pygame.image.load(os.path.join("img", "base.png"))
IMG_GROUND_TRANSFORM = pygame.transform.scale2x(IMG_GROUND)
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))
IMG_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))
            ]


class bird:
    IMG = IMG_BIRD
    ROTATE = 20
    VEL = 30
    ANIM = 100
    INTERVAL = 10
    JUMP = JUMP_HEIGHT

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMG[0]
        self.rot = 0
        self.jump_time = False
        self.last_jump = 0
        self.heigt = self.y
        self.last_heigt = self.heigt
        self.count = 0
        self.last_thick = 0
        self.img_count = 0
        self.last_img = 1

    def draw(self, win):
        thick = pygame.time.get_ticks()

        if thick - self.last_thick >= self.ANIM:
            self.last_thick = thick

            if self.last_img == self.img_count + 1:
                self.last_img += 1
                self.img = self.IMG[self.img_count]
                self.img_count += 1
                if self.img_count == 3:
                    self.img_count -= 1
                    self.last_img -= 3

            elif self.last_img == self.img_count - 1:
                self.last_img -= 1
                self.img = self.IMG[self.img_count]
                self.img_count -= 1
                if self.img_count == -1:
                    self.img_count += 1
                    self.last_img += 3

        if self.rot < -80:
            self.img = self.IMG[1]

        rotate_img = pygame.transform.rotate(self.img, self.rot)
        rect = rotate_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.heigt)).center)
        win.blit(rotate_img, rect.topleft)

    def jump(self):
        thick = pygame.time.get_ticks()
        if thick - self.last_jump >= self.INTERVAL:
            self.last_jump = thick
            self.heigt -= self.JUMP/2

    def move(self):
        self.count += 1
        if self.last_heigt <= self.heigt:
            if self.heigt <= 0:
                self.heigt += self.count
            self.heigt += self.count/3
            self.jump_time = True
            self.rot -= self.count/4
            if self.rot < -90:
                self.rot = -90
        elif self.last_heigt >= self.heigt and self.jump_time:
            self.count = 0
            self.jump_time = False
            self.heigt -= self.JUMP/2
            self.rot = self.ROTATE

        if self.heigt <= 10:
            self.heigt = 0
            self.rot = self.ROTATE
        self.last_heigt = self.heigt

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class backgroud:
    IMG = IMG_BG_TRANSFORM

    def __init__(self, win):
        self.img = self.IMG
        self.x = 0
        self.y = -100
        self.imgx = self.IMG
        self.xx = self.img.get_width() - 10
        self.yx = self.y
        # self.speed = SPEED
        self.window = win
        self.last_thick = 0

    def move(self):
        # thick = pygame.time.get_ticks()
        # if thick - self.last_thick >= self.speed:
        #     self.last_thick = thick
        self.xx -= 1
        self.x -= 1
        if self.xx == -1:
            self.x = self.img.get_width() -10
        elif self.x == -1:
            self.xx = self.imgx.get_width() -10

    def draw(self):
        self.window.blit(self.img, (self.x, self.y))
        self.window.blit(self.imgx, (self.xx, self.yx))


class obstacle:
    def __init__(self, x, win):
        self.img_top = pygame.transform.flip(IMG_PIPE, False, True)
        self.img_bot = IMG_PIPE
        self.gap = PIPE_GAP
        self.x = x
        self.last_thick = 0
        self.y_top = 0
        self.y_bot = 0
        self.win = win
        self.interval = PIPE_INTERVAL
        self.top = False
        self.bot = False
        self.generate()

    def generate(self):
        self.y_bot = random.randrange(PIPE_GAP, 680)
        self.y_top = self.y_bot - self.img_top.get_height() - self.gap

    def move(self):
        # thick = pygame.time.get_ticks()
        # if thick - self.last_thick >= self.speed:
        #     self.last_thick = thick
        self.x -= 1

    def draw(self):
        top = (self.x, self.y_top)
        bot = (self.x, self.y_bot)

        self.win.blit(self.img_top, top)
        self.win.blit(self.img_bot, bot)

    def collide(self, player, gnd):
        player_mask = player.get_mask()
        top_mask = pygame.mask.from_surface(self.img_top)
        bot_mask = pygame.mask.from_surface(self.img_bot)
        gnd1_mask = pygame.mask.from_surface(gnd.img)
        gnd2_mask = pygame.mask.from_surface(gnd.imgx)

        top_offset = (self.x - player.x, self.y_top - round(player.heigt))
        bot_offset = (self.x - player.x, self.y_bot - round(player.heigt))

        gnd1_offset = (gnd.x - player.x, gnd.y - round(player.heigt))
        gnd2_offset = (gnd.xx - player.x, gnd.yx - round(player.heigt))

        self.top = player_mask.overlap(top_mask, top_offset)
        self.bot = player_mask.overlap(bot_mask, bot_offset)

        gnd1_point = player_mask.overlap(gnd1_mask, gnd1_offset)
        gnd2_point = player_mask.overlap(gnd2_mask, gnd2_offset)

        if self.top or self.bot or gnd1_point or gnd2_point:
            return True

        return False


class ground:
    def __init__(self, win):
        self.img = IMG_GROUND_TRANSFORM
        self.x = 0
        self.y = 580
        self.imgx = self.img
        self.xx = self.img.get_width() - 3
        self.yx = self.y
        self.win = win

    def move(self):
        self.x -= 1
        self.xx -= 1

        if self.xx == -1:
            self.x = self.img.get_width() - 3
        elif self.x == -1:
            self.xx = self.img.get_width() - 3

    def draw(self):
        self.win.blit(self.img, (self.x, self.y))
        self.win.blit(self.imgx, (self.xx, self.yx))


def draw_window(win, player, bg, obs, gnd):
    bg.draw()
    for pipe in obs:
        pipe.draw()

    gnd.draw()
    player.draw(win)
    pygame.display.update()


def lose(win):
    gameover = FONT.render("GAME", 1, (255, 255, 255))
    win.blit(gameover, (40, 200))

    gameover = FONT.render("OVER", 1, (255, 0, 0))
    win.blit(gameover, (50, 330))

    gameover = END.render("Press Space To Continue", 1, (255, 255, 255))
    win.blit(gameover, (37, 500))
    pygame.display.update()


def main():
    pygame.init()
    timer = pygame.time.Clock()
    win = WINDOW

    last_thick = PIPE_INTERVAL * -1

    pipes = []
    pipe_inter = PIPE_INTERVAL

    fps = 40

    hard = HARD_OVER_TIME

    bg = backgroud(win)
    mybird = bird(100, 200)
    gnd = ground(win)

    run = True
    live = True
    while run:
        if hard:
            fps += 0.01
            timer.tick(int(fps))
            if fps >= 120:
                fps = 120
        else:
            timer.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                mybird.jump()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                live = True

        thick = pygame.time.get_ticks()
        if thick - last_thick >= pipe_inter:
            last_thick = thick
            pipes.append(obstacle(WIDTH, win))
            if hard:
                pipe_inter -= 500
                if pipe_inter <= 5000:
                    pipe_inter = 5000

        for pipe in pipes:
            pipe.move()
            if pipe.x <= -100:
                pipes.remove(pipe)

        if live:
            bg.move()
            gnd.move()
            mybird.move()
            draw_window(win, mybird, bg, pipes, gnd)
        else:
            lose(win)

        for pipe in pipes:
            if pipe.collide(mybird, gnd):
                live = False


main()
