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
        self.x = tile_coord[0]
        self.y = tile_coord[1]
        
    
    def click(self, mouse_press, field):
        if mouse_press[0] and field[self.x][self.y]:
            field[self.x][self.y].interact()