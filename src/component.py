from random import randint
from constants import *

class Wire:
    def __init__(self, field=None, x=None, y=None) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [0, 0, 0, 0]
        self.port  = [1, 1, 1, 1]
        self.connect = [0, 0, 0, 0]
        self.source = []
        self.on = False
    
    def place(self, field, x, y):
        self.x = x
        self.y = y
        if field[x][y] == None:
            field[x][y] = self
        else:
            print("Failed to place component")

    def rand_place(self, field=None, attempt=MAX_ATTEMPT):
        self.x = randint(BOUND[WEST], BOUND[EAST])
        self.y = randint(BOUND[NORTH], BOUND[SOUTH])
        if field[self.x][self.y] == None:
            field[self.x][self.y] = self
        else:
            if attempt >= 0:
                self.rand_place(field=field, attempt=attempt-1)
            else:
                print(f"rand-place failed after {MAX_ATTEMPT} attempt")

    def update(self, field):
        power = 0
        for direc in range(DIREC):
            neighbour = None
            neighbourX = self.x + OFFSET[direc][0]
            neighbourY = self.y + OFFSET[direc][1]
            if (neighbourX < BOUND[WEST] or 
                neighbourX > BOUND[EAST] or 
                neighbourY < BOUND[NORTH] or 
                neighbourY > BOUND[SOUTH]):
                continue
            neighbour = field[neighbourX][neighbourY]
            if neighbour:
                neighbour_open = neighbour.port[OPPOSITE[direc]]
                self.connect[direc] = neighbour_open
                if neighbour.output[OPPOSITE[direc]]:
                    power = 1
                    self.on = True
            else:
                self.connect[direc] = 0
        self.output = [power]*4

    def calc_pix_coord(self):
        x = int(TILE_SIDE * self.x)
        y = int(TILE_SIDE * self.y)
        return (x, y)

    def render(self, screen):
        blit_coord = self.calc_pix_coord()
        if self.connect == [0, 0, 0, 0]:
            screen.blit(WIRE_LONE[self.on], blit_coord)
        wire_disp = WIRE_ON if self.on else WIRE_OFF
        for direc in range(DIREC):
            if self.connect[direc]:
                screen.blit(wire_disp[direc], blit_coord)
        # # box boundary display
        # debug_box = pygame.Rect(blit_coord, (TILE_SIDE, TILE_SIDE))
        # pygame.draw.rect(screen, GREEN, debug_box, width=1)

class Switch:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [1, 1, 1, 1]
        self.port  = [1, 1, 1, 1]
        self.on = on

    def place(self, field, x, y):
        self.x = x
        self.y = y
        if field[x][y] == None:
            field[x][y] = self
        else:
            print("Failed to place component")

    def rand_place(self, field=None, attempt=MAX_ATTEMPT):
        self.x = randint(BOUND[WEST], BOUND[EAST])
        self.y = randint(BOUND[NORTH], BOUND[SOUTH])
        if field[self.x][self.y] == None:
            field[self.x][self.y] = self
        else:
            if attempt >= 0:
                self.rand_place(field=field, attempt=attempt-1)
            else:
                print(f"rand-place failed after {MAX_ATTEMPT} attempt")
    
    def update(self, field):
        pass
    

    def calc_pix_coord(self):
        x = int(TILE_SIDE * self.x)
        y = int(TILE_SIDE * self.y)
        return (x, y)
        
    def render(self, screen):
        blit_coord = self.calc_pix_coord()
        screen.blit(WIRE_LONE[self.on], blit_coord)
        screen.blit(SWITCH_COVER, blit_coord)

    def interact(self):
        self.on = not self.on