import pygame
from constants import *
from component import *

def initialise_game():
    WIN.fill(GREY)
    global game_state
    game_state = "gameon"
    global field
    field = [[None]*HEIGHT for i in range(WIDTH)]
    Switch(field=field, x=10, y=10, on=True)
    for i in range(800):
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
                elif event.key == pygame.K_j:
                    field[10][10].interact()
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