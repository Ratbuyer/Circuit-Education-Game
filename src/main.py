import pygame
from constants import *
from component import *


def draw():

    WIN.fill(WHITE)
    # WIN.blit(AND, (500, 500))
    pygame.display.update()
    return
    
def empty_field():
    f = []
    for i in range(TILE_WIDTH):
        f.append([None]*TILE_HEIGHT)
    return f

def initialise_game():
    WIN.fill(GREY)
    global game_state
    game_state = "gameon"
    global field
    field = empty_field()
    for i in range(441):
        Wire(field=field)

def update_elements():
    for i in field:
        for elem in i:
            if elem:
                elem.update(field)

def render_elements():
    for i in field:
        for elem in i:
            if elem:
                elem.render(WIN)

def main():
    initialise_game()
    global game_state, field
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_SPACE and game_state in ["gameset", "idle"]:
                    game_state = "gameon"
                elif event.key == pygame.K_k:
                    initialise_game()
                else:
                    pass
        keys_pressed = pygame.key.get_pressed()
        if game_state == "gameon":


            update_elements()

            render_elements()
        
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":

    main()