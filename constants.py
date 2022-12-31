import pygame

WIDTH, HEIGHT = 1000, 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)

FPS = 60

AND_IMAGE = pygame.image.load('And.png')
AND = pygame.transform.scale(AND_IMAGE, (55, 40))