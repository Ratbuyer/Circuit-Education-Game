import pygame
import component
from constants import *
from component import *
from util import *
import inspect

# COMP_CLASSES = [
#     obj for name, obj in inspect.getmembers(component)
#     if inspect.isclass(obj)
# ]
COMP_CLASSES = sorted([
    cls for name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass) 
    if issubclass(cls, Component) and cls not in [Component, Gates]
], key=lambda x:x.__name__)

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
        
    def click(self, mouse_press, field, tool):
        if out_bound(self.x, self.y) or self.hide:
            return
        if mouse_press[MLEFT] and field[self.x][self.y]:
            field[self.x][self.y].interact()
        elif mouse_press[MRIGHT] and field[self.x][self.y]==None:
            tool(field=field, x=self.x, y=self.y)
            item = field[self.x][self.y]
            if not item:
                raise ValueError
            item.initialise(field)
            neighbours = get_neighbours(item, field)
            for i in neighbours:
                if i:
                    i.initialise(field)
        elif (mouse_press[2] and type(field[self.x][self.y]).__name__):
            item = field[self.x][self.y]
            neighbours = get_neighbours(item, field)
            field[self.x][self.y] = None
            for i in neighbours:
                if i:
                    i.initialise(field)

class Inventory:
    def __init__(self) -> None:
        self.x = INV_BOUND[WEST]
        self.y = INV_BOUND[NORTH]
        self.comps = COMP_CLASSES
        self.disp_comps = self.comps
        self.comp_count = len(self.disp_comps)
        self.choice = 0
        self.tool = self.comps[self.choice]
        self.hover = -1
        # print([i.__name__ for i in self.disp_comps])

    def update(self, mouse_pos):
        if on_inventory(mouse_pos):
            self.hover = self.get_mouse_idx(mouse_pos)
        else:
            self.hover = -1
        pass

    def render(self, screen):
        blit_coord = (self.x, self.y)
        for i, comp in enumerate(self.disp_comps):
            img = scale(INV_THUMB[comp.__name__], 2)
            coord = (blit_coord[0] + i*INV_HEIGHT, blit_coord[1])
            screen.blit(img, coord)
        if self.hover != -1:
            screen.blit(INV_HOVER_GLARE, self.calc_hover_pos(self.hover))
        screen.blit(INV_DEAC_BASE, blit_coord)
        screen.blit(INV_AC_BASE, self.calc_hover_pos(self.choice))
        screen.blit(INV_LABEL, blit_coord)

    def calc_hover_pos(self, idx):
        blit_coord = [self.x, self.y]
        blit_coord[0] += INV_AC_BASE.get_width() * idx
        return blit_coord

    def select_tool(self, index):
        if index < self.comp_count:
            self.choice = index
            self.tool = self.comps[index]
    
    def get_mouse_idx(self, mouse_pos):
        x = mouse_pos[0] - INV_BOUND[WEST]
        return x//INV_HEIGHT

    def click(self, mouse_press, mouse_pos):
        if not on_inventory(mouse_pos):
            return
        if mouse_press[MLEFT]:
            idx = self.get_mouse_idx(mouse_pos)
            self.select_tool(idx)

    def render_box(self, screen):
        blit_coord = (self.x, self.y)
        # box boundary display
        debug_box = pygame.Rect(blit_coord, (INV_WIDTH, INV_HEIGHT))
        pygame.draw.rect(screen, GREEN, debug_box, width=1)

class Button:
    def __init__(self, coord, text=BUTTON_FONT, onClick=NOOP) -> None:
        self.onClick = onClick
        self.x, self.y = coord
        self.text = BUTTON_FONT.render(text, True, CYAN)
        self.hover = False
    
    def update(self, mousepos):
        pass
    
    def calc_text_coord(self):
        x = self.x + BUTTON_FRAME.get_width()//2 - self.text.get_width()//2 
        y = self.y + BUTTON_FRAME.get_height()//2 - self.text.get_height()//2 
        return (x, y)

    def render(self, screen):
        screen.blit(self.text, self.calc_text_coord())
        screen.blit(BUTTON_FRAME, (self.x, self.y))
    
