# Main program loop

import pygame
import scripts.game as game
import scripts.menu as menu
import scripts.settings as settings


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption('Jetpack Goodride')
        pygame.display.set_icon(pygame.image.load(settings.ICON_LOC))
        self.clock = pygame.time.Clock()
        self.dt = None

        # game states TODO maybe change to stack list
        self.running = True  # running the program
        self.playing = False  # in gameplay part
        self.in_menu = True
        self.game = game.Game(self)  # TODO remove this and put on the button on click play game
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
        self.dt = self.clock.tick(settings.FPS) / 1000 * 1.2  # delta time in seconds | cap fps


# dont execute code when importing
if __name__ == '__main__':
    main = Main()
    while main.running:
        main.main_loop()
