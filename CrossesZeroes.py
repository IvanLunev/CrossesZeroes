from typing import List

import pygame
from enum import Enum

FPS = 60

WIDTH = 800
HEIGHT = 600

LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)


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
    def __init__(self):
        self.height = 3
        self.width = 3
        self.cells = [[Cell.VOID] * self.width for i in range(self.height)]


class GameFieldView:
    """
    Виджет игрового поля, который отображает его на экране, а также выясняет место клика.
    """

    def __init__(self, field):
        # загрузить картинки значков клеток...
        # отобразить первичное состояние поля
        self._field = field
        self._start_point = ((WIDTH - HEIGHT + 20), 20)
        self._width = (HEIGHT - 40)

    def draw(self, screen):
        pygame.draw.rect(screen, color=LIGHT_GRAY,
                         rect=(self._start_point[0], self._start_point[1], self._width, self._width),
                         width=0, border_radius=10)
        pygame.draw.rect(screen, color=DARK_GRAY,
                         rect=(self._start_point[0], self._start_point[1], self._width, self._width),
                         width=4, border_radius=10)
        for i in range(1, self._field.width):
            pygame.draw.line(screen, color=DARK_GRAY, width=4,
                             start_pos=(self._start_point[0] + i * self._width / 3, self._start_point[1]),
                             end_pos=(self._start_point[0] + i * self._width / 3, self._start_point[1] + self._width))

        for j in range(1, self._field.height):
            pygame.draw.line(screen, color=DARK_GRAY, width=4,
                             start_pos=(self._start_point[0], self._start_point[1] + j * self._width / 3),
                             end_pos=(self._start_point[0] + self._width, self._start_point[1] + j * self._width / 3))

    def check_coords_correct(self, x, y):
        return True  # TODO: self._height учесть

    def get_coords(self, x, y):
        return 0, 0  # TODO: реально вычислить клетку клика


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
        # игрок делает клик на поле
        print("click_handled", i, j)


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

        player1 = Player("Петя", Cell.CROSS)
        player2 = Player("Вася", Cell.ZERO)
        self._game_manager = GameRoundManager(player1, player2)
        self._field_widget = GameFieldView(self._game_manager.field)

        self._field_widget.draw(self._screen)

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
            pygame.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.main_loop()
    print('Game over!')


if __name__ == "__main__":
    main()
