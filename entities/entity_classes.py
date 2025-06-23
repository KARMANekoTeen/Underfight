import pygame
import constants as const

class Entity:
    def __init__(self, left: int, top: int, width: int, height: int, image: pygame.Surface):
        self.rect = pygame.rect.Rect(left, top, width, height)
        self.image = image

    def update(self):
        const.screen.blit(self.image, self.rect)

class MovingEntity(Entity):
    def __init__(self, left, top, width, height, image, speed):
        super().__init__(left, top, width, height, image)
        self.speed = speed
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        
    def move(self):
        if self.moving_up:
            self.rect.y -= self.speed
        if self.moving_down:
            self.rect.y += self.speed
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed

    def update(self):
        self.move()
        super().update()
    

class Player(MovingEntity):
    def __init__(self, image):
        super().__init__(
            (const.SCREEN_WIDTH - const.PLAYER_SIZE) // 2,
            const.BORDERS_Y + (const.DEFAULT_BORDERS_HEIGHT - const.PLAYER_SIZE) // 2,
            const.PLAYER_SIZE,
            const.PLAYER_SIZE,
            image,
            const.PLAYER_SPEED
            )
        
        self.using_ability = False

    def controls(self, event: pygame.event.Event):
        event_type = event.type
        if event_type == pygame.QUIT:
            pygame.quit()

        if event_type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.key_left(True)
            if event.key == pygame.K_RIGHT:
                self.key_right(True)
            if event.key == pygame.K_UP:
                self.key_up(True)
            if event.key == pygame.K_DOWN:
                self.key_down(True)
            if event.key == pygame.K_z:
                self.key_action(True)

        if event_type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.key_left(False)
            if event.key == pygame.K_RIGHT:
                self.key_right(False)
            if event.key == pygame.K_UP:
                self.key_up(False)
            if event.key == pygame.K_DOWN:
                self.key_down(False)
            if event.key == pygame.K_z:
                self.key_action(False)

    def key_up(self, is_pressed):
        self.moving_up = is_pressed

    def key_down(self, is_pressed):
        self.moving_down = is_pressed

    def key_left(self, is_pressed):
        self.moving_left = is_pressed
    
    def key_right(self, is_pressed):
        self.moving_right = is_pressed

    def key_action(self, is_pressed):
        pass

    def update(self, field_borders):
        for event in pygame.event.get():
            self.controls(event)
        self.move()
        field_borders.collide(self)
        const.screen.blit(self.image, self.rect)


class Missile(MovingEntity):
    def __init__(self, left, top, width, height, image, speed, damage, isdestructive):
        super().__init__(left, top, width, height, image, speed)
        self.damage = damage
        self.isdestructive = isdestructive
        
    def update(self, player: Player):
        super().update()
        if self.rect.colliderect(player.rect):
            return self.damage


class Border(Entity):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height, None)

    def update(self):
        pygame.draw.rect(const.screen, const.WHITE, self.rect)