import pygame
from constants import *

# return a coord pair coverted from TILE -> PIX
def calc_pix_coord(item):
    x = int(TILE_SIDE * item.x)
    y = int(TILE_SIDE * item.y)
    return (x, y)

def calc_tile_coord(tup):
    x = tup[0]//TILE_SIDE
    y = tup[1]//TILE_SIDE
    return (x, y)