import glob
import json
import re
import sys
from random import *

import pygame
from pygame.locals import *

pygame.init()
pygame.OPENGL

#  NEW GAME ##################################################################

SCREEN_WIDTH = 1122
SCREEN_HEIGHT = 653
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Space Lab 76')
game_icon = pygame.image.load('game_icon.png').convert_alpha()
pygame.display.set_icon(game_icon)

score_digits = pygame.font.Font("fonts/WhiteRabbit-47pD.ttf", 40)
score_title = pygame.font.Font("fonts/WhiteRabbit-47pD.ttf", 15)

game_over_font_shadow = pygame.font.Font("fonts/WhiteRabbit-47pD.ttf", 150)
game_over_font = pygame.font.Font("fonts/WhiteRabbit-47pD.ttf", 150)
game_over_shadow = game_over_font_shadow.render(
    "Game Over", True, (33, 33, 33))
game_over = game_over_font.render("Game Over", True, (225, 78, 69))
score_gui = score_title.render("Disks collected:", True, (204, 197, 87))

UP = 'up'
LEFT = 'left'
RIGHT = 'right'
DOWN = 'down'

FPS_CLOCK = pygame.time.Clock()
FPS = 60
COUNT = 0


bot_padding = 13

up_sprite = 'tl.png'
down_sprite = 'br.png'
right_sprite = 'tr.png'
left_sprite = 'bl.png'

direction = None
score = 0
run_once = False

not_on_wall = True
next_wall_item = 0

top_wall_y_start = 520
right_wall_y_start = -270
bottom_wall_y_start = 660
left_wall_y_start = place_on_top_wall = 355

wall_items = []
extra_wall_details = []
disk_list = []

disks = 22
got_key = unlock = open_door = False

# Sounds
hit_sound = pygame.mixer.Sound("sounds/reverse-bass-blip-2.flac")
pygame.mixer.music.load('music/spaceLab76-intro.mp3')
item_sound = "sounds/square_beep.wav"
open_door_image = pygame.image.load(
    'image_archive/open_door.png').convert_alpha()
play_once = True

speed_timer = USEREVENT + 1

# pygame.mixer.music.play(-1, 0.0)

# pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound\enemy_hit.wav'))


class Enemy():
    def __init__(self, x, y):
        """
        docstring
        """
        self.image = pygame.image.load("enemy/enemy_blue.png").convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.x = x
        self.y = y
        self.vel_x = 20
        self.vel_y = 10

    def update(self):
        if self.y > (top_wall_y_start + 32) - (self.x / 2) and self.y < \
            (bottom_wall_y_start + 43) - (self.x / 2) and self.y < \
            (left_wall_y_start + 5) + (self.x / 2) and self.y > \
                (right_wall_y_start + 35) + (self.x/2):
            pass
        else:
            # print("here")
            self.vel_y *= -1
            self.vel_x *= -1

        self.y += self.vel_y * .2
        self.x += self.vel_x * .2
        # if self.switch > 0:

        #     print("if")
        #     self.y += self.vel_y * .2
        #     self.x += self.vel_x * .2

        # if self.switch < 0:
        #     print("else")
        #     self.y += self.vel_y
        #     self.x += self.vel_x

    def render(self):
        screen.blit(self.image, (self.x, self.y))

        pass


class Bot(pygame.sprite.Sprite):  # represents the bot, not the game
    def __init__(self):
        self.image = pygame.image.load(right_sprite).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        # the bot's position
        x = 227
        y = 457
        self.dist_x = 2  # distance moved right or left
        self.dist_y = 1  # distance moved up or down
        self.x = x
        self.y = y

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_UP]:
            if (self.y + 5) > top_wall_y_start - (self.x / 2):
                self.speedy -= self.dist_y
                self.speedx -= self.dist_x
            self.image = pygame.image.load(up_sprite).convert_alpha()

        elif keystate[pygame.K_DOWN]:
            if self.y < bottom_wall_y_start - (self.x / 2):
                self.speedy += self.dist_y
                self.speedx += self.dist_x
            self.image = pygame.image.load(down_sprite).convert_alpha()

        elif keystate[pygame.K_LEFT]:
            if (self.y + 20) < left_wall_y_start + (self.x/2):
                self.speedy += self.dist_y
                self.speedx -= self.dist_x
            self.image = pygame.image.load(left_sprite).convert_alpha()

        elif keystate[pygame.K_RIGHT]:
            if self.y > right_wall_y_start + (self.x/2):
                self.speedy -= self.dist_y
                self.speedx += self.dist_x
            self.image = pygame.image.load(right_sprite).convert_alpha()

        self.x += self.speedx
        self.y += self.speedy

    def render(self):
        screen.blit(self.image, (self.x, self.y))


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("space-lab76-game-blank.png").convert()
        self.y = 0
        self.x = 0

    def render(self):
        screen.blit(self.image, (self.x, self.y))


class DiskItem:
    def __init__(self, x, y):
        super().__init__()
        # get all images in /images directory
        disks = [f for f in glob.glob("disks/*.png")]
        # get a random image from the list
        image = sample(disks,  1)
        # load one random image
        self.image = pygame.image.load(image[0]).convert_alpha()
        self.x = x
        self.y = y
        self.image_string = image[0]

    def render(self):
        screen.blit(self.image, (self.x, self.y))


class WallObjects:
    def __init__(self, x):
        super().__init__()
        # photoshop all items the same width and height

        # get all images in /images directory
        wall_images = [f for f in glob.glob("wall_l_objects/*.png")]
        # get a random image from the list
        image = sample(wall_images,  1)
        # load one random image
        self.image = pygame.image.load(image[0]).convert_alpha()
        # Start wall items with a 20 pixel buffer so items are not right in the upper rught corner
        self.x = x + ((top_wall_y_start - 20) - self.image.get_width())
        # start the wall objects baesed on info on the line above
        self.y = (-x / 2) + 175
        self.width = self.image.get_width()

    def render(self):
        screen.blit(self.image, (self.x, self.y))


class HealthBar:

    def __init__(self, red, blue, green, left, top, width, height, filled):
        super().__init__()
        self.red = red
        self.blue = blue
        self.green = green
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.filled = filled

    def render(self):
        pygame.draw.rect(screen, [self.red, self.blue, self.green], [
                         self.left, self.top, self.width, self.height], self.filled)


def show_open_door(is_open):
    if is_open:
        screen.blit(open_door_image, (876, 87))


def is_in_bounds(top, botton, left, right):
    # Get a point on the floor
    bounds = True
    while bounds:
        x = randint(0, SCREEN_WIDTH)
        y = randint(0, SCREEN_HEIGHT)

        if y > (top_wall_y_start + top) - (x / 2) and y < (bottom_wall_y_start + botton) - (x / 2) \
            and y < (left_wall_y_start + left) + (x / 2) and y > (right_wall_y_start + right) + (x/2):
            bounds = False
            return x, y
        else:
            bounds = True


def is_on_top_wall(x, y):
    # Add wall items from upper right to  lower left so they over lap
    if y == top_wall_y_start - (x / 2) and x >= 200 and x <= 600:
        global not_on_wall
        not_on_wall = False
        return True


# add wall objects randomly
for i in range(10):
    # Spacing?
    place_on_top_wall -= 65
    wall_object = WallObjects(place_on_top_wall)
    extra_wall_details.append(wall_object)

# add floor items randomly
while len(disk_list) < disks:
    x, y = is_in_bounds(32, 54, 5, 35)

    # make the key the last item so it is on top
    if len(disk_list) == disks - 2:
        new_disk = (DiskItem(x, y))
        # speed bboost
        new_disk.image = pygame.image.load("key/blue-key.png").convert_alpha()
        new_disk.image_string = "key/blue-key.png"
    elif len(disk_list) == disks - 1:
        new_disk = (DiskItem(x, y))
        # unlock door
        new_disk.image = pygame.image.load("key/gold-key.png").convert_alpha()
        new_disk.image_string = "key/gold-key.png"
        # how do i add more - need to regenerate new random numbers

    else:
        new_disk = DiskItem(x, y)

    disk_list.append(new_disk)


def player_hit(disk_list, sprite_x, sprite_y):
    global score, got_key, FPS, run_once

    # Offset the hit box to the bottom of bot
    sprite_x += 8
    sprite_y += (bot.image_height / 2) + 7

    for idx, disk in enumerate(disk_list):
        bot.dist_x, bot.dist_y
        if ((sprite_x > disk.x + (bot_padding * -1) and sprite_x < disk.x + bot_padding)
                and (sprite_y > disk.y + (bot_padding * -1) and sprite_y < disk.y + bot_padding)):
            item_sound = "sounds/jd-hihat.wav"

            # get key first
            if re.search(r"gold", disk.image_string):
                # show info to user
                got_key = True
                item_sound = "sounds/beep.wav"

                # <<<<--------------------------------------
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('sounds/beep.wav'))
                # print("got gold key - now unlock door")

            elif re.search(r"blue", disk.image_string):
                bot.dist_x = 4
                bot.dist_y = 2
                pygame.time.set_timer(speed_timer, 650)
                run_once = True
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('sounds/reverse-bass-blip-2.flac'))

            # Dont touch disks until door unloccked
            # elif got_key and score >= 1 and not unlock or not got_key:
            #     # error nosie?
            #     print("error need to unlock first")

            # got the key and unlocked the door
            elif got_key and score <= 1 and unlock:
                print("score!")
                # make door open sound
                # make door open image

            if re.search(r"red", disk.image_string):
                # print('here')
                health.width += health_bg.width/disks
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(item_sound))


            disk_list.pop(idx)
            score += 1
            # pygame.mixer.Channel(0).play(pygame.mixer.Sound(item_sound))
            # pygame.mixer.Sound.play(hit_sound)


background = Background()
bot = Bot()  # create an instance
enmy_x, enmy_y = is_in_bounds(32, 54, 5, 35)
enemy = Enemy(enmy_x, enmy_y)
health_bg = HealthBar(255, 78, 65, 10, 80, 500, 10, 1)
health = HealthBar(255, 78, 65, 10, 80, 1, 10, 0)

run = True
all_enemies = []
# The game loop
while run:
    background.render()
    show_open_door(open_door)
    health_bg.render()
    health.render()
    for disk in disk_list:
        disk.render()

    for extra_wall_detail in extra_wall_details:
        extra_wall_detail.render()

    # *** SCORE ***
    screen.blit(score_gui, (10, 107))
    score_value = score_digits.render(str(score), True, (255, 255, 255))
    screen.blit(score_value, (160, 100))

   

    for event in pygame.event.get():

        # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print("Clicky")
            pass

        if event.type == pygame.QUIT:
            run = False
            print('exit')
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            direction = event.key
            if event.key == pygame.K_ESCAPE:
                loop = 0
            # if event.key == pygame.K_r:
            #     # main()
            #     print("restart")
            # if event.key == K_SPACE:
            #     print("unlock")

        if event.type == KEYUP:
            if event.key == direction:
                direction = None

        # if event.key == pygame.K_r and not player.alive():
        #         main()

    enemy.update()
    enemy.render()
    bot.update()
    bot.render()
    
     # **** GAME OVER ****
    if len(disk_list) <= 0:

        screen.blit(game_over_shadow, ((SCREEN_WIDTH / 2) -
                                       (game_over.get_rect().width) / 2, 4 + SCREEN_HEIGHT / 2))
        screen.blit(game_over, ((SCREEN_WIDTH / 2) -
                                (game_over.get_rect().width) / 2, SCREEN_HEIGHT / 2))

    player_hit(disk_list, bot.x, bot.y)

    # for some reason the timeing is random
    # check event queue contains speed_timer
    if pygame.event.get(speed_timer) and run_once:
        run_once = False
        bot.dist_x = 2
        bot.dist_y = 1

    # detect door open
    if bot.x >= 860 and bot.y <= 180:
        unlock = True
        if play_once and got_key:
            # print("door unlocked get rest of disks")
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound("sounds/bass_drum.wav"))
            pygame.mixer.Sound("sounds/bass_drum.wav")
            play_once = False
            open_door = True

    pygame.display.update()
    # pygame.display.flip()
    FPS_CLOCK.tick(FPS)
