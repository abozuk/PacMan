from abc import ABC, abstractmethod
from enum import Enum
import random


class Direction(Enum):
    """
    Class representing directions in which sprites can move.
    """
    RIGHT = [0, 1]
    LEFT = [0, -1]
    UP = [1, 0]
    DOWN = [-1, 0]


class StartingDirection(Enum):
    START = [0, 0]


class SpriteMove(ABC):

    @abstractmethod
    def move(self, board, x: int, y: int):
        pass


class RandomWalk(SpriteMove):
    """
    Class to represent strategy of moving in random directions.
    Methods
        -------
        move():
            Returns coordinates of a sprite after making a move.
    """

    def move(self, board, x: int, y: int) -> tuple[int, int]:
        """
        Returns new coordinates of a sprite after making a move.

        Parameters
        ----------
           board : game board
           x : current x coordinate
           y : current y coordinate
        """
        possible_moves = board.directions(x, y)  # possible moves from current position
        d = random.choice(possible_moves)
        xnew = x + d.value[0]
        ynew = y + d.value[1]
        return xnew, ynew


class PersistentWalk(SpriteMove):
    """
        Class to represent strategy of moving in one direction until it is not possible.

        Attributes
        ----------
        __current_direction: Direction
            Current direction of sprite movement.

        Methods
        -------
        current_direction():
            Returns current direction of a sprite.
        move():
            Returns coordinates of a sprite after making a move.
    """
    def __init__(self):
        self.__current_direction = Direction.RIGHT

    @property
    def current_direction(self):
        return self.__current_direction

    def move(self, board, x: int, y: int) -> tuple[int, int]:
        """
        Returns new coordinates of a sprite after making a move.

        Parameters
        ----------
           board : game board
           x : current x coordinate
           y : current y coordinate
        """
        possible_moves = board.directions(x, y)  # possible moves from current position

        if self.__current_direction not in possible_moves:
            self.__current_direction = random.choice(possible_moves)

        xnew = x + self.__current_direction.value[0]
        ynew = y + self.__current_direction.value[1]

        return xnew, ynew


class ManualWalk(SpriteMove):
    """
        Class to represent strategy of moving controlled by a player.

        Attributes
        ----------
        __direction: Direction of sprite movement.

        Methods
        -------
        direction():
            Returns current direction of a sprite.
        move():
            Returns coordinates of a sprite after making a move.
    """

    def __init__(self):
        self.__direction = StartingDirection.START  # at the beginning sprite does not move

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, d):
        self.__direction = d

    def move(self, board, x: int, y: int) -> tuple[int, int]:
        """
        Returns new coordinates of a sprite after making a move.

        Parameters
        ----------
           board : game board
           x : current x coordinate
           y : current y coordinate
        """

        xnew = x + self.__direction.value[0]
        ynew = y + self.__direction.value[1]

        possible_moves = board.directions(x, y)  # possible moves from current position

        if self.__direction in possible_moves:
            return xnew, ynew
        else:
            return x, y
