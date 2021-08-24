import pygame
import sys
import scripts.tools as tools
import scripts.settings as settings


# base class for menu
class Menu:
    def __init__(self, main):
        self.main = main

        # background image
        self.background_image = pygame.image.load('assets/sprites/BackdropMain.png')
        self.background_image = pygame.transform.scale2x(self.background_image)

        # logo
        self.logo_image = pygame.image.load('assets/sprites/LogoGlow.png').convert_alpha()
        self.logo_image = pygame.transform.smoothscale(self.logo_image, (int(self.logo_image.get_size()[0]*0.8), int(self.logo_image.get_size()[1]*0.8)))

        # buttons images
        self.play_game_image = pygame.image.load('assets/sprites/ButtonPlayGame.png').convert_alpha()
        self.shop_image = pygame.image.load('assets/sprites/ButtonShop.png').convert_alpha()
        self.settings_image = pygame.image.load('assets/sprites/ButtonSettings.png').convert_alpha()
        self.quit_image = pygame.image.load('assets/sprites/ButtonQuit.png').convert_alpha()
        self.sound_on_image = pygame.image.load('assets/sprites/SoundOn.png').convert_alpha()

        # buttons
        self.button_play_game = tools.Button(self.main.screen, self.play_game_image, (settings.WIDTH/2, 425), 'center')
        self.button_shop = tools.Button(self.main.screen, self.shop_image, (settings.WIDTH / 2, 484), 'center')
        self.button_settings = tools.Button(self.main.screen, self.settings_image, (settings.WIDTH / 2, 536), 'center')
        self.button_quit = tools.Button(self.main.screen, self.quit_image, (settings.WIDTH / 2, 589), 'center')
        self.button_sound_on = tools.Button(self.main.screen, self.sound_on_image, (1234, 0))

        # self.button_list = [self.button_play_game, self.button_shop, self.button_settings, self.button_quit, self.button_sound_on]

    def update_menu(self, main):
        self.main = main
        self.check_events()

        self.draw_background()
        self.draw_logo()
        self.draw_buttons()

        self.check_buttons_interactions()

        '''for button in self.button_list:
            button.draw()
            button.check_collision()'''

        pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():  # go through all events
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # inputs key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.playing = True
                    self.main.menu = False  # TODO REMOVE THIS LATER / JUST FOR TESTING

    def draw_background(self):
        self.main.screen.blit(self.background_image, (0, 0))

    def draw_logo(self):
        self.main.screen.blit(self.logo_image, (settings.WIDTH // 2 - self.logo_image.get_size()[0] // 2, 70))

    def draw_buttons(self):
        self.button_play_game.draw()
        self.button_shop.draw()
        self.button_settings.draw()
        self.button_quit.draw()
        self.button_sound_on.draw()

    def check_buttons_interactions(self):
        if self.button_play_game.check_collision():
            self.main.playing = True
            self.main.menu = False
        if self.button_shop.check_collision():
            pass
        if self.button_settings.check_collision():
            pass
        if self.button_quit.check_collision():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if self.button_sound_on.check_collision():
            pass
