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
    WIN.fill(BLACK)
    global game_state
    game_state = "gameon"
    global field
    field = [[None]*HEIGHT for i in range(WIDTH)]
    for i in range(500):
        Wire(field=field)
    init_items()

    global frame 
    frame = SelectFrame(x=3, y=3)
    global inventory
    inventory = Inventory()
    

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
    frame.update(mouse_pos)
    inventory.update(mouse_pos)

def render_elements():
    WIN.fill(BLACK)
    for i in field:
        for elem in i:
            if elem:
                elem.render(WIN)
                # elem.render_box(WIN) #debug box renderer
    frame.render(WIN)
    inventory.render(WIN)
    # inventory.render_box(WIN) #debug box renderer

def handle_keydown(key):
    if key == pygame.K_ESCAPE:
        pygame.quit()
        exit()
    elif key == pygame.K_k:
        initialise_game()
    elif key == pygame.K_j:
        save_level()
    elif key == pygame.K_l:
        load_level()
    elif key in INV_KEYS.keys():
        inventory.select_tool(INV_KEYS[key])
    else:
        pass

def handle_mouse_press(mouse_press, mouse_pos):
    if on_field(mouse_pos):
        frame.click(mouse_press, field, inventory.tool)
    elif on_inventory(mouse_pos):
        inventory.click(mouse_press, mouse_pos)
    
def main():
    initialise_game()
    global game_state, field
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_press = pygame.mouse.get_pressed()
                handle_mouse_press(mouse_press, mouse_pos)

        keys_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if game_state == "gameon":

            update_components(mouse_pos)

            render_elements()
        
            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":

    main()