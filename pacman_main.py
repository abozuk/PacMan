# -*- coding: utf-8 -*-
"""
PacMan GUI and main loop of the game.
"""

from Board import Board
from Cell import Wall
from Sprite import Sprite, Food, Ghost, PacMan
from SpriteMove import RandomWalk, PersistentWalk, ManualWalk, Direction
import sys
import pygame

board_drawn = """
#################################
#      ####                     #
# #### #### #### #### #### #### #
#                               #
# #### #### #### #### #### #### #
#                               #
# #### #### #### #### #### #### #
#                               #
# ######### #### #### #### ######
#                          ######
#################################
"""

PXY = 30
WIDTH = 600
HEIGHT = 400

FOOD_COLOR = (147, 240, 250)
SPRITE_COLOR = (100, 100, 0)
GHOST_COLOR = (250, 179, 250)
WALL_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT_NAME = pygame.font.match_font('arial')


def draw_board(brd: Board, screen):
    """
    Draws PacMan board in pygame.

    Parameters
    ----------
    brd: game board, list of lists of cells
    screen: pygame window
    """

    # ---------- Set the screen background
    screen.fill(BLACK)
    for i in range(brd.width()):
        for j in range(brd.height()):
            if isinstance(brd.at(j, i), Wall):
                pygame.draw.rect(screen, WALL_COLOR, (i * PXY, j * PXY, PXY, PXY))
            else:
                for s in brd.at(j, i).my_sprites():
                    draw_sprite(s, screen)


def draw_sprite(sprit: Sprite, screen):
    """
    Draws sprites on a pygame board.

    Parameters
    ----------
    sprit: sprite to be drawn
    screen: pygame window
    """

    # sprite coordinates on pygame board
    x = int(PXY * (sprit.x + sprit.size))
    y = int(PXY * (sprit.y + sprit.size))

    if isinstance(sprit, Food):
        x += PXY / 3
        y += PXY / 3

    pygame.draw.circle(screen, sprit.color, (y, x), int(PXY * sprit.size))


def draw_text(surf, text: str, size: int, x: float, y: float):
    """
    Draws text on a pygame screen.

    Parameters
    ----------
    surf: pygame window
    text: text to be written on a screen
    size: text font size
    x: x coordinate of the text
    y: y coordinate of the text
    """

    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x: float, y: float, lives: int):
    """
    Draws circles representing remaining PacMan lives on a pygame screen.

    Parameters
    ----------
    surf: pygame window
    x: x coordinate of text and circles
    y: y coordinate of text and circles
    lives: number of lives to draw
    """

    draw_text(window, "Lives: ", 24, x - 100, y - 15)
    for i in range(lives):
        pygame.draw.circle(surf, WHITE, (x + 30 * i, y), int(PXY * 0.4))


def show_go_screen(text1: str, text2: str = ""):

    draw_text(window, text1, 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    draw_text(window, text2, 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    pygame.display.flip()

    # wait to start the game or to exit pygame
    waiting = True
    while waiting:
        fpsclock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False


if __name__ == "__main__":

    # create board object
    board = Board.board_from_str(board_drawn)

    WINDOW_WIDTH = board.width() * PXY
    WINDOW_HEIGHT = board.height() * PXY

    # fill path cells with food
    board.insert_food()

    pc_mover = ManualWalk()

    sprites = [
        Ghost("g1", *board.random_cell(), RandomWalk()),
        Ghost("g2", *board.random_cell(), RandomWalk()),
        Ghost("g3", *board.random_cell(), PersistentWalk()),
        Ghost("g4", *board.random_cell(), PersistentWalk()),
        PacMan("pc", *board.random_cell(), pc_mover)
    ]

    # insert sprites into board
    for si in sprites:
        board.insert(si)

    pygame.init()

    fps = 5
    fpsclock = pygame.time.Clock()

    was_pressed = pygame.key.get_pressed()

    window = pygame.display.set_mode((board.width() * PXY, board.height() * PXY))
    pygame.display.set_caption("PacMan")
    draw_board(board, window)

    done = False
    game_over = True

    while not done:

        if game_over:
            show_go_screen("Press any key to start")
            game_over = False

        # ---------- process external input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    sys.exit()

        key_is_pressed = pygame.key.get_pressed()

        # set pacman movement direction from keyboard
        if key_is_pressed[pygame.K_UP] and not was_pressed[pygame.K_UP]:
            pc_mover.direction = Direction.DOWN

        elif key_is_pressed[pygame.K_RIGHT] and not was_pressed[pygame.K_RIGHT]:
            pc_mover.direction = Direction.RIGHT

        elif key_is_pressed[pygame.K_DOWN] and not was_pressed[pygame.K_DOWN]:
            pc_mover.direction = Direction.UP

        elif key_is_pressed[pygame.K_LEFT] and not was_pressed[pygame.K_LEFT]:
            pc_mover.direction = Direction.LEFT

        was_pressed = key_is_pressed

        # move sprites
        for si in sprites:
            si.mover(board)

            # check if pacman is on the board
            count_pacman = board.count_by_type(PacMan)

            if count_pacman == 0:
                draw_board(board, window)
                pygame.display.update()
                points = 0
                for sprite in sprites:
                    if isinstance(sprite, PacMan):
                        points = sprite.points
                show_go_screen("Game Over", "Points: " + str(points))
                done = True

        # check number of food on the board
        count_food = board.count_by_type(Food)

        if count_food == 0:
            draw_board(board, window)
            pygame.display.update()
            points = 0
            for sprite in sprites:
                if isinstance(sprite, PacMan):
                    points = sprite.points
            show_go_screen("YOU WIN!", "Points: " + str(points))
            done = True

        draw_board(board, window)
        draw_lives(window, WINDOW_WIDTH * 0.9, WINDOW_HEIGHT * 0.05, sprites[-1].lives)  # PacMan is last in sprites
        pygame.display.update()

        fpsclock.tick(fps)

    pygame.quit()
    sys.exit()
