from random import randint
from constants import *

class Wire:
    def __init__(self, field) -> None:
        self.x = 0
        self.y = 0
        self.rand_spawn(field)
        # self.spawn(field, x, y)
        self.output = [0, 0, 0, 0]
        self.port  = [1, 1, 1, 1]
        self.connect = [0, 0, 0, 0]
        self.on = False
    
    def spawn(self, field, x, y):
        self.x = x
        self.y = y
        if field[x][y] == None:
            field[x][y] = self

    def rand_spawn(self, field):
        self.x = randint(0, 20)
        self.y = randint(0, 20)
        if field[self.x][self.y] == None:
            field[self.x][self.y] = self
        else:
            self.rand_spawn(field=field)

    def update(self, field):
        power = 0
        for direc in range(DIREC):
            neighbour = None
            neighbourX = self.x + OFFSET[direc][0]
            neighbourY = self.y + OFFSET[direc][1]
            if (neighbourX < 0 or neighbourX >= TILE_WIDTH
                or neighbourY < 0 or neighbourY >= TILE_HEIGHT):
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
        x = TILE_SIDE * (3 + self.x)
        y = TILE_SIDE * self.y
        return (x, y)

    def render(self, screen):
        blit_coord = self.calc_pix_coord()
        debug_box = pygame.Rect(blit_coord, (TILE_SIDE, TILE_SIDE))
        if self.connect == [0, 0, 0, 0]:
            screen.blit(WIRE_LONE[self.on], blit_coord)
        wire_disp = WIRE_ON if self.on else WIRE_OFF
        for direc in range(DIREC):
            if self.connect[direc]:
                screen.blit(wire_disp[direc], blit_coord)
        # pygame.draw.rect(screen, GREEN, debug_box, width=1)
                