import pygame
import inspect
import constants as const
from typing import List, Callable

class Button:
    def __init__(self, x: int, y: int, text: str, func: Callable, kwargs: dict = {}):
        self.is_selected = False
        self.func = func
        self.kwargs = kwargs
        self.text = text
        self.text_surface = const.FONT.render(text, True, const.ORANGE)
        self.image = const.NSELECTED_BUTTON
        self.rect = pygame.rect.Rect(x, y, const.BUTTON_WIDTH, const.BUTTON_HEIGHT)
        text_wigth, text_height = self.text_surface.get_size()
        self.text_rect = pygame.rect.Rect(self.rect.centerx - text_wigth // 2, self.rect.centery - text_height // 2, 0, 0)

    def activate(self):
        if self.kwargs != {}:
            self.func(self.kwargs)
        else: 
            self.func()

    def update(self):
        if self.is_selected:
            self.image = const.SELECTED_BUTTON
            self.text_surface = const.FONT.render(self.text, True, const.YELLOW)
        else:
            self.image = const.NSELECTED_BUTTON
            self.text_surface = const.FONT.render(self.text, True, const.ORANGE)
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def __repr__(self):
        return str(f'({self.rect.x}, {self.rect.y})')


class ButtonTable:
    def __init__(self, width, height, pos_x, pos_y):
        self.table: List[List[Button]] = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.selected_x = 0
        self.selected_y = 0

    def change_selection(self, x: int, y: int):
        self.table[y][x].is_selected = not self.table[y][x].is_selected

    def add(self, buttons: list[list[dict['text': str, 'func': Callable, 'kwargs': dict]]]):
        if len(buttons) > 1:
            y_offset = (self.height - const.BUTTON_HEIGHT * len(buttons)) // (len(buttons) - 1)
        else:
            y_offset = 0
        
        y = self.pos_y
        for row in buttons:
            if len(row) > 1:
                x_offset = (self.width - const.BUTTON_WIDTH * len(row)) // (len(row) - 1)  
            else:
                x_offset = 0

            x = self.pos_x
            buttons_row = []
            for button in row:
                buttons_row.append(Button(x, y, text=button['text'], func=button['func'], kwargs=button['kwargs']))
                x += x_offset + const.BUTTON_WIDTH

            self.table.append(buttons_row)
            y += y_offset + const.BUTTON_HEIGHT
        self.table[0][0].is_selected = True

    def move(self, x: int = 0, y: int = 0):
        self.change_selection(self.selected_x, self.selected_y)
        self.selected_y = (self.selected_y + y) % len(self.table)
        self.selected_x = (self.selected_x + x) % len(self.table[self.selected_y])
        self.change_selection(self.selected_x, self.selected_y)

    def activate(self):
        self.table[self.selected_y][self.selected_x].activate()

    def update(self):
        for row in self.table:
            for button in row:
                button.update()

    def draw(self, screen: pygame.Surface):
        for row in self.table:
            for button in row:
                button.draw(screen)

def draw_hp_bar(hp, max_hp):
    pygame.draw.rect(const.screen, const.RED, pygame.rect.Rect(
        const.HP_BAR_X,
        const.HP_BAR_Y,
        const.HP_BAR_WIDTH,
        const.HP_BAR_HEIGHT
    ))

    pygame.draw.rect(const.screen, const.YELLOW, pygame.rect.Rect(
        const.HP_BAR_X,
        const.HP_BAR_Y,
        const.HP_BAR_WIDTH * hp // max_hp,
        const.HP_BAR_HEIGHT
    ))