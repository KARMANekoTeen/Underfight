import pygame

#screen
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 255)
PINK = (255, 192, 203)

#ingame characteristics
PLAYER_SPEED = 5
JUMP_HEIGHT = 30
MAX_HP = 20
ROUND_TIME = 5

#sizes
PLAYER_SIZE = 20
SHIELD_SIZE = PLAYER_SIZE * 5
YELLOW_BULLET_HEIGHT = 16
YELLOW_BULLET_WIDTH = 8
DEFAULT_BORDERS_WIDTH = PLAYER_SIZE * 30
DEFAULT_BORDERS_HEIGHT = PLAYER_SIZE * 15
BORDERS_X = (SCREEN_WIDTH - DEFAULT_BORDERS_WIDTH) // 2
BORDERS_Y = 300
BUTTON_HEIGHT = 50

BUTTON_WIDTH = 150
HP_BAR_WIDTH = 100
HP_BAR_HEIGHT = HP_BAR_WIDTH // 2
HP_BAR_Y = BORDERS_Y + DEFAULT_BORDERS_HEIGHT + 10
HP_BAR_X = (SCREEN_WIDTH - HP_BAR_WIDTH) // 2
FONT = pygame.font.Font('misc/font/font.otf', 32)

#IMAGES
def get_image(path: str, size: tuple[int]):
    return pygame.transform.scale(pygame.image.load(f'images/{path}'), size)

#player
RED_HEART = get_image('player/red.png', (PLAYER_SIZE, PLAYER_SIZE))
BLUE_HEART = get_image('player/blue.png', (PLAYER_SIZE, PLAYER_SIZE))
YELLOW_HEART = get_image('player/yellow.png', (PLAYER_SIZE, PLAYER_SIZE))
YELLOW_BULLET = get_image('player/yellow bullet.png', (YELLOW_BULLET_WIDTH, YELLOW_BULLET_HEIGHT))
PURPLE_HEART = get_image('player/purple.png', (PLAYER_SIZE, PLAYER_SIZE))
GREEN_HEART = get_image('player/green.png', (PLAYER_SIZE, PLAYER_SIZE))
GREEN_SHIELD = get_image('player/green shield.png', (SHIELD_SIZE, SHIELD_SIZE))
ORANGE_HEART = get_image('player/orange.png', (PLAYER_SIZE, PLAYER_SIZE))

#ui
SELECTED_BUTTON = get_image('UI/button_selected.png', (BUTTON_WIDTH, BUTTON_HEIGHT))
NSELECTED_BUTTON = get_image('UI/button_nselected.png', (BUTTON_WIDTH, BUTTON_HEIGHT))
ORANGE_GUIDE = [
    'КРАСНЫЕ ПЛИТКИ НЕПРОХОДИМЫ! ТЫ НЕ МОЖЕШЬ ХОДИТЬ ПО НИМ! ЖЁЛТЫЕ ПЛИТКИ ЗАРЯЖЕНЫ ТОКОМ!',
    'ОНИ МОГУТ УДАРИТЬ ТЕБЯ! ОРАНЖЕВЫЕ ПЛИТКИ ПАХНУТ АПЕЛЬСИНАМИ. СТУПИВ НА НИХ, ТЫ БУДЕШЬ',
    'ПАХНУТЬ ВКУСНО! А СИНИЕ ПЛИТКИ — ВОДЯНЫЕ. ПРОПЛЫВИ ЧЕРЕЗ НИХ, ЕСЛИ ХОЧЕШЬ, НО...',
    'ЕСЛИ ПАХНЕШЬ АПЕЛЬСИНАМИ! ПИРАНЬИ ПОКУСАЮТ ТЕБЯ. А ТАКЖЕ ЕСЛИ СИНЯЯ ПЛИТКА РЯДОМ, НУ,',
    'С ЖЁЛТОЙ ПЛИТКОЙ, ВОДА УБЬЁТ ТЕБЯ! ФИОЛЕТОВЫЕ ПЛИТКИ СКОЛЬЗКИЕ! ТЫ ПРОСКОЛЬЗИШЬ К',
    'СЛЕДУЮЩЕЙ ПЛИТКЕ! ОДНАКО, МЫЛО НА ФИОЛЕТОВЫХ ПЛИТКАХ... ПАХНЕТ ЛИМОНАМИ!! КОТОРЫЕ НЕ',
    'НРАВЯТСЯ ПИРАНЬЯМ! ФИОЛЕТОВЫЕ И ГОЛУБЫЕ ПЛИТКИ — НОРМАЛЬНЫЕ! И, НАКОНЕЦ, РОЗОВЫЕ ПЛИТКИ.',
    'ОНИ НИЧЕГО НЕ СДЕЛАЮТ. СТУПАЙ НА НИХ, КАК ХОЧЕШЬ.'
]

#missiles
GREEN_MISSILE_SIZE = 16
GREEN_MISSILE = get_image('missiles/green bullet.png', (GREEN_MISSILE_SIZE, GREEN_MISSILE_SIZE))
SPIDER_MISSILE_SIZE = 16
SPIDER_MISSILE = get_image('missiles/spider.png', (SPIDER_MISSILE_SIZE, SPIDER_MISSILE_SIZE))
BONE_MISSILE_WIDTH = 16
BONE_MISSILE = get_image('missiles/bone.png', (BONE_MISSILE_WIDTH, BONE_MISSILE_WIDTH * 4))
YELLOW_BOMB_SIZE = 16
YELLOW_BOMB_MISSILE = get_image('missiles/yellow bomb.png', (YELLOW_BOMB_SIZE, YELLOW_BOMB_SIZE))