import pygame
import constants as const
from random import randint, choice
from entities import player, borders, entity_classes, missiles

class Cell:
    def __init__(self, left, top):
        self.rect = pygame.rect.Rect(
            const.BORDERS_X + left * const.PLAYER_SIZE,
            const.BORDERS_Y + top * const.PLAYER_SIZE,
            const.PLAYER_SIZE,
            const.PLAYER_SIZE
        )
        self.is_start = False
        self.is_end = False
        self.color = None
        self.is_path = False
        self.is_daughter = False
        self.field_x = left
        self.field_y = top
        
        self.path_length = 0
        self.euristic = 0
        self.direction = None

    @property
    def weight(self):
        return self.path_length + self.euristic
        
    def become_path(self, field: list[list], is_cross: bool = True) -> list:
        def get_neighbours(distance: int):
            neightbours = {
                'up': None,
                'down': None,
                'left': None,
                'right': None
            }
            if self.field_x >= distance:
                neightbours['left'] = (self.field_y, self.field_x - distance)
            if self.field_x <= len(field[0]) - distance - 1:
                neightbours['right'] = (self.field_y, self.field_x + distance)
            if self.field_y >= distance:
                neightbours['up'] = (self.field_y - distance, self.field_x)
            if self.field_y <= len(field) - distance - 1:
                neightbours['down'] = (self.field_y + distance, self.field_x)
            return neightbours
        
        self.close = get_neighbours(1)
        self.is_path = True
        if self.color == const.RED:
            self.color = choice(
                [
                const.GREEN,
                const.BLUE,
                const.PURPLE,
                const.PINK
                ]
            )

        if is_cross:
            self.far = get_neighbours(2)
            paths = []
            daughters = []
            for side, far_coord in self.far.items():
                if far_coord != None:
                    if field[far_coord[0]][far_coord[1]].is_path:
                        paths.append(self.close[side])
                    elif not field[far_coord[0]][far_coord[1]].is_daughter:
                        daughters.append(field[far_coord[0]][far_coord[1]])
                        field[far_coord[0]][far_coord[1]].is_daughter = True
            if paths != []:
                new_path = choice(paths)
                field[new_path[0]][new_path[1]].become_path(field, False)
            return daughters
        
    def activate(self, you: player.Player, field_borders, labyrinth):
        result = {
            'damage': 0,
            'win': False
        }
        if self.color == const.RED:
            if you.moving_up:
                you.moving_up = False
                you.rect.y += you.speed
            elif you.moving_down:
                you.moving_down = False
                you.rect.y -= you.speed
            elif you.moving_left:
                you.moving_left = False
                you.rect.x += you.speed
            elif you.moving_right:
                you.moving_right = False
                you.rect.x -= you.speed
        elif self.color == const.YELLOW:
            result['damage'] = 5
        elif self.color == const.GREEN:
            you.smell = True
        elif self.color == const.BLUE:
            yellow_nearby = False
            for side, coords in self.close.items():
                if coords != None \
                and labyrinth.field[coords[0]][coords[1]].color == const.YELLOW:
                    yellow_nearby = True
                    print(yellow_nearby)
                    print(self.close)
            if yellow_nearby or you.smell:
                result['damage'] = 10
        elif self.color == const.PURPLE:
            you.smell = False
            if not (
                you.moving_up and self.field_y == 0
                or you.moving_down and self.field_y == const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // const.PLAYER_SIZE
                or you.moving_left and self.field_x == 0
                or you.moving_right and self.field_x == const.BORDERS_X + const.DEFAULT_BORDERS_WIDTH // const.PLAYER_SIZE
            ):
                result = you.update(field_borders, labyrinth)
        elif self.color == const.BLACK:
            print('win')
            result['win'] = True
        return result
        
    def draw(self):
        if self.is_end:
            pygame.draw.rect(const.screen, const.BLACK, self.rect)
        else:
            pygame.draw.rect(const.screen, self.color, self.rect)

    def __eq__(self, other):
        return self.weight == other.weight
    
    def __ne__(self, other):
        return self.weight != other.weight
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __gt__(self, other):
        return self.weight > other.weight
    
    def __le__(self, other):
        return self.weight <= other.weight
    
    def __ge__(self, other):
        return self.weight >= other.weight

    def __repr__(self):
        return str(self.rect.center)



class Labyrinth:
    def __init__(self):
        self.field: list[list[Cell]] = []
        self.unset_path_cells: list[Cell] = []

        self.field_height = const.DEFAULT_BORDERS_HEIGHT // const.PLAYER_SIZE
        self.field_width = const.DEFAULT_BORDERS_WIDTH // const.PLAYER_SIZE
        for top in range(self.field_height):
            self.field.append([])
            for left in range(self.field_width):
                self.field[top].append(Cell(left, top))

        self.start_y = randint(0, self.field_height - 1)
        self.start_x = randint(0, self.field_width - 1)
        self.end_y = None
        self.end_x = None
        daughters = self.field[self.start_y][self.start_x].become_path(self.field)
        for cell in daughters:
            self.unset_path_cells.append(cell)
        self.field[self.start_y][self.start_x].is_start = True
        self.weights: list[Cell] = []

    def create(self):
        while self.unset_path_cells != []:
            cell_i = randint(0, len(self.unset_path_cells) - 1)
            cell = self.unset_path_cells.pop(cell_i)
            daughters = cell.become_path(self.field)
            for daughter_cell in daughters:
                self.unset_path_cells.append(daughter_cell)
        cell.is_end = True
        self.end_y = cell.field_y
        self.end_x = cell.field_x
        self._find_path()
        self._set_colors()

    def _find_path(self):
        current_cell: Cell = self.field[self.end_y][self.end_x]
        while not current_cell.is_start:
            for side, path_i in current_cell.close.items():
                if path_i != None:
                    path: Cell = self.field[path_i[0]][path_i[1]]
                    if path.is_path and path.direction == None:
                        if current_cell.field_x > path.field_x:
                            direction = 'right'
                        elif current_cell.field_x < path.field_x:
                            direction = 'left'
                        elif current_cell.field_y > path.field_y:
                            direction = 'down'
                        elif current_cell.field_y < path.field_y:
                            direction = 'up'
                        path.direction = direction
                        path.euristic = abs(self.start_x - path.field_x) + abs(self.start_y - path.field_y)
                        path.path_length = current_cell.path_length + 1
                        self.weights.append(path)
            current_cell = self.weights[0]
            min_i = 0
            for cell_i in range(1, len(self.weights)):
                if current_cell > self.weights[cell_i]:
                    min_i = cell_i
                    current_cell = self.weights[cell_i]
            self.weights.pop(min_i)
        current_cell.direction = direction
    
    def _set_colors(self):
        for top in range(self.field_height):
            for left in range(self.field_width):
                current_cell = self.field[top][left]
                if current_cell.is_path:
                    colors = (const.GREEN, const.BLUE, const.PURPLE, const.PINK)
                else:
                    colors = (const.RED, const.YELLOW)
                current_cell.color = choice(colors)

        current_cell: Cell = self.field[self.start_y][self.start_x]
        current_cell.color = const.PINK
        orange_effect = False
        while not current_cell.is_end:
            prev_cell = current_cell
            current_cell_coord = prev_cell.close[prev_cell.direction]
            current_cell = self.field[current_cell_coord[0]][current_cell_coord[1]]
            colors = [const.GREEN, const.PINK]

            yellow_nearby = False
            for side, coords in current_cell.close.items():
                if coords != None \
                and side != current_cell.direction \
                and self.field[coords[0]][coords[1]].color == const.YELLOW:
                    yellow_nearby = True
                    print(yellow_nearby)

            if not (yellow_nearby or orange_effect):
                colors.append(const.BLUE)
                    
            if current_cell.direction == prev_cell.direction:
                colors.append(const.PURPLE)

            color = choice(colors)
            if color == const.PURPLE:
                orange_effect = False
            elif color == const.GREEN:
                orange_effect = True
            current_cell.color = color
        current_cell.color = const.BLACK

    def draw(self):
        for height in range(self.field_height):
            for width in range(self.field_width):
                self.field[height][width].draw()

    def activate(self, you: player.OrangeHeart, field_borders):
        field_x = (you.rect.x - const.BORDERS_X) // const.PLAYER_SIZE
        field_y = (you.rect.y - const.BORDERS_Y) // const.PLAYER_SIZE
        current_cell: Cell = self.field[field_y][field_x]
        return current_cell.activate(you, field_borders, self)


    
def red_mode():
    pass

def orange_mode():
    lab = Labyrinth()
    lab.create()
    return lab

def yellow_mode():
    if randint(1, 100) <= 80:
        return [missiles.YellowBomb(randint(0, const.DEFAULT_BORDERS_WIDTH - const.YELLOW_BOMB_SIZE))]

def spawn_green_missile():
    if randint(1, 100) <= 2:
        return [missiles.GreenArrow(choice((0, 90, 180, 270)))]


def blue_mode():
    if randint(1, 100) <= 2:
        side = choice(('left', 'right'))
        max_height = const.JUMP_HEIGHT * const.PLAYER_SPEED - const.PLAYER_SIZE * 2
        height = randint(16, max_height)
        return [missiles.BlueBone(side, height)]

def spawn_purple_missile():
    lines = (
        const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 4,
        const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 2,
        const.BORDERS_Y + const.DEFAULT_BORDERS_HEIGHT // 4 * 3
        )
    
    for line in lines:
        pygame.draw.rect(const.screen, const.PURPLE, pygame.rect.Rect(
            const.BORDERS_X,
            line,
            const.DEFAULT_BORDERS_WIDTH,
            1
        )
        )

    create = randint(0, 100) < 3
    if create:
        on_chosen_line = randint(0, 1)
        chosen_line = randint(0, 2)
        facing = choice(['left', 'right'])
        if facing == 'left':
            spiders_x = const.BORDERS_X + const.DEFAULT_BORDERS_WIDTH
        else:
            spiders_x =  const.BORDERS_X - const.SPIDER_MISSILE_SIZE
        spiders = []
        for line in range(3):
            if (line == chosen_line) and on_chosen_line \
            or (line != chosen_line) and not on_chosen_line:
                spiders.append(missiles.PurpleSpider(spiders_x, lines[line] - const.SPIDER_MISSILE_SIZE // 2, facing))
        return spiders