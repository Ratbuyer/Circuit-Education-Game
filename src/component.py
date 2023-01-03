from random import randint
from constants import *

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
        neighbours = self.get_neighbours(field=field)
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


    # return array of 4 neighbour object, value=None when no neighbour
    def get_neighbours(self, field):
        neighbours = []
        for direc in range(DIREC):
            neighbour = None
            neighbourX = self.x + OFFSET[direc][0]
            neighbourY = self.y + OFFSET[direc][1]
            if (neighbourX < BOUND[WEST] or 
                neighbourX > BOUND[EAST] or 
                neighbourY < BOUND[NORTH] or 
                neighbourY > BOUND[SOUTH]):
                neighbours.append(neighbour)
                continue
            neighbour = field[neighbourX][neighbourY]
            neighbours.append(neighbour)
        return neighbours

    def update(self, field):
        max_source = 0

        neighbours = self.get_neighbours(field=field)
        for direc in range(DIREC):
            neighbour = neighbours[direc]
            if neighbour and neighbour.output[OPPOSITE[direc]]:
                max_source = max(max_source, neighbour.power)

        if self.power < max_source:
            self.power = max_source - 1
        else:
            self.power = 0

        self.on = self.power > 0

    # return a coord pair coverted from TILE -> PIX
    def calc_pix_coord(self):
        x = int(TILE_SIDE * self.x)
        y = int(TILE_SIDE * self.y)
        return (x, y)

    # render item on given screen
    def render(self, screen):
        blit_coord = self.calc_pix_coord()
        screen.blit(self.img[self.on], blit_coord)

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
        self.power = SWITCH_POWER if self.on else 0

    def initialise(self, field):
        pass