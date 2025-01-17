import pygame
from pygame import Vector2
from random import randrange
import config
import pygame.freetype

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# flags to start (flag begin, flag bait)
running = True
begin = True
bait = True

clock.tick(60)

pygame.quit()
