import pygame
pygame.init()
pygame.mixer.init()
from scenes import scenes

print("it's a studying project. Sprites and music were copied from original game 'Undertale'")

pygame.display.set_caption("Underfight")

scenes.Main()

print('Thanks for playing')