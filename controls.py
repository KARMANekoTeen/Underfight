import pygame
import UI

def menu_controls(event: pygame.event.Event, buttons: UI.ButtonTable):
    event_type = event.type
    if event_type == pygame.QUIT:
        pygame.quit()
    if event_type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            buttons.move(-1, 0)
        if event.key == pygame.K_RIGHT:
            buttons.move(1, 0)
        if event.key == pygame.K_UP:
            buttons.move(0, -1)
        if event.key == pygame.K_DOWN:
            buttons.move(0, 1)
        if event.key == pygame.K_z:
            buttons.activate()