import pygame
from pygame.image import load as limg
from pygame.locals import *

def scale(img, factor):
    size = [i*factor for i in img.get_size()]
    return pygame.transform.scale(img, size)

# directional constant
NORTH, WEST, SOUTH, EAST  = 0, 1, 2, 3
OPPOSITE = [SOUTH, EAST, NORTH, WEST]
OFFSET = [
    [0, -1],
    [-1, 0],
    [0, 1],
    [1, 0]
]
DIREC = 4

# dimension constant
TILE_SIDE = 40
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
DISP_BOUND = [
    TILE_SIDE * 2, # North padding
    TILE_SIDE * 3, # West padding
    SCREEN_HEIGHT - (TILE_SIDE * 4), # South padding
    SCREEN_WIDTH - (TILE_SIDE * 3)  # East padding
]
BOUND = [int(d/TILE_SIDE) for d in DISP_BOUND]

WIDTH = BOUND[EAST] - BOUND[WEST]
HEIGHT = BOUND[SOUTH] - BOUND[NORTH]

# game ini & constant
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Circuit Education")
FPS = 60

# color constants
WHITE = (255, 255, 255)
GREY  = (105, 105, 105)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# game asset loading
AND_IMG = limg("./asset/gates/and.png").convert_alpha()
OR_IMG = limg("./asset/gates/or.png").convert_alpha()
NOT_IMG = limg("./asset/gates/not.png").convert_alpha()

TIMER_BASE = limg("./asset/timer/timer_base.png").convert_alpha()
TIMER_HAND = limg("./asset/timer/timer_hand.png").convert_alpha()

WIRE_LONE = [
    limg("./asset/wire/wire_lone_off.png").convert_alpha(),
    limg("./asset/wire/wire_lone_on.png").convert_alpha()
]

WIRE_ON_IMG = limg("./asset/wire/wire_on.png").convert_alpha()
WIRE_ON = [
    pygame.transform.rotate(WIRE_ON_IMG, 0),
    pygame.transform.rotate(WIRE_ON_IMG, 90),
    pygame.transform.rotate(WIRE_ON_IMG, 180),
    pygame.transform.rotate(WIRE_ON_IMG, 270)
]

WIRE_OFF_IMG = limg("./asset/wire/wire_off.png").convert_alpha()
WIRE_OFF = [
    pygame.transform.rotate(WIRE_OFF_IMG, 0),
    pygame.transform.rotate(WIRE_OFF_IMG, 90),
    pygame.transform.rotate(WIRE_OFF_IMG, 180),
    pygame.transform.rotate(WIRE_OFF_IMG, 270)
]
SWITCH_COVER = limg("./asset/switch_cover.png").convert_alpha()
VOID = limg("./asset/void.png").convert_alpha()

SELECT_FRAME = limg("./asset/select_frame.png").convert_alpha()

INV_LABEL = scale(limg("./asset/inventory/inv_label.png").convert_alpha(), 2)
INV_DEAC_BASE = scale(limg("./asset/inventory/inv_deactive_base.png").convert_alpha(), 2)
INV_AC_BASE = limg("./asset/inventory/inv_active_base.png").convert_alpha()
INV_KEYS = {
    K_1: 0, K_2: 1, K_3: 2, K_4: 3,
    K_q: 4, K_w: 5, K_e: 6, K_r: 7,
    K_a: 8, K_s: 9, K_d: 10, K_f: 11,
    K_z: 12, K_x: 13, K_c: 14, K_v: 15
}
INV_WIDTH = INV_LABEL.get_width()
INV_HEIGHT = INV_LABEL.get_height()
INV_BOUND = [
    DISP_BOUND[SOUTH] + TILE_SIDE,
    9 * TILE_SIDE,
    DISP_BOUND[SOUTH] + TILE_SIDE + INV_HEIGHT,
    9 * TILE_SIDE + INV_WIDTH
]

MLEFT = 0
MRIGHT = 2

MAX_ATTEMPT = 300
SWITCH_POWER = 50

LEVEL_PATH = "./levels/"


