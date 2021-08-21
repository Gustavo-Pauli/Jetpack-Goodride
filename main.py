import pygame
import random
import sys
from settings import *


def move_background():
    screen.blit(bg_surface, (bg_pos_x, 0))  # put bg_surface on screen surface
    screen.blit(bg_surface, (bg_pos_x + 1536, 0))


def create_obstacle():
    # [rect object, relative position] TODO change 100% random y to choose from a list
    return [obstacles_surface.get_rect(center=[1920, random.randint(190, 540)]), obstacle_num * 620]


# receive a obstacle list, move and draw them
def move_obstacles(obstacles):
    for obstacle, relative_pos in obstacles:
        obstacle.x = obstacles_pos_x + relative_pos  # move
        screen.blit(obstacles_surface, [obstacle.x, obstacle.y])  # draw


def obstacles_check_collision(obstacles):
    for obstacle, _ in obstacles:
        if obstacle.colliderect(player_rect):  # check if any obstacle is colliding with player
            pygame.event.post(died)


def lerp(A, B, C):
    return ((1 - C) * A) + ((1 - C) * B)


def update_score():
    score_surface = default_font.render('Score: %i' % round(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(topleft=(30, 45))
    screen.blit(score_surface, score_rect)

def load_save():
    global high_score
    with open(HIGH_SCORE_LOC, 'r+') as file:
        try:
            high_score = int(file.read())
            print('past save loaded')
        except :
            file.write('0')
            high_score = 0
            print('save file created')
    print(high_score)
    file.close()

def save_game(HS):
    global high_score
    with open(HIGH_SCORE_LOC, 'w') as file:
        high_score = int(file.write(str(HS)))
        print('Saved')


####################### INITIALIZE GAME #######################
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Goodride')
pygame.display.set_icon(pygame.image.load(ICON_LOC))
clock = pygame.time.Clock()


####################### FONTS #######################
default_font = pygame.font.Font(DEFAULT_FONT_LOC, 48)


####################### AUDIOS #######################


####################### SPRITES #######################
# TODO correct bg image in photoshop
bg_surface = pygame.image.load('assets/sprites/BackdropMain.png').convert()  # convert the image to a pygame lightweight format
bg_surface = pygame.transform.scale2x(bg_surface)  # double the size

player_fly_surface = pygame.image.load('assets/sprites/PlayerFly.png').convert_alpha()
player_fly_surface = pygame.transform.scale(player_fly_surface, [64, 68])  # 1.3x (69, 74))

player_dead_surface = pygame.image.load('assets/sprites/PlayerDead.png').convert_alpha()
player_dead_surface = pygame.transform.scale(player_dead_surface, [82, 74])

player_surface = player_fly_surface  # default player sprite
player_rect = player_surface.get_rect(center=(256, 360))  # return new rectangle covering entire surface

obstacles_surface = pygame.image.load('assets/sprites/Zapper1.png').convert_alpha()
obstacles_surface = pygame.transform.scale2x(obstacles_surface)
# obstacle_rect = obstacles_surface.get_rect(center=(1920, 360))


####################### USER EVENTS #######################
spawn_obstacle = pygame.USEREVENT

DIED = pygame.USEREVENT + 1  # event id
died = pygame.event.Event(DIED)  # event object


####################### GLOBAL VARIABLES #######################
score = 0
high_score = 0

gravity = GRAVITY

is_moving_up = False
dead = False
player_pos_y = 0
player_vel_x = DEFAULT_VELOCITY_X  # TODO make game progressive faster
player_vel_y = 0

bg_pos_x = 0

obstacles_pos_x = OBSTACLE_OFFSET
obstacles_list = []
obstacle_num = 0
pygame.time.set_timer(spawn_obstacle, OBSTACLE_SPAWN_TIME)  # call the event spawn_obstacle every x milliseconds

lerp_factor = 0
lerp_x_vel = False
player_vel_x_start = 0


####################### LOAD SAVE #######################
load_save()


####################### GAME LOOP #######################
while True:
    dt = clock.tick(150)/1000  # delta time in seconds | cap fps around 120
    # print(clock.get_fps())

    # catch events
    for event in pygame.event.get():  # go through all events
        # quit game
        if event.type == pygame.QUIT:  # if it has a event type of QUIT, than quit
            save_game(high_score)
            pygame.quit()
            sys.exit()  # TODO see what this do

        # create new obstacle
        if event.type == spawn_obstacle:
            obstacles_list.append(create_obstacle())
            obstacle_num += 1
            # print(obstacles_list)

        # kill player
        if event.type == DIED and not dead:
            dead = True
            is_moving_up = False
            player_surface = player_dead_surface
            lerp_x_vel = True
            player_vel_x_start = player_vel_x

            if round(score) > high_score:
                high_score = round(score)
                print('New high score!')

        # inputs key down
        if event.type == pygame.KEYDOWN and not dead:
            if event.key == pygame.K_w:
                is_moving_up = True

        # inputs key up
        if event.type == pygame.KEYUP and not dead:
            if event.key == pygame.K_w:
                is_moving_up = False

    # do the death lerp velocity
    if lerp_x_vel:
        lerp_factor += dt*0.75
        player_vel_x = lerp(player_vel_x_start, 0, lerp_factor)
        if player_vel_x <= 0:
            lerp_x_vel = False
            player_vel_x = 0

    # background movement
    bg_pos_x -= player_vel_x * dt
    move_background()
    if bg_pos_x <= -1536:
        bg_pos_x += 1536

    # obstacle movement
    obstacles_pos_x -= player_vel_x * dt * 1.1
    move_obstacles(obstacles_list)
    obstacles_check_collision(obstacles_list)

    # player velocity (up || down)
    if not is_moving_up:
        player_vel_y += gravity * dt * 1000
    else:
        player_vel_y += -gravity * dt * 1000

    # keep player inside the bound
    if player_pos_y < 80:  # if touch celling
        player_pos_y = 80
        player_vel_y = 0
    elif player_pos_y > 645 - player_surface.get_size()[0]:  # if touch ground
        player_pos_y = 645 - player_surface.get_size()[0]
        player_vel_y = 0
    else:
        player_pos_y += player_vel_y * dt

    # update player position and draw
    player_rect.y = player_pos_y
    screen.blit(player_surface, player_rect)

    # score
    if not dead:
        score += dt * 25
    update_score()

    # debug player hitbox
    # pygame.draw.rect(player_surface, [255, 255, 255, 80], pygame.Rect(0, 0, 200, 200))

    pygame.display.update()
