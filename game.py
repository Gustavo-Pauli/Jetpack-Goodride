import pygame
import random
import sys
from settings import *


class Game:

    def __init__(self):
        ####################### INITIALIZE GAME #######################
        pygame.init()
        self.running = True  # running the program
        self.playing = False  # in gameplay part
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Jetpack Goodride')
        pygame.display.set_icon(pygame.image.load(ICON_LOC))
        self.clock = pygame.time.Clock()
        self.dt = None

        ####################### AUDIOS #######################

        ####################### SPRITES #######################
        # TODO correct bg image in photoshop
        self.bg_surface = pygame.image.load('assets/sprites/BackdropMain.png').convert()  # convert the image to a pygame lightweight format
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)  # double the size

        self.player_fly_surface = pygame.image.load('assets/sprites/PlayerFly.png').convert_alpha()
        self.player_fly_surface = pygame.transform.scale(self.player_fly_surface, [64, 68])  # 1.3x (69, 74))

        self.player_dead_surface = pygame.image.load('assets/sprites/PlayerDead.png').convert_alpha()
        self.player_dead_surface = pygame.transform.scale(self.player_dead_surface, [82, 74])

        self.player_surface = self.player_fly_surface  # default player sprite
        self.player_rect = self.player_surface.get_rect(center=(256, 360))  # return new rectangle covering entire surface

        self.obstacles_surface = pygame.image.load('assets/sprites/Zapper1.png').convert_alpha()
        self.obstacles_surface = pygame.transform.scale2x(self.obstacles_surface)
        # self.obstacle_rect = self.obstacles_surface.get_rect(center=(1920, 360))

        ####################### USER EVENTS #######################
        # self.spawn_obstacle = pygame.USEREVENT

        self.DIED = pygame.USEREVENT + 1  # event id
        self.died = pygame.event.Event(self.DIED)  # event object

        ######################## COLORS #########################
        self.BLACK = pygame.color.Color(0, 0, 0)
        self.WHITE = pygame.color.Color(255, 255, 255)
        self.YELLOW = pygame.color.Color(255, 255, 0)

        ####################### GLOBAL VARIABLES #######################
        self.score = 0
        self.high_score = 0

        self.gravity = GRAVITY

        self.is_moving_up = False
        self.dead = False
        self.player_pos_y = 0
        self.player_vel_x = DEFAULT_X_VELOCITY  # TODO make game progressive faster
        self.player_vel_y = 0

        self.bg_pos_x = 0

        self.foreground_pos_x = 0  # obstacles and coins pos FIRST_OBSTACLE_OFFSET
        self.obstacles_list = []
        self.obstacle_num = 0
        # pygame.time.set_timer(self.spawn_obstacle, OBSTACLE_SPAWN_TIME)  # call the event spawn_obstacle every x milliseconds

        self.lerp_factor = 0
        self.lerp_x_vel = False
        self.player_vel_x_start = 0

        # MENU KEYS
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False

        ####################### LOAD SAVE #######################
        self.load_save()

    def game_loop(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # delta time in seconds | cap fps around 120

            self.check_events()
            self.check_obstacles()
            self.move_things()
            self.check_collisions()
            self.update_x_velocity()
            self.debug()

            # if self.START_KEY:
            #     self.playing = False

            # GUI
            self.draw_text('Distance: %i' % round(self.score), 'left', 48, (34, 90))
            self.draw_text('Velocity: %i' % round(self.player_vel_x), 'left', 32, (34, 116))

            self.reset_keys()
            pygame.display.update()

    ################## MOVE ##################

    # TODO move this to game loop
    def move_things(self):
        # do the death lerp velocity
        if self.lerp_x_vel:
            self.lerp_factor += self.dt*0.75
            self.player_vel_x = self.lerp(self.player_vel_x_start, 0, self.lerp_factor)
            if self.player_vel_x <= 0:
                self.lerp_x_vel = False
                self.player_vel_x = 0

        # background movement
        self.move_background()

        # obstacle movement
        self.foreground_pos_x -= self.player_vel_x * self.dt * 1.1  # 1.1 is for parallax with background
        self.move_obstacles(self.obstacles_list)

        # change player velocity (up || down) -change faster if going faster
        if not self.is_moving_up:
            self.player_vel_y += self.gravity * self.dt * self.player_vel_x * 1.8
        else:
            self.player_vel_y += -self.gravity * self.dt * self.player_vel_x * 1.8

        # keep player inside the bound
        if self.player_pos_y < 80:  # if touch celling
            self.player_pos_y = 80
            self.player_vel_y = 0
        elif self.player_pos_y > 645 - self.player_surface.get_size()[0]:  # if touch ground
            self.player_pos_y = 645 - self.player_surface.get_size()[0]
            self.player_vel_y = 0
        else:
            self.player_pos_y += self.player_vel_y * self.dt

        # update player position and draw
        self.player_rect.y = self.player_pos_y
        self.screen.blit(self.player_surface, self.player_rect)

        # increase distance
        if not self.dead:
            self.score += self.dt * self.player_vel_x * 0.05  # TODO change this to foreground x pos

    def move_background(self):
        self.bg_pos_x -= self.player_vel_x * self.dt
        self.screen.blit(self.bg_surface, (self.bg_pos_x, 0))  # put bg_surface on screen surface
        self.screen.blit(self.bg_surface, (self.bg_pos_x + 1536, 0))
        if self.bg_pos_x <= -1536:
            self.bg_pos_x += 1536

    # receive a obstacle list, move and draw them
    def move_obstacles(self, obstacles):
        for obstacle, relative_pos in obstacles:
            obstacle.x = self.foreground_pos_x + relative_pos  # move
            self.screen.blit(self.obstacles_surface, [obstacle.x, obstacle.y])  # draw

    ################## CREATE ##################

    def create_obstacle(self):
        # [rect object, relative position] TODO change 100% random y to choose from a list
        return [self.obstacles_surface.get_rect(center=[0, random.randint(190, 540)]), self.obstacle_num * OBSTACLE_OFFSET + FIRST_OBSTACLE_OFFSET]

    ################## COLLISION ##################

    def check_collisions(self):
        # check obstacles collisions
        self.obstacles_check_collision(self.obstacles_list)

        # TODO check coin collisions

    def obstacles_check_collision(self, obstacles):
        for obstacle, _ in obstacles:
            if obstacle.colliderect(self.player_rect):  # check if any obstacle is colliding with player
                pygame.event.post(self.died)

    ################## LOAD/SAVE ################## TODO move this to main maybe, load and save options too

    def load_save(self):
        try:
            with open(HIGH_SCORE_LOC, 'r+') as file:
                self.high_score = int(file.read())
                print('past save loaded')
        except:
            with open(HIGH_SCORE_LOC, 'w+') as file:
                file.write('0')
                print('save file created')
        print(self.high_score)

    def save_game(self, HS):
        with open(HIGH_SCORE_LOC, 'w') as file:
            self.score = int(file.write(str(HS)))
            print('Saved')

    #################### DEBUG ####################

    def debug(self):
        if DEBUG:
            if DEBUG_HIT_BOXES:
                self.debug_hit_boxes()
            if DEBUG_SCREEN_SIZE_BOX:
                self.debug_screen_box()

    def debug_hit_boxes(self):
        # obstacles
        pygame.draw.rect(self.obstacles_surface, self.YELLOW, pygame.Rect(0, 0, 92, 218), 1)

        # player
        if not self.dead:  # flying
            pygame.draw.rect(self.player_surface, self.YELLOW, pygame.Rect(0, 0, 64, 68), 1)
        elif self.dead:  # dead
            pygame.draw.rect(self.player_surface, self.YELLOW, pygame.Rect(0, 0, 82, 74), 1)

    def debug_screen_box(self):
        pygame.draw.rect(self.screen, self.YELLOW, pygame.Rect(0, 0, WIDTH, HEIGHT), 1)

    ###############################################

    def check_events(self):  # catch events
        for event in pygame.event.get():  # go through all events
            # quit game
            if event.type == pygame.QUIT:  # if it has a event type of QUIT, than quit
                self.save_game(self.high_score)
                pygame.quit()
                sys.exit()

            # kill player
            if event.type == self.DIED and not self.dead:
                self.dead = True
                self.is_moving_up = False
                self.player_surface = self.player_dead_surface
                self.lerp_x_vel = True
                self.player_vel_x_start = self.player_vel_x

                if round(self.score) > self.high_score:
                    self.high_score = round(self.score)
                    print('New high score!')

            # inputs key down
            if event.type == pygame.KEYDOWN and not self.dead:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_w:
                    self.UP_KEY = True

                # in game key, maybe change later
                if event.key == pygame.K_w:
                    self.is_moving_up = True

            # inputs key up
            if event.type == pygame.KEYUP and not self.dead:
                if event.key == pygame.K_w:
                    self.is_moving_up = False

    # check if need to create or destroy obstacles this frame, and do if needed
    def check_obstacles(self):
        # create obstacles if needed
        # travelled distance > distance covered with obstacles until now
        if -self.foreground_pos_x > OBSTACLE_OFFSET * (self.obstacle_num + 1):
            self.obstacles_list.append(self.create_obstacle())
            self.obstacle_num += 1
            print(len(self.obstacles_list))

        # destroy obstacles if has more than needed
        if len(self.obstacles_list) > 12:
            self.obstacles_list.pop(0)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False, False, False, False

    def lerp(self, A, B, C):
        return ((1 - C) * A) + ((1 - C) * B)

    def update_x_velocity(self):
        if not self.dead and self.player_vel_x < MAX_X_VELOCITY:
            self.player_vel_x += self.dt * 4  # make game progressive faster

    def draw_text(self, text, align, size, pos):
        font = pygame.font.Font(DEFAULT_FONT_LOC, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        if align == 'center':
            text_rect.center = pos
        elif align == 'left':
            text_rect.bottomleft = pos
        elif align == 'right':
            text_rect.bottomright = pos
        else:
            raise ValueError('Align option not valid')
        self.screen.blit(text_surface, text_rect)

