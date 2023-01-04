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

# return array of 4 neighbour object, value=None when no neighbour
def get_neighbours(item, field):
    neighbours = []
    for direc in range(DIREC):
        neighbour = None
        neighbourX = item.x + OFFSET[direc][0]
        neighbourY = item.y + OFFSET[direc][1]
        if (neighbourX < BOUND[WEST] or 
            neighbourX > BOUND[EAST] or 
            neighbourY < BOUND[NORTH] or 
            neighbourY > BOUND[SOUTH]):
            neighbours.append(neighbour)
            continue
        neighbour = field[neighbourX][neighbourY]
        neighbours.append(neighbour)
    return neighbours