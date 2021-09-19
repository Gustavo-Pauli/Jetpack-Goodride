# global constants

import pygame

# program settings
TITLE = 'Jetpack Goodride'
ICON_LOC = 'assets/sprites/icon.png'
DEFAULT_FONT_LOC = 'assets/fonts/New Athletic M54.ttf'
HIGH_SCORE_LOC = 'save/highscore.txt'
WIDTH = 1280
HEIGHT = 720
FPS = 300

# player settings
DEFAULT_X_VELOCITY = 480
MAX_X_VELOCITY = 690
GRAVITY = 1.7

# scenario settings
FIRST_OBSTACLE_OFFSET = 1920
OBSTACLE_OFFSET = 680  # 520-860
MIN_OBSTACLE_OFFSET = 520
MAX_OBSTACLE_OFFSET = 860
MIN_HEIGHT = 645
MAX_HEIGHT = 80
# OBSTACLE_Y_POSITIONS = [190, 278, 365, 453, 540]

# colors
BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
YELLOW = pygame.color.Color(255, 255, 0)
YELLOW_COIN = pygame.color.Color(255, 189, 28)

# audio
# MUSIC_LOC_LIST = []

# DEBUG
DEBUG = False
DEBUG_HIT_BOXES = True
DEBUG_SCREEN_SIZE_BOX = True
