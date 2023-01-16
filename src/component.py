from random import randint
from constants import *
from util import *

# return class reference of classname(str)


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


class Component:
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        if x == None or y == None:
            self.rand_place(field=field)
        else:
            if not out_bound(x, y):
                self.place(field=field, x=x, y=y)
            else:
                pass
        self.on = on
        self.power = 0

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
        self.x = randint(0, WIDTH - 1)
        self.y = randint(0, HEIGHT - 1)
        if field[self.x][self.y] == None:
            field[self.x][self.y] = self
        else:
            if attempt >= 0:
                self.rand_place(field=field, attempt=attempt-1)
            else:
                print(f"rand-place failed after {MAX_ATTEMPT} attempt")

    def initialise(self, field):
        pass

    def interact(self):
        pass

    def update(self, field):
        pass

    def render(self, screen):
        pass

    def render_box(self, screen):
        blit_coord = calc_pix_coord(self)
        # box boundary display
        debug_box = pygame.Rect(blit_coord, (TILE_SIDE, TILE_SIDE))
        pygame.draw.rect(screen, GREEN, debug_box, width=1)


class Wire(Component):
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        super().__init__(field=field, x=x, y=y, on=on)
        self.output = [1, 1, 1, 1]
        self.port = [1, 1, 1, 1]
        self.connect = [0, 0, 0, 0]
        self.img = []


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


class Switch(Component):
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        super().__init__(field, x, y, on)
        self.output = [1, 1, 1, 1]
        self.port = [1, 1, 1, 1]
        self.power = SWITCH_POWER if self.on else 0

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(WIRE_LONE[self.on], blit_coord)
        screen.blit(SWITCH_COVER, blit_coord)

    def interact(self):
        self.on = not self.on
        self.power = SWITCH_POWER if self.on else 0


class AndGate(Component):
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        super().__init__(field, x, y, on)
        self.output = [1, 0, 0, 0]
        self.port = [1, 1, 0, 1]

    def update(self, field):

        supplies = get_power_supply(self, field)
        if (supplies[WEST] and supplies[EAST]):
            self.power = SWITCH_POWER
        else:
            self.power = 0

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(AND_IMG, blit_coord)


class NandGate(AndGate):

    def update(self, field):
        supplies = get_power_supply(self, field)
        if (supplies[WEST] and supplies[EAST]):
            self.power = 0
        else:
            self.power = SWITCH_POWER

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(NAND_IMG, blit_coord)
        pass


class OrGate(Component):
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        super().__init__(field, x, y, on)
        self.output = [1, 0, 0, 0]
        self.port = [1, 1, 0, 1]

    def update(self, field):
        supplies = get_power_supply(self, field)
        if (supplies[WEST] or supplies[EAST]):
            self.power = SWITCH_POWER
        else:
            self.power = 0

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(OR_IMG, blit_coord)


class NorGate(OrGate):

    def update(self, field):
        supplies = get_power_supply(self, field)
        if (supplies[WEST] or supplies[EAST]):
            self.power = 0
        else:
            self.power = SWITCH_POWER

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(NOR_IMG, blit_coord)
        pass


class XorGate(OrGate):

    def update(self, field):
        supplies = get_power_supply(self, field)
        
        if supplies[WEST] and supplies[EAST]:
            self.power = 0
        elif (not supplies[WEST]) and (not supplies[EAST]):
            self.power = 0
        elif supplies[WEST] and (not supplies[EAST]):
            self.power = SWITCH_POWER
        elif supplies[EAST] and (not supplies[WEST]):
            self.power = SWITCH_POWER


    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(XOR_IMG, blit_coord)
        pass


class XnorGate(XorGate):

    def update(self, field):
        super().update(field)
        self.power = 0 if self.power else SWITCH_POWER
    
    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(XNOR_IMG, blit_coord)
        pass


class NotGate(Component):
    def __init__(self, field=None, x=None, y=None, on=False) -> None:
        super().__init__(field, x, y, on)
        self.output = [1, 0, 0, 0]
        self.port = [1, 0, 1, 0]

    def update(self, field):
        supplies = get_power_supply(self, field)
        if supplies[SOUTH]:
            self.power = 0
        else:
            self.power = SWITCH_POWER

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        screen.blit(NOT_IMG, blit_coord)


class Timer(Component):
    def __init__(self, field=None, x=None, y=None, on=False, maxsec=2) -> None:
        super().__init__(field, x, y, on)
        self.output = [1, 1, 1, 1]
        self.port = [1, 1, 1, 1]
        self.tick = 0
        self.maxtick = maxsec * FPS
        self.eith_tick = self.maxtick/8

    def update(self, field):
        if self.tick >= 0 and self.tick < self.maxtick:
            self.tick += 1
        else:
            self.tick = 0
            self.power = 0 if self.power else SWITCH_POWER

    def render(self, screen):
        blit_coord = calc_pix_coord(self)
        rot_angle = calc_angle(self.tick, self.maxtick)
        hand_img = rot_center(TIMER_HAND, rot_angle)
        screen.blit(TIMER_BASE, blit_coord)
        screen.blit(hand_img, blit_coord)
