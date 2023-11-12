# PONG pygame

import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# globals
WIDTH = 600
HEIGHT = 400
BALL_DIAMETER = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
BALL_VEL_HORIZONTAL = 2
BALL_VEL_VERTICAL = 2
ball_pos = [0, 0]
ball_vel = [BALL_VEL_HORIZONTAL, BALL_VEL_VERTICAL]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pong")


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right: bool = False):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = -horz


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    l_score = 0
    r_score = 0
    ball_init(random.randrange(0, 2) == 0)


# draw function of canvas
def draw(canvas: pygame.Surface):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    # update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # draw paddles and ball
    rect = pygame.Rect(ball_pos[0], ball_pos[1], BALL_DIAMETER, BALL_DIAMETER)
    pygame.draw.rect(canvas, WHITE, rect, BALL_DIAMETER)
    pygame.draw.polygon(
        canvas,
        WHITE,
        [
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
        ],
    )
    pygame.draw.polygon(
        canvas,
        WHITE,
        [
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
        ],
    )

    # ball collision check on top and bottom walls
    if int(ball_pos[1]) == 0:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT - BALL_DIAMETER:
        ball_vel[1] = -ball_vel[1]

    # ball collision check on gutters or paddles
    if ball_pos[0] <= PAD_WIDTH and (
        ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT - BALL_DIAMETER
        and ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
    elif ball_pos[0] <= PAD_WIDTH:
        print(ball_pos, paddle1_pos)
        r_score += 1
        ball_init(True)

    if ball_pos[0] >= WIDTH - BALL_DIAMETER - PAD_WIDTH and (
        ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT - BALL_DIAMETER
        and ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
    elif ball_pos[0] >= WIDTH - BALL_DIAMETER - PAD_WIDTH:
        print(ball_pos, paddle2_pos)
        l_score += 1
        ball_init(False)

    # update scores
    my_font1 = pygame.font.SysFont("mono", 20, True)
    label1 = my_font1.render("Score " + str(l_score), 1, WHITE)
    canvas.blit(label1, (50, 20))

    my_font2 = pygame.font.SysFont("mono", 20, True)
    label2 = my_font2.render("Score " + str(r_score), 1, WHITE)
    canvas.blit(label2, (470, 20))


# keydown handler
def keydown(event: pygame.event.Event):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8


# keyup handler
def keyup(event: pygame.event.Event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0


init()


# game loop
while True:
    draw(window)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
