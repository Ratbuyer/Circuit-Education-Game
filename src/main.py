import pygame
from constants import *
from component import *
from game_element import *

def initialise_game():
    WIN.fill(GREY)
    global game_state
    game_state = "gameon"
    global field
    field = [[None]*HEIGHT for i in range(WIDTH)]
    Switch(field=field, x=3, y=2, on=True)
    for i in range(800):
        Wire(field=field)
    init_items()
    global frame 
    frame = SelectFrame(x=3, y=3)
    

def init_items():
    for i in field:
        for elem in i:
            if elem:
                elem.initialise(field)

def update_components(mouse_pos):
    for i in field:
        for elem in i:
            if elem:
                elem.update(field)
    frame.update(mouse_pos, field)

def render_elements():
    WIN.fill(GREY)
    for i in field:
        for elem in i:
            if elem:
                elem.render(WIN)
    frame.render(WIN)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_press = pygame.mouse.get_pressed()
                frame.click(mouse_press, field)

        keys_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if game_state == "gameon":


            update_components(mouse_pos)

            render_elements()
        
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":

    main()