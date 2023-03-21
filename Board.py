from dataclasses import dataclass
import random
import copy
from Cell import Cell, Path, Wall
from SpriteMove import Direction
from Sprite import Food, Sprite


@dataclass
class Board:
    """
        A class to represent a board in Pacman game.
        ...
        Attributes
        ----------
        __cells : list
            list of list of cells.

        Methods
        -------
        board_from_str():
            Method that returns game board from string input.
        cells():
            Returns board cells.
        width():
            Returns board width.
        height():
            Returns board height.
        at():
            Returns a list of sprites in a certain cell.
        directions():
            Returns a list of possible directions from current position on the board.
        insert_food():
            Fills each path cell with one food sprite.
        insert():
            Inserts a sprite into a certain board cell.
        random_cell():
            Returns coordinates of random path cell.
        count_by_type():
            Returns a number of sprites of certain type present on the board.
    """
    __cells: list[list[Cell]]

    @staticmethod
    def board_from_str(lines: str):
        """
        Returns list of lists of board cells.

        Parameters
        ----------
           lines: string representing pacman game board
        """

        class_factory = {" ": Path, "#": Wall}
        board = Board([])
        lines_split = lines.split("\n")

        for line in lines_split:
            row = []
            if len(line) == 0:
                continue
            for ch in line:
                row.append(copy.deepcopy(class_factory[ch]()))
            board.__cells.append(row)

        return board

    @property
    def cells(self):
        return self.__cells

    def width(self):
        return len(self.__cells[0])

    def height(self):
        return len(self.__cells)

    def at(self, i: int, j: int):
        return self.__cells[i][j]

    def directions(self, i: int, j: int) -> list:
        """
        Returns list of possible directions from current cell.

        Parameters
        ----------
           i: row coordinate
           j: column coordinate
        """

        possible_directions = []

        if isinstance(self.__cells[i][j + 1], Path):
            possible_directions.append(Direction.RIGHT)
        if isinstance(self.__cells[i][j - 1], Path):
            possible_directions.append(Direction.LEFT)
        if isinstance(self.__cells[i + 1][j], Path):
            possible_directions.append(Direction.UP)
        if isinstance(self.__cells[i - 1][j], Path):
            possible_directions.append(Direction.DOWN)

        return possible_directions

    def insert_food(self):

        for xs in range(len(self.__cells)):
            for ys in range(len(self.__cells[0])):
                if isinstance(self.__cells[xs][ys], Path):
                    self.__cells[xs][ys].my_sprites().append(Food("f", xs, ys))

    def insert(self, sprite: Sprite):
        self.__cells[sprite.x][sprite.y].my_sprites().append(sprite)

    def random_cell(self) -> tuple[int, int]:

        possible_sprite_indexes = []

        for xs in range(len(self.__cells)):
            for ys in range(len(self.__cells[0])):
                if isinstance(self.__cells[xs][ys], Path):
                    possible_sprite_indexes.append((xs, ys))

        return random.choice(possible_sprite_indexes)

    def count_by_type(self, sprite_type) -> int:

        counter = 0

        for xs in range(len(self.__cells)):
            for ys in range(len(self.__cells[0])):
                for si in self.__cells[xs][ys].my_sprites():
                    if isinstance(si, sprite_type):
                        counter += 1

        return counter
