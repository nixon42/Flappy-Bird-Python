#   import all module we need
import pygame
import os
import random

#   Pygame font initialization
pygame.font.init()

#   The variable for the game
WIDTH = 500  # Width of the Window
HEIGT = 700  # Height of the Window
JUMP_HEIGHT = 50  # How Height the bird will jump
JUMP_INTERVAL = 200  # Interval between jump
PIPE_GAP = 150  # Distance Between Top pipe and Bottom pipe
PIPE_INTERVAL = 10000  # Interval between pipe to spawn
HARD_OVER_TIME = True  # If you want the game more hard (this will change the speed and pipe interval over time)

#   Font that will be use
FONT = pygame.font.SysFont("comicsans", 200)
END = pygame.font.SysFont("comicsans", 50)
SCORE = pygame.font.SysFont("comicsans", 80)

#   Set and Draw the Window
WINDOW = pygame.display.set_mode((WIDTH, HEIGT))

#   Load all the image
IMG_BG = pygame.image.load(os.path.join("img", "bg.png"))  # load baground image
IMG_BG_TRANSFORM = pygame.transform.scale(IMG_BG, (
int(IMG_BG.get_width() * 1.8), int(IMG_BG.get_height() * 1.5)))  # transform the baground image (make more bigger)
IMG_GROUND = pygame.image.load(os.path.join("img", "base.png"))  # load the ground image
IMG_GROUND_TRANSFORM = pygame.transform.scale2x(IMG_GROUND)  # transform the ground image (make little bigger)
IMG_PIPE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("img", "pipe.png")))  # load pipe image & transform it to 2x scale
IMG_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))
            ]  # load all the bird image and transform to 2x scale


class bird:
    """
    Bird class for the bird
    """
    #   Global variabel for bird
    IMG = IMG_BIRD  # the image of the bird
    ROTATE = 20  # How much the bird will rotared if jump
    ANIM = 100  # How long The bird fly Animation each image
    JUMP = JUMP_HEIGHT  # The Height of bird will jump
    INTERVAL = JUMP_INTERVAL  # The interval between jump

    def __init__(self, x, y):
        """
        Initialization all the instance variable
        :param x: The starting  position of X in the window
        :param y: The starting  position of Y in the window
        """
        self.x = x  # Submit x
        self.y = y  # Submit y
        self.img = self.IMG[0]  # submit image
        self.rot = 0  # Instace Variable for rotation
        self.last_jump = 0  # The intance variable to record the last jump
        self.heigt = self.y  # The height of the bird
        self.last_heigt = self.heigt  # The instance variable to record the height
        self.count = 0  # counting for the fall speed
        self.last_thick = 0  # The Intance variable to record the last image change
        self.img_count = 0  # The instance varible to change the image (animation)
        self.last_img = 1  # The instance variable to record last image

    def draw(self, win):
        """
        Draw The Bird in the window
        :param win: The window
        :return: none
        """
        #   get how long program run
        thick = pygame.time.get_ticks()

        #   Non Bloking Delay ( This not very efficient ) I just want to sharp my logic :p
        if thick - self.last_thick >= self.ANIM:
            self.last_thick = thick  # Record the last thick

            #   Increase the image count if it increase
            if self.last_img == self.img_count + 1:
                self.last_img += 1
                self.img = self.IMG[self.img_count]
                self.img_count += 1
                # If image count equal 3 the decreasing it
                if self.img_count == 3:
                    self.img_count -= 1
                    self.last_img -= 3

            #   Decreasing the image count if it decrease
            elif self.last_img == self.img_count - 1:
                self.last_img -= 1
                self.img = self.IMG[self.img_count]
                self.img_count -= 1
                #  If image count equql -1 Increasing it
                if self.img_count == -1:
                    self.img_count += 1
                    self.last_img += 3

        #   If bird rotated lower than -80 change the image to 1 (so if the bird move down, bird will not flap his wing)
        if self.rot < -80:
            self.img = self.IMG[1]

        #   Rotate the image
        rotate_img = pygame.transform.rotate(self.img, self.rot)
        rect = rotate_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.heigt)).center)

        #   Draw the image in window
        win.blit(rotate_img, rect.topleft)

    def jump(self):
        """
        Jump method for bird
        :return: none
        """
        #   Get how long program has run
        thick = pygame.time.get_ticks()

        #   Non Bloking delay to check if over or equal the jump interval
        if thick - self.last_jump >= self.INTERVAL:
            self.last_jump = thick  # Record the last thick
            self.heigt -= self.JUMP / 2  # Increase the height of bird

    def move(self):
        """
        Make bird move or has some physics
        :return: none
        """
        #   Count for the fall speed
        self.count += 1

        #   Check if the last Height is equal or lower from current heght
        if self.last_heigt <= self.heigt:
            self.heigt += self.count / 3  # Make bird move down
            self.rot -= self.count / 4  # Make bird rotare to bottom
            # And if rotation is over -90 make it -90 ( so the bird did not do backflip dan spinning )
            if self.rot < -90:
                self.rot = -90

        #   Check if the current height if hinger from last ( this mean the bird has jump)
        elif self.last_heigt >= self.heigt:
            self.count = 0  # Reset the counter so the bird didn't fall so fast
            self.heigt -= self.JUMP / 2  # Increase the bird Height
            self.rot = self.ROTATE  # Make the bird rotare

        #   Check if the height is lower than 5 make it 3 ( so the bird didn't fly trought window)
        if self.heigt <= 5:
            self.heigt = 5
            self.rot = self.ROTATE  # and make it rotare

        #   Record height
        self.last_heigt = self.heigt

    def get_mask(self):
        """
        Get the mask of bird for perfect pixel collision
        :return: Mask of Bird
        """
        return pygame.mask.from_surface(self.img)  # Give the bird mask as return


class backgroud:
    """
    Class for the baground image
    """
    #   The variabel we need
    IMG = IMG_BG_TRANSFORM  # Submit Transfromed baground image as Image

    def __init__(self, win):
        """
        The class instance inisialization
        :param win: The window for draw the image
        """
        self.img = self.IMG  # Submit the firs image
        self.x = 0  # The x of image 1 in the screen
        self.y = -100  # The y of image 1 in the screen
        self.imgx = self.IMG  # submit the second image
        self.xx = self.img.get_width() - 10  # make the x positioan of image 2 equal of the widht of image 1
        self.yx = self.y  # make the y position of image 2 is same as image 1
        self.window = win  # Create instance of window

    def move(self):
        """
        Move the baground
        :return: none
        """

        #   Increase the x of image 1 and 2 little bit so they move slower from the other
        self.xx -= 0.5
        self.x -= 0.5

        #   move the image to backward if they move over the window
        #   ( idk why this work, because i think the logic is wrong. or just i )
        if self.xx == -1:
            self.x = self.img.get_width() - 10
        elif self.x == -1:
            self.xx = self.imgx.get_width() - 10

    def draw(self):
        """
        Draw the baground image in the window
        :return: none
        """
        #   Draw the baground image in the windows
        self.window.blit(self.img, (self.x, self.y))
        self.window.blit(self.imgx, (self.xx, self.yx))


class obstacle:
    """
    Class for the pipe or obstacle
    """
    def __init__(self, x, win):
        """
        Instance inisialization
        :param x: The x possition of the pipe
        :param win: The window for draw the pipe
        """
        self.img_top = pygame.transform.flip(IMG_PIPE, False, True)  # Flip the pipe image for top pipe
        self.img_bot = IMG_PIPE  # Submit the bottom pipe
        self.gap = PIPE_GAP  # Submit the pipe gap
        self.x = x  # Submit the x position of pipe
        self.y_top = 0  # The y position of top pipe
        self.y_bot = 0  # The y position of bottom pipe
        self.win = win  # The working window
        self.interval = PIPE_INTERVAL  # Submit the interval of pipe
        self.generate()  # make the program execute generate method if is init

    def generate(self):
        """
        Generate random number for the Y of pipe
        :return: none
        """
        #   Generate the heigt of pipe
        self.y_bot = random.randrange(PIPE_GAP, 550)  # Generate random number for bottom pipe
        self.y_top = self.y_bot - self.img_top.get_height() - self.gap  # Search for the Y position of top pipe from the Y of bottom pipe

    def move(self):
        """
        Move the pipe along the window
        :return: none
        """
        self.x -= 1  # Move the pipe

    def draw(self):
        """
        Draw the pipe in the window
        :return: none
        """
        #   Create the position of top pipe and bottom pipe
        top = (self.x, self.y_top)
        bot = (self.x, self.y_bot)

        #   Draw the image
        self.win.blit(self.img_top, top)
        self.win.blit(self.img_bot, bot)

    def collide(self, player, gnd):
        """
        Perfect pixel collision method
        :param player: The player
        :param gnd: The Ground
        :return: Boolean
        """
        #   Get the mask
        player_mask = player.get_mask()  # get the bird mask from bird call
        top_mask = pygame.mask.from_surface(self.img_top)  # get the mask from top pipe
        bot_mask = pygame.mask.from_surface(self.img_bot)  # get the image from bootom pipe
        gnd1_mask = pygame.mask.from_surface(gnd.img)  # get the mask from ground image 1 (this is not efficient, but why not)
        gnd2_mask = pygame.mask.from_surface(gnd.imgx)  # get the mask from ground image 2 (this is not efficient, but why not)

        #   Create the offset of collision
        top_offset = (self.x - player.x, self.y_top - round(player.heigt))  # Top pipe offset
        bot_offset = (self.x - player.x, self.y_bot - round(player.heigt))  # Bottom pipe offset
        gnd1_offset = (gnd.x - player.x, gnd.y - round(player.heigt))  # Gnd 1 offset
        gnd2_offset = (gnd.xx - player.x, gnd.yx - round(player.heigt))  # Gnd 2 offset

        #   Check if the object collide with bird
        top = player_mask.overlap(top_mask, top_offset)  # Top pipe
        bot = player_mask.overlap(bot_mask, bot_offset)  # Bottom pipe
        gnd1_point = player_mask.overlap(gnd1_mask, gnd1_offset)  # Ground 1
        gnd2_point = player_mask.overlap(gnd2_mask, gnd2_offset)  # Ground 2

        #   Return True if any object colide
        if top or bot or gnd1_point or gnd2_point:
            return True

        #   Return False if not
        return False


class ground:
    """
    Class for the Ground
    """
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


def draw_window(win, player, bg, obs, gnd, score):
    bg.draw()
    for pipe in obs:
        pipe.draw()

    gnd.draw()

    sc = SCORE.render(str(score), 4, (255, 255, 255))
    win.blit(sc, (int(WIDTH / 2 - sc.get_width() / 2), 20))

    player.draw(win)
    pygame.display.update()


def lose(win):
    game = FONT.render("GAME", 1, (255, 255, 255))
    over = FONT.render("OVER", 1, (255, 0, 0))
    des = END.render("Press Space To Play Again", 1, (255, 255, 255))

    center = WIDTH / 2

    win.blit(game, (int(center - game.get_width() / 2), 200))
    win.blit(over, (int(center - over.get_width() / 2), 330))
    win.blit(des, (int(center - des.get_width() / 2), 500))

    pygame.display.update()


def main():
    pygame.init()
    timer = pygame.time.Clock()
    win = WINDOW

    last_thick = PIPE_INTERVAL * -1

    pipes = []
    pipe_inter = PIPE_INTERVAL

    fps = 40
    score = 0

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not live:
                for pipe in pipes:
                    pipes.remove(pipe)

                fps = 40
                pipe_inter = PIPE_INTERVAL
                main()

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

            if pipe.x == mybird.x:
                score += 1

            if pipe.x <= -100:
                pipes.remove(pipe)

        if live:
            bg.move()
            gnd.move()
            mybird.move()
            draw_window(win, mybird, bg, pipes, gnd, score)
        else:
            lose(win)

        for pipe in pipes:
            if pipe.collide(mybird, gnd):
                live = False


main()
