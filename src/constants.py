import pygame

# dimension constant
TILE_SIDE = 40
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
WIDTH = int(SCREEN_WIDTH/TILE_SIDE)
HEIGHT = int(SCREEN_HEIGHT/TILE_SIDE)

DISP_BOUND = [
    TILE_SIDE * 2, # North padding
    TILE_SIDE * 3, # West padding
    SCREEN_HEIGHT - (TILE_SIDE * 4), # South padding
    SCREEN_WIDTH - (TILE_SIDE * 3)  # East padding
]
BOUND = [int(d/TILE_SIDE) for d in DISP_BOUND]

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

# game asset loading
AND_IMG = pygame.image.load("./asset/and.png").convert_alpha()

WIRE_LONE = [
    pygame.image.load("./asset/wire/wire_lone_off.png").convert_alpha(),
    pygame.image.load("./asset/wire/wire_lone_on.png").convert_alpha()
]

WIRE_ON_IMG = pygame.image.load("./asset/wire/wire_on.png").convert_alpha()
WIRE_ON = [
    pygame.transform.rotate(WIRE_ON_IMG, 0),
    pygame.transform.rotate(WIRE_ON_IMG, 90),
    pygame.transform.rotate(WIRE_ON_IMG, 180),
    pygame.transform.rotate(WIRE_ON_IMG, 270)
]

WIRE_OFF_IMG = pygame.image.load("./asset/wire/wire_off.png").convert_alpha()
WIRE_OFF = [
    pygame.transform.rotate(WIRE_OFF_IMG, 0),
    pygame.transform.rotate(WIRE_OFF_IMG, 90),
    pygame.transform.rotate(WIRE_OFF_IMG, 180),
    pygame.transform.rotate(WIRE_OFF_IMG, 270)
]
SWITCH_COVER = pygame.image.load("./asset/switch_cover.png").convert_alpha()

MAX_ATTEMPT = 300

