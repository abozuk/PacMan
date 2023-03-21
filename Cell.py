from abc import ABC, abstractmethod
from Sprite import Sprite


class Cell(ABC):
    """
        A class to represent a cell in Pacman game board.
        ...
        Attributes
        ----------
        _mysprites : list
            list of sprites in a cell

        Methods
        -------
        my_sprites():
            Abstract method for getting a list of sprites.
        set_mysprites():
            Abstract method for updating a list of sprites in a cell.
    """
    def __init__(self, sprites: list = None):
        """
        Constructs necessary attributes for the cell object.

        Parameters
        ----------
            sprites : str
                list of sprites in a cell
        """
        if sprites is None:
            sprites = []

        self._mysprites = sprites

    @abstractmethod
    def my_sprites(self):
        pass

    @abstractmethod
    def set_mysprites(self, s):
        pass


class Wall(Cell):
    """
        A class to represent a wall on a board.
        ...
        Methods
        -------
        my_sprites():
            Returns empty list of sprites.
        set_mysprites():
            Sets an empty list of sprites for a wall cell.
    """
    def __init__(self, sprites: list = None):
        super().__init__(sprites)

    def my_sprites(self):
        self._mysprites = []
        return self._mysprites

    def set_mysprites(self, s: Sprite):
        self._mysprites = []


class Path(Cell):
    """
        A class to represent a path on a board.
        ...
        Methods
        -------
        my_sprites():
            Returns a list of sprites in a path cell.
        set_mysprites():
            Adds a sprite to a path cell.
    """
    def __init__(self, sprites: list = None):
        super().__init__(sprites)

    def my_sprites(self): return self._mysprites

    def set_mysprites(self, s: Sprite):
        self._mysprites.append(s)
