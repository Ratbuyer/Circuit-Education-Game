import pygame
from constants import *
from component import *
from util import *

class SelectFrame:
    def __init__(self, x=None, y=None) -> None:
        self.x = x
        self.y = y
        self.img = SELECT_FRAME

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(self.img, blit_coord)

    def update(self, mouse_pos, field):
        tile_coord = calc_tile_coord(mouse_pos)
        if not out_bound_X(tile_coord[0]):
            self.x = tile_coord[0]
        if not out_bound_Y(tile_coord[1]):
            self.y = tile_coord[1]
        
    
    def click(self, mouse_press, field):
        if out_bound(self.x, self.y):
            return
        if mouse_press[0] and field[self.x][self.y]:
            field[self.x][self.y].interact()
        elif mouse_press[2] and field[self.x][self.y]==None:
            Wire(field=field, x=self.x, y=self.y)
            item = field[self.x][self.y]
            if not item:
                raise ValueError
            item.initialise(field)
            neighbours = get_neighbours(item, field)
            for i in neighbours:
                if i:
                    i.initialise(field)
        elif (mouse_press[2] and 
            type(field[self.x][self.y]).__name__=="Wire"):
            item = field[self.x][self.y]
            neighbours = get_neighbours(item, field)
            field[self.x][self.y] = None
            for i in neighbours:
                if i:
                    i.initialise(field)