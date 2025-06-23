import pygame
import constants as const
from entities.entity_classes import Player, Border

class Borders:
    def __init__(self):
        self.borders_width = const.DEFAULT_BORDERS_WIDTH
        self.borders_height = const.DEFAULT_BORDERS_HEIGHT
        self.borders_y = const.BORDERS_Y

        self.up_y = self.borders_y
        self.down_y = self.borders_y + self.borders_height
        self.left_x = (const.SCREEN_WIDTH - self.borders_width) // 2
        self.right_x = (const.SCREEN_WIDTH + self.borders_width) // 2

        self.left_border = Border(
            self.left_x,
            self.up_y,
            1,
            self.borders_height
        )
        self.right_border = Border(
            self.right_x,
            self.up_y,
            1,
            self.borders_height
        )
        self.up_border = Border(
            self.left_x,
            self.up_y,
            self.borders_width,
            1
        )
        self.down_border = Border(
            self.left_x,
            self.down_y,
            self.borders_width,
            1
        )
        
        self.borders = {
            'up': self.up_border,
            'down': self.down_border,
            'left': self.left_border,
            'right': self.right_border
        }

    def collide(self, player: Player):
        collided = False
        if player.rect.y < const.BORDERS_Y:
            player.rect.y = const.BORDERS_Y
            collided = True
        if player.rect.y > const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT - player.rect.height:
            player.rect.y = const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT - player.rect.height
            collided = True
            if player.color == 'blue':
                player.moving_down = False
                player.jumping = False
        if player.rect.x < const.BORDERS_X:
            player.rect.x = const.BORDERS_X
            collided = True
        if player.rect.x > const.BORDERS_X + const.DEFAULT_BORDERS_WIDTH - player.rect.width:
            player.rect.x = const.BORDERS_X + const.DEFAULT_BORDERS_WIDTH - player.rect.width
            collided = True
    
    def update(self):
        for name, border in self.borders.items():
            border.update()