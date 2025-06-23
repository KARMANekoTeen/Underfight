from entities.entity_classes import Player, Entity
from entities.missiles import YellowBullet
from entities.borders import Borders
import constants as const
import pygame

class RedHeart(Player):
    def __init__(self):
        super().__init__(const.RED_HEART)
        self.color = 'red'


class BlueHeart(Player):
    def __init__(self):
        super().__init__(const.BLUE_HEART)
        self.color = 'blue'
        self.moving_down = True
        self.jumping = True
        self.current_height = 0
        self.jump_height = 40

    def key_down(self, is_pressed):
        pass

    def key_up(self, is_pressed):
        if not self.jumping and is_pressed:
            self.jumping = True
            self.moving_up = True
            self.moving_down = False
            self.current_height = 0
        elif not is_pressed:
            self.current_height = self.jump_height
            self.moving_up = False
            self.moving_down = True
    
    def update(self, field_borders):
        if self.jumping:
            self.current_height += 1
        if self.current_height == self.jump_height:
            self.moving_up = False
            self.moving_down = True
            self.current_height = 0
        super().update(field_borders)

class OrangeHeart(Player):
    def __init__(self):
        super().__init__(const.ORANGE_HEART)
        self.smell = False
        self.color = 'orange'
        self.speed = const.PLAYER_SIZE

    def move(self):
        if self.moving_up:
            self.rect.y -= self.speed
        elif self.moving_down:
            self.rect.y += self.speed
        elif self.moving_left:
            self.rect.x -= self.speed
        elif self.moving_right:
            self.rect.x += self.speed

    def update(self, field_borders, labyrinth):
        for event in pygame.event.get():
            self.controls(event)
        self.move()
        field_borders.collide(self)
        result = {
            'damage': 0,
            'win': False
        }
        if self.moving_up or self.moving_down or self.moving_left or self.moving_right:
            result = labyrinth.activate(self, field_borders)

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        const.screen.blit(self.image, self.rect)
        return result

class YellowHeart(Player):
    def __init__(self):
        super().__init__(const.YELLOW_HEART)
        self.color = 'yellow'
        self.shooting_timeout = 5
        self.timeout = self.shooting_timeout
    
    def key_action(self, is_pressed):
        self.using_ability = is_pressed
        
    def update(self, field_borders):
        super().update(field_borders)
        if self.timeout < self.shooting_timeout:
            self.timeout += 1
        if self.using_ability and self.timeout == self.shooting_timeout:
            self.timeout = 0
            return (YellowBullet(
                self.rect.centerx - const.YELLOW_BULLET_WIDTH // 2,
                self.rect.centery
                ))

class PurpleHeart(Player):
    def __init__(self):
        super().__init__(const.PURPLE_HEART)
        self.line = 1
        self.color = 'purple'

    def key_up(self, is_pressed):
        if is_pressed and self.line > 0:
            self.rect.y -= const.DEFAULT_BORDERS_HEIGHT // 4
            self.line -= 1
    
    def key_down(self, is_pressed):
        if is_pressed and self.line < 2:
            self.rect.y += const.DEFAULT_BORDERS_HEIGHT // 4
            self.line += 1

class GreenHeart(Entity):
    def __init__(self):
        super().__init__(
            (const.SCREEN_WIDTH - const.PLAYER_SIZE) // 2,
            const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 2,
            const.PLAYER_SIZE,
            const.PLAYER_SIZE,
            const.GREEN_HEART
            )
        self.color = 'yellow'
        self.shield = Entity(0, 0, const.SHIELD_SIZE, const.SHIELD_SIZE, const.GREEN_SHIELD)
        self.shield.rect.center = self.rect.center
        self.shield_side = 0
        self.default_rotation_speed = 30
        self.rotation_speed = 10
        self.angle = 0
        self.rotating = False

    def controls(self, event: pygame.event.Event):
        event_type = event.type
        if event_type == pygame.QUIT:
            pygame.quit()

        if event_type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_shield_side(0)
            elif event.key == pygame.K_RIGHT:
                self.change_shield_side(270)
            elif event.key == pygame.K_DOWN:
                self.change_shield_side(180)
            elif event.key == pygame.K_LEFT:
                self.change_shield_side(90)

    def change_shield_side(self, side: int):
        if not self.rotating:
            self.shield_side = side
            if self.shield_side - self.angle > 180 or self.shield_side - self.angle < 0 and self.shield_side - self.angle > -180:
                self.rotation_speed = - self.default_rotation_speed
            else:
                self.rotation_speed = self.default_rotation_speed
            self.rotating = True

    def update(self, field_border):
        screen = const.screen
        for event in pygame.event.get():
            self.controls(event)
        if self.angle != self.shield_side and (self.angle + 360) != self.shield_side:
            self.angle = (self.angle + self.rotation_speed) % 360
            self.shield.image = pygame.transform.rotozoom(const.GREEN_SHIELD, self.angle, 1)
            self.shield.rect = self.shield.image.get_rect(center=self.shield.rect.center)
        else:
            self.angle = self.shield_side
            self.rotating = False
        self.shield.update()
        super().update()