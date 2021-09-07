# common functions in different game states

import pygame
import scripts.settings as settings


def draw_text(screen_surface, text, align, size, pos, color=settings.WHITE, background=None):
    font = pygame.font.Font(settings.DEFAULT_FONT_LOC, size)
    text_surface = font.render(text, True, color, background)
    text_rect = text_surface.get_rect()
    if align == 'center':
        text_rect.center = pos
    elif align == 'left':
        text_rect.bottomleft = pos
    elif align == 'right':
        text_rect.bottomright = pos
    else:
        raise ValueError('Align option not valid')
    screen_surface.blit(text_surface, text_rect)


class Button:
    def __init__(self, screen, image, pos, align='topleft', scale=1.0):
        self.clicked = False
        self.screen = screen
        self.image = pygame.transform.smoothscale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        if align == 'topleft':
            self.rect.topleft = (pos[0], pos[1])
        elif align == 'center':
            self.rect.center = (pos[0], pos[1])
        elif align == 'bottomright':
            self.rect.bottomright = (pos[0], pos[1])
        else:
            raise ValueError('Align option not valid')

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_collision(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        # check if clicked
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed(3)[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed(3)[0]:
            self.clicked = False

        return action
