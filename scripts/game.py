import pygame
import random
import sys
import scripts.tools as tools
import scripts.settings as settings


class Game:

    def __init__(self, main):
        self.main = main

        # paused screen black overlay
        self.paused_screen_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA, 32)
        self.death_screen_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA, 32)

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

        # death screen buttons image
        self.play_again_image = pygame.image.load('assets/sprites/ButtonPlayAgain.png').convert_alpha()
        self.shop_image = pygame.image.load('assets/sprites/ButtonShopDeathScreen.png').convert_alpha()

        ####################### USER EVENTS #######################

        self.DIED = pygame.USEREVENT + 1  # event id
        self.died = pygame.event.Event(self.DIED)  # event object

        ####################### GLOBAL VARIABLES #######################

        self.gravity = settings.GRAVITY  # TODO maybe a item that change gravity?

        # score
        self.score = 0
        self.high_score = 0
        self.coins_collected = 0
        self.coins = 0

        # player
        self.is_moving_up = False
        self.dead = False
        self.paused = False
        self.player_pos_y = 645
        self.player_pos_x = -100
        self.player_vel_x = settings.DEFAULT_X_VELOCITY  # TODO make game progressive faster
        self.player_vel_y = 0

        # objets positions
        self.bg_pos_x = 0
        self.foreground_pos_x = 0  # obstacles and coins pos FIRST_OBSTACLE_OFFSET

        # obstacles
        self.obstacles_list = []
        self.obstacle_num = 0

        # lerp
        self.lerp_factor = 0
        self.lerp_x_vel = False
        self.player_vel_x_start = 0

        self.timer1 = 0
        self.lerp_start_velocity = True

        # death screen buttons
        self.button_play_again = tools.Button(self.main.screen, self.play_again_image, (settings.WIDTH * 9.5 // 13, 320), 'center')
        self.button_shop = tools.Button(self.main.screen, self.shop_image, (settings.WIDTH * 9.5 // 13, 416), 'center')

        ####################### LOAD SAVE #######################
        self.load_save()

    def update_game(self, main):
        self.main = main

        self.check_events(main)
        if self.paused:
            self.main.dt = 0
        self.check_obstacles()
        self.move_things()
        if self.dead:
            self.draw_deathscreen()
        else:
            self.draw_score_gui()
        self.check_collisions()
        self.update_x_velocity()
        self.debug()

        self.check_paused()
        self.reset_keys()
        pygame.display.update()

    ################## MOVE ##################

    # TODO move this to game loop and functions
    def move_things(self):
        # do the death lerp velocity
        if self.lerp_x_vel:
            self.lerp_factor += self.main.dt*0.75
            self.player_vel_x = self.lerp(self.player_vel_x_start, 0, self.lerp_factor)
            if self.player_vel_x <= 0:
                self.lerp_x_vel = False
                self.player_vel_x = 0

        # TEST
        # if not self.lerp_start_velocity:  # block controls at start
        if self.lerp_start_velocity:
            lerping_time = 4
            self.timer1 += self.main.dt / lerping_time  # divided by time in seconds of lerp

            # lerp velocity
            self.player_vel_x = settings.DEFAULT_X_VELOCITY - self.lerp(0, settings.DEFAULT_X_VELOCITY, self.timer1)

            # lerp position x
            self.player_pos_x = 256 - self.lerp(100, 256, self.timer1)
            if self.timer1 >= 1 or self.player_vel_x >= settings.DEFAULT_X_VELOCITY:
                self.lerp_start_velocity = False
                self.player_vel_x = settings.DEFAULT_X_VELOCITY
                self.player_pos_x = 256

        # background movement
        self.move_background()

        # obstacle movement
        self.foreground_pos_x -= self.player_vel_x * self.main.dt * 1.1  # 1.1 is for parallax with background
        self.move_obstacles(self.obstacles_list)

        # change player velocity (up || down) -change faster if going faster
        if not self.is_moving_up:
            self.player_vel_y += self.gravity * self.main.dt * self.player_vel_x * 1.8
        else:
            self.player_vel_y += -self.gravity * self.main.dt * self.player_vel_x * 1.8

        # keep player inside the bound
        if self.player_pos_y < 80:  # if touch celling
            self.player_pos_y = 80
            self.player_vel_y = 0
        elif self.player_pos_y > 645 - self.player_surface.get_size()[0]:  # if touch ground
            self.player_pos_y = 645 - self.player_surface.get_size()[0]
            self.player_vel_y = 0
        else:
            self.player_pos_y += self.player_vel_y * self.main.dt

        # update player position and draw
        self.player_rect.y = self.player_pos_y
        self.player_rect.x = self.player_pos_x
        self.main.screen.blit(self.player_surface, self.player_rect)

        # increase distance
        if not self.dead:
            self.score += self.main.dt * self.player_vel_x * 0.05  # TODO change this to foreground x pos

    def move_background(self):
        self.bg_pos_x -= self.player_vel_x * self.main.dt
        self.main.screen.blit(self.bg_surface, (self.bg_pos_x, 0))  # put bg_surface on screen surface
        self.main.screen.blit(self.bg_surface, (self.bg_pos_x + 1536, 0))
        if self.bg_pos_x <= -1536:
            self.bg_pos_x += 1536

    # receive a obstacle list, move and draw them
    def move_obstacles(self, obstacles):
        for obstacle, relative_pos in obstacles:
            obstacle.x = self.foreground_pos_x + relative_pos  # move
            self.main.screen.blit(self.obstacles_surface, [obstacle.x, obstacle.y])  # draw

    ################## CREATE ##################

    def create_obstacle(self):
        # [rect object, relative position] TODO change 100% random y to choose from a list
        return [self.obstacles_surface.get_rect(center=(0, random.randint(190, 540))), settings.FIRST_OBSTACLE_OFFSET - self.foreground_pos_x]

    ################## COLLISION ##################

    def check_collisions(self):
        # check obstacles collisions
        self.obstacles_check_collision(self.obstacles_list)

        # TODO check coin collisions

    def obstacles_check_collision(self, obstacles):
        for obstacle, _ in obstacles:
            if obstacle.colliderect(self.player_rect):  # check if any obstacle is colliding with player
                pygame.event.post(self.died)

    ################## LOAD/SAVE ##################

    # TODO maybe move this to main, load and save options too

    def load_save(self):
        try:
            with open(settings.HIGH_SCORE_LOC, 'r+') as file:
                self.high_score = int(file.read())
                print('past save loaded')
        except:
            with open(settings.HIGH_SCORE_LOC, 'w+') as file:
                file.write('0')
                print('save file created')
        print(self.high_score)

    def save_game(self, HS):
        with open(settings.HIGH_SCORE_LOC, 'w') as file:
            self.score = int(file.write(str(HS)))
            print('Saved')

    #################### DEBUG ####################

    def debug(self):
        if settings.DEBUG:
            if settings.DEBUG_HIT_BOXES:
                self.debug_hit_boxes()
            if settings.DEBUG_SCREEN_SIZE_BOX:
                self.debug_screen_box()

    def debug_hit_boxes(self):
        # obstacles
        pygame.draw.rect(self.obstacles_surface, settings.YELLOW, pygame.Rect(0, 0, 92, 218), 1)

        # player
        if not self.dead:  # flying
            pygame.draw.rect(self.player_surface, settings.YELLOW, pygame.Rect(0, 0, 64, 68), 1)
        elif self.dead:  # dead
            pygame.draw.rect(self.player_surface, settings.YELLOW, pygame.Rect(0, 0, 82, 74), 1)

    def debug_screen_box(self):
        pygame.draw.rect(self.main.screen, settings.YELLOW, pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT), 1)

    ###############################################

    def check_events(self, main):  # catch events
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
                # pause
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
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
        if -self.foreground_pos_x > settings.OBSTACLE_OFFSET * (self.obstacle_num):
            self.obstacles_list.append(self.create_obstacle())
            self.obstacle_num += 1
            print(len(self.obstacles_list))

        # destroy obstacles if has more than needed
        if len(self.obstacles_list) > 12:
            self.obstacles_list.pop(0)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False, False, False, False

    def update_x_velocity(self):
        if not self.dead and self.player_vel_x < settings.MAX_X_VELOCITY and not self.lerp_start_velocity:
            self.player_vel_x += self.main.dt * 4  # make game progressive faster

    def check_paused(self):
        if self.paused:
            self.paused_screen_surface.fill((0, 0, 0, 140))
            self.main.screen.blit(self.paused_screen_surface, (0, 0))
            tools.draw_text(self.main.screen, 'PAUSED', 'center', 96, (settings.WIDTH // 2, settings.HEIGHT // 2))

    def draw_score_gui(self):
        tools.draw_text(self.main.screen, 'Distance: %i' % round(self.score), 'left', 48, (34, 90))
        tools.draw_text(self.main.screen, 'Velocity: %i' % round(self.player_vel_x), 'left', 32, (34, 116))

    def draw_deathscreen(self):
        # draw dark overlay
        self.death_screen_surface.fill((0, 0, 0, 170))
        self.main.screen.blit(self.death_screen_surface, (0, 0))

        tools.draw_text(self.main.screen, 'you flew', 'center', 63, (settings.WIDTH * 4 // 13, settings.HEIGHT * 4.62 // 13))
        tools.draw_text(self.main.screen, '%im' % self.score, 'center', 161, (settings.WIDTH * 4 // 13, settings.HEIGHT * 6.32 // 13), settings.YELLOW_COIN)

        tools.draw_text(self.main.screen, 'and collected', 'center', 38, ((settings.WIDTH * 4 // 13), settings.HEIGHT * 7.86 // 13))  # 89
        tools.draw_text(self.main.screen, '%i coins' % self.coins_collected, 'center', 38, ((settings.WIDTH * 4 // 13), settings.HEIGHT * 8.53 // 13), settings.YELLOW_COIN)

        # draw buttons
        self.button_play_again.draw()
        self.button_shop.draw()

        # detect click
        if self.button_play_again.check_collision():
            self.main.game = Game(self.main)  # instantiate game
        if self.button_shop.check_collision():
            self.main.menu.current_menu = 'Shop'
            self.main.in_menu = True
            self.main.playing = False


    @staticmethod
    def lerp(A, B, C):
        return ((1 - C) * A) + ((1 - C) * B)
