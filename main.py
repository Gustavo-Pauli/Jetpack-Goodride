# Main program loop

import pygame
import scripts.game as game
import scripts.menu as menu
import scripts.settings as settings


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        pygame.display.set_icon(pygame.image.load(settings.ICON_LOC))
        self.clock = pygame.time.Clock()
        self.dt = None

        # audio
        self.global_volume = 0.56
        self.music_volume = 0.48
        self.sfx_volume = 1
        self.last_global_volume = self.global_volume
        self.last_music_volume = self.music_volume
        self.sound_on = True
        self.music_on = True

        self.coins = 0
        self.player_skin = 'Blue'
        self.skins_purchased = ['Blue']

        # game states TODO maybe change to stack list
        self.running = True  # running the program
        self.playing = False  # in gameplay part
        self.in_menu = True
        self.game = None
        self.menu = menu.Menu(self)

        self.already_instantiated_game = False

    def main_loop(self):
        while self.in_menu:
            self.update_dt()
            self.menu.update_menu(self)

        while self.playing:  # gameplay loop
            self.update_dt()
            self.game.update_game(self)

    def update_dt(self):
        self.dt = self.clock.tick(settings.FPS) / 1000  # delta time in seconds | cap fps


if __name__ == '__main__':
    main = Main()
    while main.running:
        main.main_loop()
