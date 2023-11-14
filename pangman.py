import pygame, sys
import pygame.locals as pygame_locals

import serial

SERIAL_PORT = "COM18"
BAUD_RATE = 115200
BYTE_SIZE = 7
PARITY = "O"
STOP_BITS = 1

ser = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    BYTE_SIZE,
    PARITY,
    STOP_BITS,
)  # open serial port
print(ser.name)  # check which port was really used

# ser.close()  # close port

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
BALL_VEL_HORIZONTAL = 4
BALL_VEL_VERTICAL = 4
ball_pos = [0.0, 0.0]
ball_vel = [BALL_VEL_HORIZONTAL, BALL_VEL_VERTICAL]
paddle1_vel = 0
paddle2_vel = 0
MAX_ANGLE = 160
MIN_ANGLE = 20
MAX_DIST = 50
MIN_DIST = 10
DIST_DIFF = MAX_DIST - MIN_DIST

letter_ascii = ord("A")

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pong")


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init():
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    ball_init()


# draw function of canvas
def draw(canvas: pygame.surface.Surface):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, letter_ascii, ser

    canvas.fill(BLACK)

    # receive serial measure
    meas = ser.read(8).decode()
    angle = int(meas.split(",")[0])
    distance = int(meas.split(",")[1].replace("#", ""))

    distance = min(distance, MAX_DIST)
    distance = max(distance, MIN_DIST)

    # update paddle position
    paddle1_pos[1] = max(
        (HEIGHT - HALF_PAD_HEIGHT)
        - (((HEIGHT - HALF_PAD_HEIGHT) / DIST_DIFF) * (distance - MIN_DIST)),
        HALF_PAD_HEIGHT,
    )
    print(paddle1_pos[1])

    # update ball
    ball_pos[0] = (WIDTH - BALL_DIAMETER - PAD_WIDTH) - (
        (WIDTH - BALL_DIAMETER - PAD_WIDTH) / (MAX_ANGLE - MIN_ANGLE)
    ) * (angle - MIN_ANGLE)
    ball_pos[1] += ball_vel[1]
    print(meas)

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
            [paddle2_pos[0] - HALF_PAD_WIDTH, 0],
            [paddle2_pos[0] - HALF_PAD_WIDTH, HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, 0],
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
        if letter_ascii >= ord("Z"):
            letter_ascii = ord("A")
        else:
            letter_ascii += 1
    elif ball_pos[0] <= PAD_WIDTH:
        ball_init()
        letter_ascii = ord("A")

    if ball_pos[0] == WIDTH - BALL_DIAMETER - PAD_WIDTH:
        ball_vel[0] = -ball_vel[0]

    # current letter
    font = pygame.font.SysFont("mono", 20, True)
    label1 = font.render("Letter " + chr(letter_ascii), True, WHITE)
    canvas.blit(label1, (50, 20))


# keydown handler
def keydown(event: pygame.event.Event):
    global paddle1_vel, paddle2_vel

    # if event.key == K_UP:
    #     paddle2_vel = -8
    # elif event.key == K_DOWN:
    #     paddle2_vel = 8
    # elif event.key == K_w:
    if event.key == pygame_locals.K_w:
        paddle1_vel = -8
    elif event.key == pygame_locals.K_s:
        paddle1_vel = 8


# keyup handler
def keyup(event: pygame.event.Event):
    global paddle1_vel, paddle2_vel

    # if event.key in (pygame_locals.K_w, pygame_locals.K_s):
    #     paddle1_vel = 0
    # elif event.key in (pygame_locals.K_UP, pygame_locals.K_DOWN):
    #     paddle2_vel = 0
    if event.key == pygame_locals.K_q:
        pygame.event.post(pygame.event.Event(pygame_locals.QUIT))


init()

# game loop
while True:
    draw(window)

    for event in pygame.event.get():
        if event.type == pygame_locals.KEYDOWN:
            keydown(event)
        elif event.type == pygame_locals.KEYUP:
            keyup(event)
        elif event.type == pygame_locals.QUIT:
            ser.close()
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
