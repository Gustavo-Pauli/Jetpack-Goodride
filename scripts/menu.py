import pygame
import sys
import scripts.tools as tools
import scripts.settings as settings
import scripts.game as game


# base class for menu
class Menu:
    def __init__(self, main):
        self.main = main

        self.current_menu = 'MainMenu'

        self.main_menu = MainMenu(self)
        self.shop = Shop(self)
        self.credits = Credits(self)

        # background image
        self.background_image = pygame.image.load('assets/sprites/BackdropMain.png')
        self.background_image = pygame.transform.scale2x(self.background_image)

        # music
        pygame.mixer.music.load('assets/sounds/MainMenu.wav')
        pygame.mixer.music.set_volume(self.main.global_volume * self.main.music_volume)
        pygame.mixer.music.play(-1, fade_ms=2300)

        # buttons images
        self.sound_on_image = pygame.image.load('assets/sprites/ButtonSoundOn.png').convert_alpha()
        self.sound_off_image = pygame.image.load('assets/sprites/ButtonSoundOff.png').convert_alpha()
        self.music_on_image = pygame.image.load('assets/sprites/ButtonMusicOn.png').convert_alpha()
        self.music_off_image = pygame.image.load('assets/sprites/ButtonMusicOff.png').convert_alpha()

        # buttons
        self.button_sound = tools.Button(self.main.screen, self.sound_on_image, (1206, 20))
        self.button_music = tools.Button(self.main.screen, self.music_on_image, (1144, 20))

    def update_menu(self, main):
        self.main = main

        if self.current_menu == 'MainMenu':
            self.main_menu.update()
        elif self.current_menu == 'Shop':
            self.shop.update()
        elif self.current_menu == 'Credits':
            self.credits.update()

        pygame.mixer.music.set_volume(self.main.global_volume * self.main.music_volume)

        # if music is not playing
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('assets/sounds/MainMenu.wav')
            pygame.mixer.music.play(-1, fade_ms=2300)

        pygame.display.update()

    def draw_background(self):
        self.main.screen.blit(self.background_image, (0, 0))

    def draw_sound_music_buttons(self):
        # draw sound button
        if self.main.sound_on:
            self.button_sound.image = self.sound_on_image
            self.button_sound.draw()
        else:
            self.button_sound.image = self.sound_off_image
            self.button_sound.draw()

        # draw music button
        if self.main.music_on:
            self.button_music.image = self.music_on_image
            self.button_music.draw()
        else:
            self.button_music.image = self.music_off_image
            self.button_music.draw()

    def check_sound_music_buttons_interactions(self):
        if self.button_sound.check_collision():
            self.mute_audio()
        if self.button_music.check_collision():
            self.mute_music()

    def mute_audio(self):
        if self.main.sound_on:
            self.main.sound_on = False
            self.main.last_global_volume = self.main.global_volume
            self.main.global_volume = 0
        else:
            self.main.sound_on = True
            self.main.global_volume = self.main.last_global_volume
            self.main.last_global_volume = 0

    def mute_music(self):
        if self.main.music_on:
            self.main.music_on = False
            self.main.last_music_volume = self.main.music_volume
            self.main.music_volume = 0
        else:
            self.main.music_on = True
            self.main.music_volume = self.main.last_music_volume
            self.main.last_music_volume = 0


class MainMenu:
    def __init__(self, menu):
        self.menu = menu

        # logo
        self.logo_image = pygame.image.load('assets/sprites/LogoGlow.png').convert_alpha()
        self.logo_image = pygame.transform.smoothscale(self.logo_image, (int(self.logo_image.get_size()[0] * 0.8), int(self.logo_image.get_size()[1] * 0.8)))

        # buttons images
        self.play_game_image = pygame.image.load('assets/sprites/ButtonPlayGame.png').convert_alpha()
        self.shop_image = pygame.image.load('assets/sprites/ButtonShop.png').convert_alpha()
        self.settings_image = pygame.image.load('assets/sprites/ButtonCredits.png').convert_alpha()
        self.quit_image = pygame.image.load('assets/sprites/ButtonQuit.png').convert_alpha()
        self.sound_on_image = pygame.image.load('assets/sprites/SoundOn.png').convert_alpha()

        # buttons
        self.button_play_game = tools.Button(self.menu.main.screen, self.play_game_image, (settings.WIDTH / 2, 425), 'center')
        self.button_shop = tools.Button(self.menu.main.screen, self.shop_image, (settings.WIDTH / 2, 484), 'center')
        self.button_settings = tools.Button(self.menu.main.screen, self.settings_image, (settings.WIDTH / 2, 536), 'center')
        self.button_quit = tools.Button(self.menu.main.screen, self.quit_image, (settings.WIDTH / 2, 589), 'center')
        self.button_sound_on = tools.Button(self.menu.main.screen, self.sound_on_image, (1234, 0))

    def update(self):
        self.check_events()

        self.menu.draw_background()
        self.draw_logo()
        self.draw_buttons()

        self.check_buttons_interactions()

    def check_events(self):
        for event in pygame.event.get():  # go through all events
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # inputs key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.main.playing = True
                    self.menu.main.menu = False  # TODO REMOVE THIS LATER / JUST FOR TESTING

    def draw_logo(self):
        self.menu.main.screen.blit(self.logo_image, (settings.WIDTH // 2 - self.logo_image.get_size()[0] // 2, 70))

    def draw_buttons(self):
        self.button_play_game.draw()
        self.button_shop.draw()
        self.button_settings.draw()
        self.button_quit.draw()
        self.menu.draw_sound_music_buttons()

    def check_buttons_interactions(self):
        if self.button_play_game.check_collision():
            self.menu.main.game = game.Game(self.menu.main)  # instantiate game
            self.menu.main.playing = True
            self.menu.main.in_menu = False
        if self.button_shop.check_collision():
            self.menu.current_menu = 'Shop'
        if self.button_settings.check_collision():
            self.menu.current_menu = 'Credits'
        if self.button_quit.check_collision():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.menu.check_sound_music_buttons_interactions()


class Credits:
    def __init__(self, menu):
        self.menu = menu

        self.text_y_offset = 230

        self.paused_screen_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA, 32)

        # logo
        self.logo_image = pygame.image.load('assets/sprites/LogoGlow.png').convert_alpha()
        self.logo_image = pygame.transform.smoothscale(self.logo_image, (int(self.logo_image.get_size()[0] * 0.8), int(self.logo_image.get_size()[1] * 0.8)))

        # buttons images
        self.back_image = pygame.image.load('assets/sprites/ButtonBack.png').convert_alpha()

        # buttons
        self.button_back = tools.Button(self.menu.main.screen, self.back_image, (20, 20))

    def update(self):
        self.check_events()

        self.menu.draw_background()

        self.paused_screen_surface.fill((0, 0, 0, 100))
        self.menu.main.screen.blit(self.paused_screen_surface, (0, 0))

        self.draw_logo()
        self.draw_buttons()

        tools.draw_text(self.menu.main.screen, 'Programming, GUI and logo by', 'left', 32, (settings.WIDTH * 5.6 / 10, 0 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'Gustavo Pauli', 'left', 32, (settings.WIDTH * 5.6 / 10, 32 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'Art mainly done by', 'left', 32, (settings.WIDTH * 5.6 / 10, 90 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'DarkLava', 'left', 32, (settings.WIDTH * 5.6 / 10, 122 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'New Athletic M54 font by', 'left', 32, (settings.WIDTH * 5.6 / 10, 180 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'justme54s', 'left', 32, (settings.WIDTH * 5.6 / 10, 212 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'Special thanks to HalfBrick for', 'left', 32, (settings.WIDTH * 5.6 / 10, 270 + self.text_y_offset))
        tools.draw_text(self.menu.main.screen, 'Jetpack Joyride', 'left', 32, (settings.WIDTH * 5.6 / 10, 302 + self.text_y_offset))

        self.check_buttons_interactions()

    def check_events(self):
        for event in pygame.event.get():  # go through all events
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # inputs key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.current_menu = 'MainMenu'

    def draw_logo(self):
        self.menu.main.screen.blit(self.logo_image, (settings.WIDTH * 2.8 // 10 - self.logo_image.get_size()[0] // 2,
                                                     settings.HEIGHT // 2 - self.logo_image.get_size()[1] // 2))

    def draw_buttons(self):
        self.menu.draw_sound_music_buttons()
        self.button_back.draw()

    def check_buttons_interactions(self):
        self.menu.check_sound_music_buttons_interactions()
        if self.button_back.check_collision():
            self.menu.current_menu = 'MainMenu'


class Shop:
    def __init__(self, menu):
        self.menu = menu

        self.transparency_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA, 32)

        # coins
        self.load()

        # sound  # TODO move to menu
        self.wrong_sound = pygame.mixer.Sound('assets/sounds/wrong.wav')
        self.wrong_sound.set_volume(self.menu.main.global_volume * self.menu.main.sfx_volume * 0.3)
        self.right_sound = pygame.mixer.Sound('assets/sounds/right.wav')
        self.right_sound.set_volume(self.menu.main.global_volume * self.menu.main.sfx_volume * 0.3)

        # logo
        self.logo_image = pygame.image.load('assets/sprites/LogoGlow.png').convert_alpha()
        self.logo_image = pygame.transform.smoothscale(self.logo_image, (int(self.logo_image.get_size()[0] * 0.4), int(self.logo_image.get_size()[1] * 0.4)))


        # buttons images
        self.sound_on_image = pygame.image.load('assets/sprites/SoundOn.png').convert_alpha()
        self.back_image = pygame.image.load('assets/sprites/ButtonBack.png').convert_alpha()
        self.buy_image = pygame.image.load('assets/sprites/ButtonBuy.png').convert_alpha()
        self.small_buy_image = pygame.transform.smoothscale(self.buy_image, (int(105 * 0.75), int(52 * 0.75)))
        self.select_image = pygame.image.load('assets/sprites/ButtonSelect.png').convert_alpha()
        self.small_select_image = pygame.transform.smoothscale(self.select_image, (int(105 * 0.75), int(52 * 0.75)))


        # buttons
        self.button_sound_on = tools.Button(self.menu.main.screen, self.sound_on_image, (1234, 0))
        self.button_back = tools.Button(self.menu.main.screen, self.back_image, (20, 20))

        self.button_buy_blue = tools.Button(self.menu.main.screen, self.small_buy_image, (620, 320))
        self.button_select_blue = tools.Button(self.menu.main.screen, self.small_select_image, (620, 320))

        self.button_buy_green = tools.Button(self.menu.main.screen, self.small_buy_image, (802, 320))
        self.button_select_green = tools.Button(self.menu.main.screen, self.small_select_image, (802, 320))

        self.button_buy_pink = tools.Button(self.menu.main.screen, self.small_buy_image, (984, 320))
        self.button_select_pink = tools.Button(self.menu.main.screen, self.small_select_image, (984, 320))

        self.button_buy_orange = tools.Button(self.menu.main.screen, self.small_buy_image, (620, 553))
        self.button_select_orange = tools.Button(self.menu.main.screen, self.small_select_image, (620, 553))

        self.button_buy_red = tools.Button(self.menu.main.screen, self.small_buy_image, (802, 553))
        self.button_select_red = tools.Button(self.menu.main.screen, self.small_select_image, (802, 553))

        self.button_buy_yellow = tools.Button(self.menu.main.screen, self.small_buy_image, (984, 553))
        self.button_select_yellow = tools.Button(self.menu.main.screen, self.small_select_image, (984, 553))

        self.button_buy_perry = tools.Button(self.menu.main.screen, self.buy_image, (241, 474))
        self.button_select_perry = tools.Button(self.menu.main.screen, self.select_image, (241, 474))


        # skins
        self.skin_perry_image = pygame.image.load('assets/sprites/skins/PlayerFly_Perry.png')
        self.skin_perry_image = pygame.transform.scale(self.skin_perry_image, (53 * 4, 57 * 4))

        self.skin_blue_image = pygame.image.load('assets/sprites/skins/PlayerFly_Blue.png')
        self.skin_blue_image = pygame.transform.scale(self.skin_blue_image, (53 * 2, 57 * 2))

        self.skin_green_image = pygame.image.load('assets/sprites/skins/PlayerFly_Green.png')
        self.skin_green_image = pygame.transform.scale(self.skin_green_image, (53 * 2, 57 * 2))

        self.skin_pink_image = pygame.image.load('assets/sprites/skins/PlayerFly_Pink.png')
        self.skin_pink_image = pygame.transform.scale(self.skin_pink_image, (53 * 2, 57 * 2))

        self.skin_orange_image = pygame.image.load('assets/sprites/skins/PlayerFly_Orange.png')
        self.skin_orange_image = pygame.transform.scale(self.skin_orange_image, (53 * 2, 57 * 2))

        self.skin_red_image = pygame.image.load('assets/sprites/skins/PlayerFly_Red.png')
        self.skin_red_image = pygame.transform.scale(self.skin_red_image, (53 * 2, 57 * 2))

        self.skin_yellow_image = pygame.image.load('assets/sprites/skins/PlayerFly_Yellow.png')
        self.skin_yellow_image = pygame.transform.scale(self.skin_yellow_image, (53 * 2, 57 * 2))


        self.skins_list = ['Blue', 'Green', 'Pink', 'Orange', 'Red', 'Yellow', 'Perry']
        self.skins_200 = ['Blue', 'Green', 'Pink', 'Orange', 'Red', 'Yellow']
        self.skins_1000 = ['Perry']
        self.skins_buttons = {
            'Blue': [self.button_buy_blue, self.button_select_blue],
            'Green': [self.button_buy_green, self.button_select_green],
            'Pink': [self.button_buy_pink, self.button_select_pink],
            'Orange': [self.button_buy_orange, self.button_select_orange],
            'Red': [self.button_buy_red, self.button_select_red],
            'Yellow': [self.button_buy_yellow, self.button_select_yellow],
            'Perry': [self.button_buy_perry, self.button_select_perry]
        }

    def update(self):
        self.check_events()

        # draw background
        self.menu.draw_background()
        self.transparency_surface.fill((0, 0, 0, 100))
        self.menu.main.screen.blit(self.transparency_surface, (0, 0))

        # draw text
        tools.draw_text(self.menu.main.screen, 'coins ' + str(self.menu.main.coins), 'center', 42, (640, 52))  # coins
        tools.draw_text(self.menu.main.screen, '200 c', 'center', 32, (840, 142), settings.YELLOW_COIN)  # perry price
        tools.draw_text(self.menu.main.screen, '1000 c', 'center', 32, (294, 182), settings.YELLOW_COIN)  # others price

        # update volume
        self.wrong_sound.set_volume(self.menu.main.global_volume * self.menu.main.sfx_volume * 0.3)
        self.right_sound.set_volume(self.menu.main.global_volume * self.menu.main.sfx_volume * 0.3)

        # self.draw_logo()
        self.draw_buttons()
        self.draw_skins()

        # tools.draw_text(self.menu.main.screen, 'Shop', 'center', 32, (settings.WIDTH / 2, 200))

        self.check_buttons_interactions()

    def check_events(self):
        for event in pygame.event.get():  # go through all events
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # inputs key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.current_menu = 'MainMenu'

    def draw_logo(self):
        self.menu.main.screen.blit(self.logo_image, (settings.WIDTH // 2 - self.logo_image.get_size()[0] // 2,
                                                     0))

    def draw_buttons(self):
        self.menu.draw_sound_music_buttons()
        self.button_back.draw()

        for skin_name in self.skins_list:
            # draw buy/select button
            if skin_name not in self.menu.main.skins_purchased:
                self.skins_buttons[skin_name][0].draw()
            else:
                self.skins_buttons[skin_name][1].draw()

    def check_buttons_interactions(self):
        self.menu.check_sound_music_buttons_interactions()
        if self.button_back.check_collision():
            self.menu.current_menu = 'MainMenu'

        for skin_name in self.skins_list:
            if skin_name not in self.menu.main.skins_purchased:
                # if buy
                collided = self.skins_buttons[skin_name][0].check_collision()
                if collided and skin_name in self.skins_200 and self.menu.main.coins >= 200:
                    self.menu.main.coins -= 200
                    self.menu.main.skins_purchased.append(skin_name)
                    self.save()
                elif collided and skin_name in self.skins_1000 and self.menu.main.coins >= 1000:
                    self.menu.main.coins -= 1000
                    self.menu.main.skins_purchased.append(skin_name)
                    self.save()
                elif collided:
                    self.wrong_sound.play()
            else:
                # if select
                if self.skins_buttons[skin_name][1].check_collision():
                    self.menu.main.player_skin = skin_name
                    self.right_sound.play()

    def draw_skins(self):
        self.menu.main.screen.blit(self.skin_perry_image, (182, 230))
        self.menu.main.screen.blit(self.skin_blue_image, (600, 185))
        self.menu.main.screen.blit(self.skin_green_image, (782, 185))
        self.menu.main.screen.blit(self.skin_pink_image, (964, 185))
        self.menu.main.screen.blit(self.skin_orange_image, (600, 420))
        self.menu.main.screen.blit(self.skin_red_image, (782, 420))
        self.menu.main.screen.blit(self.skin_yellow_image, (964, 420))

    def load(self):
        # coins
        try:
            with open('save/coins.txt', 'r+') as file:
                self.menu.main.coins = int(file.read())
        except:
            with open('save/coins.txt', 'w+') as file:
                file.write('0')

        # skins purchased
        try:
            with open('save/skins_purchased.txt', 'r+') as file:
                self.menu.main.skins_purchased = file.read().split()
        except:
            with open('save/skins_purchased.txt', 'w+') as file:
                file.write('Blue')

    def save(self):
        with open('save/coins.txt', 'w') as file:
            file.write(str(self.menu.main.coins))

        with open('save/skins_purchased.txt', 'w') as file:
            file.write(' '.join(self.menu.main.skins_purchased))

