import pygame
import math
import random
from pygame.math import Vector2

SCALE_MULTIPLIER = 8
TILE_SIZE = 8
NATIVE_WIDTH = 120
NATIVE_HEIGHT = 90
WINDOW_WIDTH = NATIVE_WIDTH * SCALE_MULTIPLIER
WINDOW_HEIGHT = NATIVE_HEIGHT * SCALE_MULTIPLIER
FPS = 60

# --- STRICT 27-COLOR PALETTE (RGB 0, 127, 255 only) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
DARK_RED = (127, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (127, 127, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 127, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 127)
MAGENTA = (255, 0, 255)
# ... other combinations from the 27 available colors as needed.
