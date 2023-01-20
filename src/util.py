import pygame
import json
import sys
from constants import *

# return a coord pair coverted from TILE -> PIX
def calc_pix_coord(item):
    x = int(TILE_SIDE * item.x) + DISP_BOUND[WEST]
    y = int(TILE_SIDE * item.y) + DISP_BOUND[NORTH]
    return (x, y)
# return a coord pair coverted from PIX -> TILE
def calc_tile_coord(tup):
    x = tup[0]//TILE_SIDE - BOUND[WEST]
    y = tup[1]//TILE_SIDE - BOUND[NORTH]
    return (x, y)

def calc_angle(cur, maximum):
    ratio = cur/maximum
    return -360*ratio

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def out_bound_X(x):
    return (x < 0 or x > WIDTH - 1)

def out_bound_Y(y):
    return (y < 0 or y > HEIGHT - 1)
    
def out_bound(x, y):
    return (out_bound_X(x) or out_bound_Y(y))
    

# return array of 4 neighbour object, value=None when no neighbour
def get_neighbours(item, field):
    neighbours = []
    for direc in range(DIREC):
        neighbour = None
        neighbourX = item.x + OFFSET[direc][0]
        neighbourY = item.y + OFFSET[direc][1]
        if out_bound(neighbourX, neighbourY):
            neighbours.append(neighbour)
            continue
        neighbour = field[neighbourX][neighbourY]
        neighbours.append(neighbour)
    return neighbours

def get_power_supply(item, field):
    neighbours = get_neighbours(item, field)
    supply = [0]*4
    for direc in range(DIREC):
        neighbour = neighbours[direc]
        if (neighbour and 
            neighbour.output[OPPOSITE[direc]]):
            supply[direc] = neighbour.power
        else:
            supply[direc] = 0
    return supply

def jsonify(item):
    if item:
        dic = {
            'class': type(item).__name__,
            'x':item.x,
            'y':item.y,
            'on':item.on
        }
    else:
        return None
    return [json.dumps(dic)]

def on_inventory(pos):
    x, y = pos[0], pos[1]
    return not (x < INV_BOUND[WEST] or 
                x > INV_BOUND[EAST] or
                y < INV_BOUND[NORTH] or 
                y > INV_BOUND[SOUTH])

def on_field(pos):
    x, y = pos[0], pos[1]
    return not (x < DISP_BOUND[WEST] or 
                x > DISP_BOUND[EAST] or
                y < DISP_BOUND[NORTH] or 
                y > DISP_BOUND[SOUTH])

def kill():
    pygame.quit()
    exit()