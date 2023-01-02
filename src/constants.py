import pygame

TILE_SIDE = 40
WIDTH, HEIGHT = 1920, 1080
TILE_WIDTH = int(WIDTH/TILE_SIDE - 3)#45
TILE_HEIGHT = int(HEIGHT/TILE_SIDE)#27

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circuit Education")

# color constants
WHITE = (255, 255, 255)
GREY  = (105, 105, 105)
GREEN = (0, 255, 0)

FPS = 60

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

# game elements
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
