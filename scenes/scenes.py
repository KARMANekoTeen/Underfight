import pygame
from random import choice
from controls import menu_controls
import constants as const
from scenes import modes
from UI import ButtonTable, draw_hp_bar
from entities import borders, player
from entities.entity_classes import Missile

def menu(func):
    def wrapper(*args):
        screen = const.screen
        clock = const.clock
        fps = const.FPS

        pygame.mixer.music.load("misc/music/start menu.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)

        button_table, texts = func(*args)

        run = True
        while run:
            clock.tick(fps)
            screen.fill(const.BLACK)

            button_table.update()

            button_table.draw(screen)
            for text in texts:
                screen.blit(text[0], text[1])

            for event in pygame.event.get():
                menu_controls(event, button_table)

            pygame.display.flip()
    return wrapper


@menu
def Main() -> ButtonTable:
    text = const.FONT.render(f'UNDERFIGHT', True, const.WHITE)
    text_rect = pygame.rect.Rect(const.SCREEN_WIDTH // 2 - text.get_size()[0] // 2, 100, 0, 0)
    button_table = ButtonTable(
        const.BUTTON_WIDTH * 3 + 100, 
        const.BUTTON_HEIGHT * 3, 
        (const.SCREEN_WIDTH - const.BUTTON_WIDTH) // 2,
        const.SCREEN_HEIGHT // 2
        )
    button_table.add(
        [
            [{'text': 'Start', 'func': Game, 'kwargs': {}}], 
            [{'text': 'Exit', 'func': pygame.quit, 'kwargs': {}}]
        ]
    )
    return (button_table, [(text, text_rect)])


def Game():
    def clean_trash(trash_can, missiles):
        for trash_i in range(len(trash_can)):
            trash = trash_can[trash_i]
            missiles.pop(trash - trash_i)

    screen = const.screen
    clock = const.clock
    fps = const.FPS
    result = 0

    pygame.mixer.music.load("misc/music/megalovania.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    field_borders = borders.Borders()
    you = player.RedHeart()
    mode = 'red'
    new_missile_generator = lambda: modes.red_mode()
    mode_start_time = pygame.time.get_ticks()
    missiles: list[Missile] = []
    max_hp = const.MAX_HP
    hp = max_hp
    run = True
    round_time = const.ROUND_TIME
    time_remains = round_time * fps
    rounds_passed = 0
    is_win = False

    while run:
        clock.tick(fps)
        screen.fill(const.BLACK)

        if is_win or time_remains <= 0:
            is_win = False
            time_remains = round_time * fps
            hp = (hp + 1) 
            if hp > max_hp:
                hp = max_hp
            prev_mode = mode
            if rounds_passed < 12:
                rounds_passed += 1
                mode = choice(('yellow', 'green', 'blue', 'purple'))
                if mode != prev_mode:
                    missiles: list[Missile] = []
                    bullets = []
                    old_you_rect = you.rect
                    if mode == 'red':
                        you = player.RedHeart()
                        you.rect = old_you_rect
                        new_missile_generator = modes.red_mode
                    elif mode == 'yellow':
                        you = player.YellowHeart()
                        you.rect = old_you_rect
                        new_missile_generator = modes.yellow_mode
                    elif mode == 'green':
                        you = player.GreenHeart()
                        new_missile_generator = modes.spawn_green_missile
                    elif mode == 'blue':
                        you = player.BlueHeart()
                        you.rect = old_you_rect
                        new_missile_generator = modes.blue_mode
                    elif mode == 'purple':
                        you = player.PurpleHeart()
                        new_missile_generator = modes.spawn_purple_missile
            else:
                mode = 'orange'
                rounds_passed = 0
                time_remains = 60 * fps
                you = player.OrangeHeart()
                labyrinth = modes.orange_mode()
                you.rect.x = const.BORDERS_X + labyrinth.start_x * const.PLAYER_SIZE
                you.rect.y = const.BORDERS_Y + labyrinth.start_y * const.PLAYER_SIZE
            

        if mode != 'orange':
            new_missiles = new_missile_generator()
            if new_missiles != None:
                for new_missile in new_missiles:
                    missiles.append(new_missile)
            
            trash_can = []
            for missile_i in range(len(missiles)):
                missile = missiles[missile_i]
                damage = missile.update(you)
                if damage != None:
                    hp -= damage
                missile_x = missile.rect.x
                missile_y = missile.rect.y
                
                if missile_x > const.SCREEN_WIDTH \
                or missile_x + missile.rect.width < 0 \
                or missile_y > const.SCREEN_HEIGHT \
                or missile_y + missile.rect.height < 0 \
                or damage != None:
                    trash_can.append(missile_i)

            if mode == 'yellow':
                bullet_trash_can = []
                for bullet_i in range(len(bullets)):
                    bullet = bullets[bullet_i]
                    shoted_bomb = bullet.update(missiles)
                    if shoted_bomb != None:
                        bullet_trash_can.append(bullet_i)
                        trash_can.append(shoted_bomb)
                clean_trash(bullet_trash_can, bullets)

            clean_trash(trash_can, missiles)
            bullet = you.update(field_borders)
            if bullet != None:
                bullets.append(bullet)
            result += 1
            time_remains -= 1
            
        else:
            labyrinth.draw()
            labytinth_result = you.update(field_borders, labyrinth)
            damage = labytinth_result['damage']
            if damage != None:
                hp -= damage
            is_win = labytinth_result['win']
            result -= 1
            time_remains -= 1

        field_borders.update()
        draw_hp_bar(hp, max_hp)

        score_text = const.FONT.render(f'Score: {int(result // 60)}', True, const.WHITE)
        screen.blit(score_text, (100, 100))

        time_text = const.FONT.render(f'Time remains: {int(time_remains // 60)}', True, const.WHITE)
        time_text_size = time_text.get_size()
        screen.blit(time_text, (const.SCREEN_WIDTH - time_text_size[0] - 100, 100))

        pygame.display.flip()
        if hp <= 0:
            run = False
    After_game(int(result // fps))

@menu
def After_game(result) -> tuple[ButtonTable, list[tuple[pygame.Surface, pygame.Rect]]]:
    f = open('./misc/best score.txt', 'r')
    best = int(f.readline().strip())
    f.close()

    your_score = const.FONT.render(f'Your score: {result}', True, const.WHITE)
    your_score_rect = pygame.rect.Rect(
        const.SCREEN_WIDTH // 2 - your_score.get_size()[0] // 2,
        100, 0, 0
        )
    
    best_score = const.FONT.render(f'Best score: {best}', True, const.WHITE)
    best_score_rect = pygame.rect.Rect(
        const.SCREEN_WIDTH // 2 - best_score.get_size()[0] // 2,
        100 + best_score.get_size()[1],
        0, 0
        )
    
    if best < result:
        f = open('./misc/best score.txt', 'w')
        f.write(str(result))
        f.close()

    button_table = ButtonTable(
        const.BUTTON_WIDTH, 
        const.BUTTON_HEIGHT * 2, 
        (const.SCREEN_WIDTH - const.BUTTON_WIDTH) // 2,
        const.SCREEN_HEIGHT // 2
        )
    button_table.add(
        [
            [{'text': 'Continue', 'func': Game, 'kwargs': {}}], 
            [{'text': 'Exit', 'func': pygame.quit, 'kwargs': {}}]
        ]
    )
    return (button_table, [(your_score, your_score_rect), (best_score, best_score_rect)])