from abc import ABC
from SpriteMove import SpriteMove


class Sprite(ABC):
    """
        A class to represent a sprite in Pacman game.
        ...
        Attributes
        ----------
        _name: sprite name
        _x: row coordinate
        _y: column coordinate
        _color: sprite color
        _size: sprite size

        Methods
        -------
        x():
            Returns row coordinate of a sprite.
        y():
            Returns column coordinate of a sprite.
        name():
            Returns name of a sprite.
        color():
            Returns RGB color value of a sprite.
        size():
            Returns sprite size.
        """

    def __init__(self, name: str, x: int, y: int, color: tuple[int, int, int] = (0, 0, 0), size: float = 0.1):
        self._name = name
        self._x = x
        self._y = y
        self._color = color
        self._size = size

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x_new: int):
        self._x = x_new

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y_new: int):
        self._y = y_new

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c: tuple[int, int, int]):
        self._color = c

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s: float):
        self._size = s


class Food(Sprite):
    """
    A class to represent a food sprite in Pacman game.

    """

    def __init__(self, name: str, x: int, y: int, color: tuple = (147, 240, 250), size: float = 0.1):
        super().__init__(name, x, y, color, size)


class TravelingSprite(Sprite):
    """
    A class to represent sprite object with ability to move.
    ...
        Attributes
        ----------
        _move_strategy: moving strategy
        _collision_solver: dispatch for collision solving

        Methods
        -------
        collision_solver():
            Returns dictionary for collision solving.
        mover():
            Moves sprite into new cell.
    """

    def __init__(self, name: str, x: int, y: int, strategy: SpriteMove, color: tuple = (0, 0, 0),
                 size: float = 0.4):
        super().__init__(name, x, y, color, size)
        self._move_strategy = strategy
        self._collision_solver = {}

    @property
    def collision_solver(self):
        return self._collision_solver

    def mover(self, board):
        """
        Moves sprite into new cell, solves possible collisions, sets new coordinates of a sprite.

        Parameters
        ----------
            board: game board
        """

        move_done = [False]
        xnew, ynew = self._move_strategy.move(board, self.x, self.y)

        for si in board.at(xnew, ynew).my_sprites()[::-1]:

            k = str(si.__class__.__name__)

            if k in self.collision_solver.keys():
                self.collision_solver[k](board, self, si, move_done)
            else:
                continue

        if move_done[0]:
            return

        board.at(xnew, ynew).my_sprites().append(self)
        board.at(self.x, self.y).my_sprites().remove(self)

        self.x, self.y = xnew, ynew


class PacMan(TravelingSprite):
    """
        A class to represent PacMan sprite.
        ...
            Attributes
            ----------
            __lives: number of PacMan lives
            __points: number of points earned

            Methods
            -------
            lives():
                Returns number of lives remaining.
            points():
                Returns number of points earned.
    """

    def __init__(self, name: str, x: int, y: int, strategy: SpriteMove, lives=3, points=0,
                 color: tuple = (255, 239, 1), size: float = 0.4):
        super().__init__(name, x, y, strategy, color, size)
        self.__lives = lives
        self.__points = points
        self._collision_solver = {"Food": EatFood(), "Ghost": PacManHitsGhost()}

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, n_lives: int):
        self.__lives = n_lives

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, n_points: int):
        self.__points = n_points


class Ghost(TravelingSprite):
    """
        A class to represent Ghost sprite.
    """

    def __init__(self, name: str, x: int, y: int, strategy: SpriteMove,
                 color: tuple = (250, 179, 250), size: float = 0.4):
        super().__init__(name, x, y, strategy, color, size)
        self._collision_solver = {"PacMan": GhostHitsPacMan()}


class EatFood:

    def __call__(self, *args):
        """
        Removes food from a certain cell and adds point to a PacMan.

        Parameters
        ---------
        board: game board
        sprite: currently moving sprite
        spritetohit: sprite to collide with
        """

        board = args[0]
        sprite: Sprite = args[1]
        spritetohit: Sprite = args[2]

        board.at(spritetohit.x, spritetohit.y).my_sprites().remove(spritetohit)
        sprite.points = sprite.points + 1


class PacManHitsGhost:

    def __call__(self, *args):
        """
        Removes PacMan from a cell in a board if there is no lives remaining, otherwise removes one life.

        Parameters
        ---------
        board: game board
        sprite: currently moving sprite
        move_done: ends move if PacMan is removed from board
        """

        board = args[0]
        sprite: Sprite = args[1]
        move_done: list = args[3]

        sprite.lives = sprite.lives - 1

        if sprite.lives == 0:
            board.at(sprite.x, sprite.y).my_sprites().remove(sprite)
            move_done[0] = True


class GhostHitsPacMan:

    def __call__(self, *args):
        """
        Removes PacMan from a cell in a board if there is no lives remaining, otherwise removes one PacMan life..

        Parameters
        ---------
        board: game board
        spritetohit: sprite to collide with
        """

        board = args[0]
        spritetohit: Sprite = args[2]

        spritetohit.lives = spritetohit.lives - 1

        if spritetohit.lives == 0:
            board.at(spritetohit.x, spritetohit.y).my_sprites().remove(spritetohit)
