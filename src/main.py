import pygame
import csv
from constants import *
from component import *
from game_element import *

def save_level():
    level = []
    for i in field:
        for j in i:
            if j:
                level.append(jsonify(j))
    with open(LEVEL_PATH+'lv1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(level)

def load_level():
    global field
    field = [[None]*HEIGHT for i in range(WIDTH)]
    level = []
    with open(LEVEL_PATH+'lv1.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            level.append(row)
    level = [i[0] for i in level]
    level = [json.loads(i) for i in level]
    for comp in level:
        classHandle = str_to_class(comp['class'])
        x = int(comp['x'])
        y = int(comp['y'])
        on = comp['on']
        classHandle(field=field, x=x, y=y, on=on)
    init_items()
    

def initialise_game():
    WIN.fill(GREY)
    global game_state
    game_state = "gameon"
    global field
    field = [[None]*HEIGHT for i in range(WIDTH)]
    for i in range(500):
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
                # elem.render_box(WIN) #debug box renderer
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
                elif event.key == pygame.K_s:
                    save_level()
                elif event.key == pygame.K_l:
                    load_level()
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
            clock.tick(FPS)

if __name__ == "__main__":

    main()