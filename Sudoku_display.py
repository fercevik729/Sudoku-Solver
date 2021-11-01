#
# Sudoku Game
# by Furkan Ercevik
# 31 October 2021
# This program uses Sudoku_solver.py and pygame to make a Sudoku game with various features
#
import copy
import datetime
from Sudoku_solver import Sudoku
import pygame
import sys
import time
import random

# TODO: Make "note" function for user to note potential values in the squares bound to RIGHT-CLICK

# Pygame window setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sudoku")

# CONSTANTS
LOGO = pygame.image.load("assets/letter_s.png")
GRID = pygame.image.load("assets/blank-sudoku-grid.png")
pygame.display.set_icon(LOGO)
COLORS = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "GREEN": (0, 255, 0), "RED": (255, 0, 0),
          "LBLUE": (173, 216, 230), "YELLOW": (255, 255, 0)}
DELAY = 0.0001
FONT = pygame.font.SysFont("Trebuchet", 25)
TIME_FONT = pygame.font.SysFont("Trebuchet", 40)
ALLOWED_MISTAKES = 3
ALLOWED_HINTS = 5


class Puzzle(object):
    """
    Makes Puzzle objects that can hold Square objects
    """
    start_x, start_y = (8, 7)
    delta_x, deltay_y = (88, 66)

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
                    ls.append(Square(r, c, self.start_x + c * self.delta_x, self.start_y + r * self.deltay_y, 80, 60,
                                     str(self.board[r][c]), mutable=False))
                # Otherwise make sure it's mutable
                else:
                    ls.append(Square(r, c, self.start_x + c * self.delta_x, self.start_y + r * self.deltay_y, 80, 60))
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

        # Generates the blank spaces
        blanks = 60
        for p in random.sample(range(81), blanks):
            sudoku.board[p // 9][p % 9] = 0

        self.board = copy.deepcopy(sudoku.board)
        sudoku.solve()
        self.solved_board = sudoku.board

    def check(self) -> int:
        """
        Checks for correctness of all values in the squares and resets the values of the incorrect squares
        :return: int representing the number of mistakes
        """
        returnable = 0
        # For all the squares in the puzzle check that they match with the squares of the solved board
        for i in range(9):
            for j in range(9):
                # If the value exists
                sq = self.squares[i][j].get_val()
                # If sq is nonzero and it doesn't match the corresponding value in the solved board
                # replace and return False
                if sq and self.solved_board[i][j] != sq:
                    self.squares[i][j].replace("")
                    returnable += 1
        return returnable

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
        self.squares[r][c].active = None

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

    def handle_event(self, event):
        """
        Handles movement key events
        :return: True if movement occurred
        """
        # Get the active square
        active_squares = []
        for i in range(9):
            active_squares.extend((list(filter(lambda s: s.active, self.squares[i]))))
        if len(active_squares) > 0:
            active_sq = active_squares.pop()
        else:
            active_sq = None
        # If there is an active square
        if active_sq:
            row = active_sq.r
            col = active_sq.c

            # If there is a key press
            if event.type == pygame.KEYDOWN:
                # Check what kind of key was pressed
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and row > 0:
                    # If it was a movement key, toggle the activity status of the current active square and the next
                    # available square if there is no mutable square in that direction there is no new_active_sq
                    active_sq.toggle()
                    new_active_sq = active_sq
                    i = row - 1
                    while i >= 0:
                        available = self.squares[i][col].active
                        if available is not None:
                            new_active_sq = self.squares[i][col]
                            break
                        else:
                            i -= 1
                    new_active_sq.toggle()

                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and row < 8:
                    active_sq.toggle()
                    new_active_sq = active_sq
                    i = row + 1
                    while i <= 8:
                        available = self.squares[i][col].active
                        if available is not None:
                            new_active_sq = self.squares[i][col]
                            break
                        else:
                            i += 1
                    new_active_sq.toggle()
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and col < 8:
                    active_sq.toggle()
                    new_active_sq = active_sq
                    i = col + 1
                    while i <= 8:
                        available = self.squares[row][i].active
                        if available is not None:
                            new_active_sq = self.squares[row][i]
                            break
                        else:
                            i += 1
                    new_active_sq.toggle()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and col > 0:
                    active_sq.toggle()
                    new_active_sq = active_sq
                    i = col - 1
                    while i >= 0:
                        available = self.squares[row][i].active
                        if available is not None:
                            new_active_sq = self.squares[row][i]
                            break
                        else:
                            i -= 1
                    new_active_sq.toggle()


class Square(object):
    # TODO: add gray numbers
    """
     Makes Square objects that represents the individual squares of the Sudoku puzzle
    """

    def __init__(self, r, c, x, y, w, h, text="", mutable=True):
        """
        Initializes a Square object
        :param x: x_position
        :param y: y_position
        :param w: width
        :param h: height
        :param text: current value
        :param mutable: determines if the text's values will be mutable by the user; default value is True
        """
        self.r = r
        self.c = c
        self.text = str(text)
        self.rect = pygame.Rect(x, y, w, h)
        self.text_surface = FONT.render(text, True, COLORS["BLACK"])
        self.b_color = COLORS["WHITE"]
        self.active = None if not mutable else False

    def handle_event(self, event) -> None:

        # If the event is a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the square can be active
            # Check if the click is left-click
            if event.button == 1:
                if self.active is not None:
                    # Check if the rectangle collides with the event
                    if self.rect.collidepoint(event.pos):
                        self.active = not self.active
                        self.b_color = COLORS["LBLUE"]
                    else:
                        self.active = False
                        self.b_color = COLORS["WHITE"]

        # If the event is a keypress
        if event.type == pygame.KEYDOWN:
            # If the cell is active check the different kinds of key presses
            if self.active:
                # If the key press is a backspace
                if event.key == pygame.K_BACKSPACE:
                    self.text = ""
                # If the event key is a movement key render the text surface
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    self.text_surface = FONT.render(self.text, True, COLORS["RED"])
                else:
                    try:
                        val = int(event.unicode)
                        self.text = event.unicode if val in range(1, 10) else ""
                    except ValueError:
                        self.text = ""
                self.text_surface = FONT.render(self.text, True, COLORS["RED"])

    def draw(self, s) -> None:
        """
        Blits a white rect onto the previous text to replace it, renders the text surface, then resets the text color
        :param s: pygame surface to draw on
        :return: None
        """
        # Reset the rectangle
        pygame.draw.rect(s, self.b_color, self.rect)
        # Output the text onto the screen with the current surface
        s.blit(self.text_surface, (self.rect.x + 32, self.rect.y + 22))
        # Reset the text surface color
        color = COLORS["RED"] if self.active is not None else COLORS["BLACK"]
        self.text_surface = FONT.render(str(self.text), True, color)

    def toggle(self):
        """
        Toggles the activity status if active isn't None as well as the color of the box
        :return: None
        """
        if self.active is not None:
            self.active = not self.active

        if self.active:
            self.b_color = COLORS["LBLUE"]
        else:
            self.b_color = COLORS["WHITE"]

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
    active_sq = None
    while True:

        # Draw the clock on the screen
        elapsed_time = datetime.datetime.now() - start_time
        s = elapsed_time.seconds
        minutes, seconds = divmod(s, 60)
        time_str = f'Time:  {minutes:02}:{seconds:02}'
        time_surface = TIME_FONT.render(str(time_str), True, COLORS["WHITE"])
        # Clear the old time with the new time
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(SCREEN_WIDTH-195, SCREEN_HEIGHT - 60, 200, 60))
        screen.blit(time_surface, (SCREEN_WIDTH-195, SCREEN_HEIGHT-60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call handle_event on the squares
            for sq_row in puzzle.squares:
                for sq in sq_row:
                    sq.handle_event(event)

            # Let the puzzle handle the movement events
            puzzle.handle_event(event)

            # If a key press is heard check for various conditions
            if event.type == pygame.KEYDOWN:
                # If it's ENTER check the puzzle
                # 13 is the event key representing ENTER
                if event.key == 13:
                    val = puzzle.check()
                    if val:
                        mistakes += val
                        # If too many mistakes are made
                        if mistakes >= ALLOWED_MISTAKES:
                            print("Puzzle could not be solved")
                            puzzle.visual_solve(screen, delay=0)
                            pygame.quit()
                            sys.exit()

                # For auto solving
                if event.key == pygame.K_SPACE:
                    solved = puzzle.visual_solve(screen, delay=delay)

                # For hints
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

        # Draw the mistakes in the bottom left
        mistake_surface = TIME_FONT.render("Mistakes: " + str(mistakes), True, COLORS["RED"])
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(30, SCREEN_HEIGHT - 60, 200, 400))
        screen.blit(mistake_surface, (30, SCREEN_HEIGHT - 60))

        # Draw the Sudoku name
        title_surface = TIME_FONT.render("Welcome to Sudoku", True, COLORS["YELLOW"])
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(260, SCREEN_HEIGHT - 60, 270, 400))
        screen.blit(title_surface, (260, SCREEN_HEIGHT - 60))
        # Draw the boxes
        puzzle.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

        # If the puzzle is solved
        if solved:
            print(f"Puzzle solved in {time_str} minutes and seconds.")
            time.sleep(10)
            pygame.quit()
            sys.exit()


play(delay=DELAY)
