import pygame
import constants as const
from random import choice
from entities.entity_classes import Entity, MovingEntity, Missile

class YellowBullet(MovingEntity):
    def __init__(self, left, top):
        super().__init__(
            left, 
            top, 
            const.YELLOW_BULLET_WIDTH, 
            const.YELLOW_BULLET_HEIGHT, 
            const.YELLOW_BULLET, 
            16
            )
        self.moving_up = True

    def update(self, missiles: list[Missile]):
        super().update()
        for missile_i in range(len(missiles)):
            if self.rect.colliderect(missiles[missile_i].rect):
                return missile_i
        
class YellowBomb(Missile):
    def __init__(self, left):
        super().__init__(
            const.BORDERS_X + left, 
            const.BORDERS_Y - const.DEFAULT_BORDERS_HEIGHT, 
            const.YELLOW_BOMB_SIZE, 
            const.YELLOW_BOMB_SIZE, 
            const.YELLOW_BOMB_MISSILE, 
            5, 
            1, 
            True)
        self.moving_down = True
        self.scatter = 5
        self.current_scatter = self.scatter
        self.horizontal_speed = 4
        self.scatter_direction = 1
    
    def update(self, player):
        if abs(self.current_scatter) == self.scatter:
            self.scatter_direction = -self.scatter_direction
            self.horizontal_speed = -self.horizontal_speed
        self.current_scatter += self.scatter_direction
        self.rect.x += self.horizontal_speed
        return super().update(player)

class GreenArrow(Missile):
    def __init__(self, facing):
        self.facing = facing
        super().__init__(
            0,
            0,
            const.GREEN_MISSILE_SIZE,
            const.GREEN_MISSILE_SIZE,
            const.GREEN_MISSILE,
            5,
            1,
            True
            )
        
        if self.facing == 90:
            self.rect.left = const.BORDERS_X
            self.rect.top = const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 2
            self.moving_right = True
        elif self.facing == 270:
            self.rect.left = (const.SCREEN_WIDTH + const.DEFAULT_BORDERS_WIDTH) // 2 - self.rect.width
            self.rect.top = const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 2
            self.moving_left = True
        elif self.facing == 180:
            self.rect.left = const.SCREEN_WIDTH // 2
            self.rect.top = const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT
            self.moving_up = True
        elif self.facing == 0:
            self.rect.left = const.SCREEN_WIDTH // 2
            self.rect.top = const.BORDERS_Y - self.rect.width
            self.moving_down = True
        self.image = pygame.transform.rotozoom(const.GREEN_MISSILE, (self.facing + 180) % 360, 1)
    
    def update(self, you):
        if self.rect.colliderect(you.shield.rect):
            if you.shield_side == self.facing:
                return 0
        return super().update(you)

class BlueBone(Missile):
    def __init__(self, side, height):
        super().__init__(0, 0, const.BONE_MISSILE_WIDTH, height, const.BONE_MISSILE, 5, 1, True)
        if side == 'left':
            left = const.BORDERS_X - const.BONE_MISSILE_WIDTH
            self.moving_right = True
        elif side == 'right':
            left = (const.SCREEN_WIDTH + const.DEFAULT_BORDERS_WIDTH) // 2
            self.moving_left = True
        top = const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT - height
        self.rect.x = left
        self.rect.y = top
        self.image = pygame.transform.scale(self.image, (const.BONE_MISSILE_WIDTH, height))
        
class PurpleSpider(Missile):
    def __init__(self, left, top, facing):
        super().__init__(
            left,
            top,
            const.SPIDER_MISSILE_SIZE,
            const.SPIDER_MISSILE_SIZE,
            const.SPIDER_MISSILE,
            5,
            1,
            True)
        if facing == 'left':
            self.moving_left = True
        else:
            self.moving_right = True