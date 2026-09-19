import pygame
import math
import random
from pygame.math import Vector2

SCALE_MULTIPLIER = 8
TILE_SIZE = 8
WINDOW_WIDTH = 120
WINDOW_HEIGHT = 90
FPS = 60

BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
CYAN = (0,255,255)
RED = (255,0,0)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)

GRAY = (127,127,127)
# add all colors

LEVEL_ORDER = [
    "tutorial_zero",
    "tutorial_one",
    "tutorial_two",
    "level_zero",
    "level_one",
    "level_two",
    "level_three"
    "level_four",
    "level_five",
    "level_six",
    "level_seven",
    "level_eight"
]
