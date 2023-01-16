import pygame
import component
from constants import *
from component import *
from util import *
import inspect

COMP_CLASSES = [
    obj for name, obj in inspect.getmembers(component)
    if inspect.isclass(obj)
]
class SelectFrame:
    def __init__(self, x=None, y=None) -> None:
        self.x = x
        self.y = y
        self.hide = True
        self.img = SELECT_FRAME

    def render(self, screen):
        if not self.hide:
            blit_coord = calc_pix_coord(self)
            screen.blit(self.img, blit_coord)

    def update(self, mouse_pos):
        tile_coord = calc_tile_coord(mouse_pos)
        self.hide = out_bound(tile_coord[0], tile_coord[1])
        if not out_bound_X(tile_coord[0]):
            self.x = tile_coord[0]
        if not out_bound_Y(tile_coord[1]):
            self.y = tile_coord[1]
        
    
    def click(self, mouse_press, field):
        if out_bound(self.x, self.y) or self.hide:
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

class Inventory:
    def __init__(self) -> None:
        self.x = 5
        self.y = BOUND[SOUTH]
        self.comps = COMP_CLASSES
        self.disp_comps = self.comps[:9]
        self.choice = 0

    def update(self, mouse_pos):
        pass

    def render(self, screen):
        blit_coord = [i for i in calc_pix_coord(self)]
        blit_coord[1] -= TILE_SIDE
        screen.blit(INV_DEAC_BASE, blit_coord)
        screen.blit(INV_AC_BASE, self.calc_hover_pos())
        screen.blit(INV_LABEL, blit_coord)

    def calc_hover_pos(self):
        blit_coord = [i for i in calc_pix_coord(self)]
        blit_coord[0] += INV_AC_BASE.get_width() * self.choice
        blit_coord[1] -= TILE_SIDE
        return blit_coord

    def select_tool(self, index):
        self.choice = index