from random import randint
from constants import *
from util import *

class Wire:
    def __init__(self, field=None, x=None, y=None) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output  = [1, 1, 1, 1]
        self.port    = [1, 1, 1, 1]
        self.connect = [0, 0, 0, 0]
        self.power = 0
        self.on = False
        self.img = []

    # place item in field at (x, y)
    def place(self, field, x, y):
        self.x = x
        self.y = y
        if field[x][y] == None:
            field[x][y] = self
        else:
            print("Failed to place component")

    # randomly place item in field,
    # if tile occupied recursively re-place, until depth=attempt
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

    def initialise(self, field):
        neighbours = get_neighbours(item=self, field=field)
        for direc in range(DIREC):
            neighbour = neighbours[direc]
            if neighbour:
                neighbour_open = neighbour.port[OPPOSITE[direc]]
                self.connect[direc] = neighbour_open
            else:
                self.connect[direc] = 0
        self.set_img()

    def set_img(self):
        blit_origin = (0, 0)
        if self.connect == [0, 0, 0, 0]:
            self.img = WIRE_LONE
        else:
            off_img, on_img = VOID.copy(), VOID.copy()
            for direc in range(DIREC):
                if self.connect[direc]:
                    off_img.blit(WIRE_OFF[direc], blit_origin)
                    on_img.blit(WIRE_ON[direc], blit_origin)
            self.img = [off_img, on_img]


    def update(self, field):
        max_source = 0

        neighbours = get_neighbours(item=self, field=field)
        for direc in range(DIREC):
            neighbour = neighbours[direc]
            if neighbour and neighbour.output[OPPOSITE[direc]]:
                max_source = max(max_source, neighbour.power)

        if self.power < max_source:
            self.power = max_source - 1
        else:
            self.power = 0

        self.on = self.power > 0


    # render item on given screen
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(self.img[self.on], blit_coord)

        # # box boundary display
        # debug_box = pygame.Rect(blit_coord, (TILE_SIDE, TILE_SIDE))
        # pygame.draw.rect(screen, GREEN, debug_box, width=1)
    
    def interact(self):
        pass


class Switch:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [1, 1, 1, 1]
        self.port  = [1, 1, 1, 1]
        self.on = on
        self.power = SWITCH_POWER if self.on else 0

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
        
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(WIRE_LONE[self.on], blit_coord)
        screen.blit(SWITCH_COVER, blit_coord)

    def interact(self):
        self.on = not self.on
        self.power = SWITCH_POWER if self.on else 0

    def initialise(self, field):
        pass


class AndGate:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [1, 0, 0, 0]
        self.port  = [1, 1, 0, 1]
        self.on = on
        self.power = 0

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
        neighbours = get_neighbours(self, field)
        if (neighbours[WEST] and neighbours[WEST].output[OPPOSITE[WEST]] and
            neighbours[EAST] and neighbours[EAST].output[OPPOSITE[EAST]] and
            neighbours[WEST].power > 0  and neighbours[EAST].power > 0):
            self.power = SWITCH_POWER
        else:
            self.power = 0
    
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(AND_IMG, blit_coord)
        
    def initialise(self, field):
        pass

class OrGate:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [1, 0, 0, 0]
        self.port  = [1, 1, 0, 1]
        self.on = on
        self.power = 0

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
        # neighbours = get_neighbours(self, field)
        supplies = get_power_supply(self, field)
        if (supplies[WEST] or supplies[EAST]):
            self.power = SWITCH_POWER
        else:
            self.power = 0
    
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(OR_IMG, blit_coord)
        
    def initialise(self, field):
        pass

class NotGate:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if not x or not y:
            self.rand_place(field=field)
        else:
            self.place(field=field, x=x, y=y)
        self.output = [1, 0, 0, 0]
        self.port  = [1, 0, 1, 0]
        self.on = on
        self.power = 0

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
        # neighbours = get_neighbours(self, field)
        supplies = get_power_supply(self, field)
        if supplies[SOUTH]:
            self.power = 0
        else:
            self.power = SWITCH_POWER
    
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(NOT_IMG, blit_coord)
        
    def initialise(self, field):
        pass
                
