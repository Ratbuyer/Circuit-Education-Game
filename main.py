import pygame
from constants import *



def draw():

    WIN.fill(WHITE)
    WIN.blit(AND, (500, 500))
    pygame.display.update()
    return
 

def main():

    pygame.display.set_caption("Circuit Education")

    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:

                run = False
        
        draw()


    pygame.QUIT


if __name__ == "__main__":

    main()