from typing import List

import pygame
from enum import Enum

FPS = 60

WIDTH = 800
HEIGHT = 600

LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Cell(Enum):
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """
    Класс игрока, содержащий тип значков и имя.
    """

    def __init__(self, name, cell_type):
        self.name = name
        self.cell_type = cell_type


class GameField:
    """
    Класс поля, который хранит значения в ячейках.
    """

    def __init__(self):
        self.height = 5
        self.width = 5
        self.cells = [[Cell.VOID] * self.height for i in range(self.width)]


class GameFieldView:
    """
    Виджет игрового поля, который отображает его на экране, а также выясняет место клика.
    """
    _space = 20

    def __init__(self, field, screen):
        self._field = field
        self._start_point = ((WIDTH - HEIGHT + self._space), self._space)
        self._width = (HEIGHT - self._space * 2)
        self._cell_width = self._width / self._field.width
        self._cell_height = self._width / self._field.height
        self._screen = screen
        self.draw()

    def draw(self):
        pygame.draw.rect(self._screen, color=LIGHT_GRAY,
                         rect=(self._start_point[0], self._start_point[1], self._width, self._width),
                         width=0, border_radius=10)
        pygame.draw.rect(self._screen, color=DARK_GRAY,
                         rect=(self._start_point[0], self._start_point[1], self._width, self._width),
                         width=4, border_radius=10)
        for j in range(1, self._field.width):
            pygame.draw.line(self._screen, color=DARK_GRAY, width=4,
                             start_pos=(self._start_point[0] + j * self._width / self._field.width,
                                        self._start_point[1]),
                             end_pos=(self._start_point[0] + j * self._width / self._field.width,
                                      self._start_point[1] + self._width))

        for i in range(1, self._field.height):
            pygame.draw.line(self._screen, color=DARK_GRAY, width=4,
                             start_pos=(self._start_point[0],
                                        self._start_point[1] + i * self._width / self._field.height),
                             end_pos=(self._start_point[0] + self._width,
                                      self._start_point[1] + i * self._width / self._field.height))

        def draw_cross(cell_i, cell_j):
            pygame.draw.line(self._screen, color=RED, width=8,
                             start_pos=(self._start_point[0] + (cell_j + 0.15) * self._cell_width,
                                        self._start_point[1] + (cell_i + 0.15) * self._cell_height),
                             end_pos=(self._start_point[0] + (cell_j + 0.85) * self._cell_width,
                                      self._start_point[1] + (cell_i + 0.85) * self._cell_height))
            pygame.draw.line(self._screen, color=RED, width=8,
                             start_pos=(self._start_point[0] + (cell_j + 0.85) * self._cell_width,
                                        self._start_point[1] + (cell_i + 0.15) * self._cell_height),
                             end_pos=(self._start_point[0] + (cell_j + 0.15) * self._cell_width,
                                      self._start_point[1] + (cell_i + 0.85) * self._cell_height))

        def draw_zero(cell_i, cell_j):
            pygame.draw.circle(self._screen, color=BLUE, width=8,
                               center=(self._start_point[0] + (cell_j + 0.5) * self._cell_width,
                                       self._start_point[1] + (cell_i + 0.5) * self._cell_height),
                               radius=min(self._cell_width, self._cell_height) / 2.5)

        for i in range(self._field.width):
            for j in range(self._field.height):
                if self._field.cells[i][j] == Cell.ZERO:
                    draw_zero(i, j)
                elif self._field.cells[i][j] == Cell.CROSS:
                    draw_cross(i, j)

    def check_coords_correct(self, x, y):
        return (x > WIDTH - HEIGHT + self._space) &\
               (x < WIDTH - self._space) &\
               (y > self._space) &\
               (y < HEIGHT - self._space)

    def get_coords(self, x, y):
        x = x - (WIDTH - HEIGHT + self._space)
        y = y - self._space
        return int(y//self._cell_height), int(x//self._cell_width)


class GameRoundManager:
    """
    Менеджер игры, запускающий все процессы.
    """

    def __init__(self, player1: Player, player2: Player):
        self._players = [player1, player2]
        self._current_player = 0
        self.field = GameField()

    def handle_click(self, i, j):
        player = self._players[self._current_player]
        if self.field.cells[i][j] == Cell.VOID:
            self.field.cells[i][j] = player.cell_type
            self._current_player = 1 - self._current_player


class GameWindow:
    """
    Содержит виджет поля,
    а также менеджера игрового раунда.
    """

    def __init__(self):
        # инициализация pygame
        pygame.init()

        self._title = "Crosses & Zeroes"
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self._title)

        player1 = Player("Ваня", Cell.CROSS)
        player2 = Player("Аня", Cell.ZERO)
        self._game_manager = GameRoundManager(player1, player2)
        self._field_widget = GameFieldView(self._game_manager.field, self._screen)

    def main_loop(self):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    if self._field_widget.check_coords_correct(x, y):
                        i, j = self._field_widget.get_coords(x, y)
                        self._game_manager.handle_click(i, j)
                        self._field_widget.draw()
            pygame.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.main_loop()
    print('Game over!')


if __name__ == "__main__":
    main()
