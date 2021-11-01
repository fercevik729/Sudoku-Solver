#
# Sudoku Display
# by Furkan Ercevik
# 31 October 2021
# This program uses Sudoku_solver.py and pygame to create a visualization of the backtracking algorithm
#
import copy
import datetime
from Sudoku_solver import Sudoku
import pygame
import sys
import time
import random

# TODO: Future program ideas: turn the visualizer into a playable game with a game clock, have Square objects that
#  the player can edit and confirm the values of, have a background process that checks for mistakes and solves the
#  program after 3 mistakes,

# Pygame window setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sudoku")

# CONSTANTS
LOGO = pygame.image.load("assets/letter_s.png")
GRID = pygame.image.load("assets/blank-sudoku-grid.png")
pygame.display.set_icon(LOGO)
COLORS = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "GREEN": (0, 255, 0), "RED": (255, 0, 0)}
DELAY = 0.0001
FONT = pygame.font.Font(None, 25)
TIME_FONT = pygame.font.Font(None, 40)
ALLOWED_MISTAKES = 3
ALLOWED_HINTS = 5


class Puzzle(object):
    """
    Makes Puzzle objects that can hold Square objects
    """
    start_x, start_y = (25, 20)
    delta_x, deltay_y = (88, 65)

    def __init__(self):
        """
        Initializes a Puzzle object
        """
        self.board = []
        self.solved_board = []
        self.random_generate_board()

        self.squares = []
        for r in range(9):
            ls = []
            for c in range(9):
                # If the value is set ahead of time make sure it's immutable
                if self.board[r][c]:
                    ls.append(Square(self.start_x + c * self.delta_x, self.start_y + r * self.deltay_y, 40,
                                     str(self.board[r][c]), mutable=False))
                # Otherwise make sure it's mutable
                else:
                    ls.append(Square(self.start_x + c * self.delta_x, self.start_y + r * self.deltay_y, 40))
            self.squares.append(ls)

    def random_generate_board(self) -> None:
        """
        Generates a random unsolved sudoku puzzle
        :return: None
        """

        # Generate a full random sudoku puzzle
        b = [[0] * 9 for _ in range(9)]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        b[0][0] = random.choice(numbers)
        sudoku = Sudoku(b)
        sudoku.solve()

        blanks = 60
        for p in random.sample(range(81), blanks):
            sudoku.board[p // 9][p % 9] = 0

        self.board = copy.deepcopy(sudoku.board)
        sudoku.solve()
        self.solved_board = sudoku.board

    def check(self) -> bool:
        """
        Checks for correctness of all values in the squares and resets the values of the incorrect squares
        :return: True if all or correct, False if otherwise
        """
        # For all the squares in the puzzle check that they match with the squares of the solved board
        for i in range(9):
            for j in range(9):
                # If the value exists
                sq = self.squares[i][j].get_val()
                if sq and self.solved_board[i][j] != sq:
                    self.squares[i][j].delete()
                    return False
        return True

    def hint(self) -> None:
        """
        Modifies an empty square with a correct answer
        :return:
        """
        idx = random.randint(0, 82)
        r = idx // 9
        c = idx % 9
        # While the square's value is filled
        while self.squares[r][c].get_val():
            idx = random.randint(0, 82)
            r = idx // 9
            c = idx % 9
        self.squares[r][c].replace(self.solved_board[r][c])

    def get_squares(self):
        return self.squares

    def visual_solve(self, window, delay) -> bool:
        """
        Creates a Sudoku object and calls solve on it with visualization on
        :param window:
        :param delay:
        :return:
        """
        sudo = Sudoku(board=self.board)
        return sudo.solve(self.squares, window, delay)

    def draw(self, s):
        for row in self.squares:
            for sq in row:
                sq.draw(s)


class Square(object):
    # TODO: add event handler for sudoku game
    """
     Makes Square objects that represents the individual squares of the Sudoku puzzle
    """

    def __init__(self, x, y, s, text="", mutable=True):
        """
        Initializes a Tile object
        :param x: x_position
        :param y: y_position
        :param s: size
        :param text: current value
        :param mutable: determines if the text's values will be mutable by the user; default value is True
        """
        self.text = str(text)
        self.rect = pygame.Rect(x, y, s, s)
        self.text_surface = FONT.render(text, True, COLORS["BLACK"])
        self.b_color = COLORS["WHITE"]

    def draw(self, s) -> None:
        """
        Blits a white rect onto the previous text to replace it, renders the text surface, then resets the text color
        :param s: pygame surface to draw on
        :return: None
        """
        # Reset the rectangle
        pygame.draw.rect(s, COLORS["WHITE"], self.rect)
        # Output the text onto the screen with the current surface
        s.blit(self.text_surface, (self.rect.x + 17, self.rect.y + 13))

        # Reset the text surface color
        self.text_surface = FONT.render(str(self.text), True, COLORS["BLACK"])

    # For use with Sudoku algorithms
    def delete(self) -> None:
        """
        Renders the text surface with a white color
        :return: None
        """
        # Clear the number values
        self.text_surface = FONT.render(str(self.text), True, COLORS["WHITE"])
        self.text = ""

    def replace(self, value) -> None:
        """
        Renders the text surface with a green color
        :param value: the value to replace the original text with
        :return: None
        """
        self.text = value
        self.text_surface = FONT.render(str(self.text), True, (0, 255, 0))

    def get_val(self) -> int:
        """
        Provides the value of the Square object
        :return: an integer representation of the text stored within the square object
        """
        return int(self.text) if self.text else 0


def play(delay=0.001):
    start_time = datetime.datetime.now()
    # Create the Puzzle object to represent the game board
    puzzle = Puzzle()
    hints_left = ALLOWED_HINTS
    mistakes = 0

    # Game loop
    solved = False
    clock = pygame.time.Clock()
    while True:

        # Draw the clock on the screen
        elapsed_time = datetime.datetime.now() - start_time
        s = elapsed_time.seconds
        minutes, seconds = divmod(s, 60)
        time_str = f'{minutes:02}:{seconds:02}'
        time_surface = TIME_FONT.render(str(time_str), True, COLORS["WHITE"])
        # Clear the old time with the new time
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50, 100, 50))
        screen.blit(time_surface, (SCREEN_WIDTH-100, SCREEN_HEIGHT-50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Create a sudoku object and call solve on it
            if event.type == pygame.KEYDOWN:
                # If a key press is heard visually solve the puzzle
                if event.key == pygame.K_SPACE:
                    solved = puzzle.visual_solve(screen, delay=delay)

                if event.key == pygame.K_h:
                    if hints_left > 0:
                        hints_left -= 1
                        puzzle.hint()
                    else:
                        print("Sorry buddy you're out of hints")

        # If the program takes too long just quit lmao
        if datetime.datetime.now() - start_time > datetime.timedelta(minutes=10):
            pygame.quit()
            print("Bummer...the puzzle appears unsolvable")
            sys.exit()
        # Constantly load the sudoku template
        screen.blit(GRID, (0, 0))

        # Draw the boxes
        puzzle.draw(screen)
        # Update the boxes
        pygame.display.flip()
        clock.tick(30)

        # If the puzzle is solved
        if solved:
            print(f"Puzzle solved in {time_str} seconds.")
            time.sleep(10)
            pygame.quit()
            sys.exit()

        # If too many mistakes are made
        elif mistakes == ALLOWED_MISTAKES:
            print("Puzzle could not be solved")
            puzzle.visual_solve(screen, delay=0)
            pygame.quit()
            sys.exit()


play(delay=DELAY)