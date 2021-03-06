#
# Sudoku Game
# by Furkan Ercevik
# 31 October 2021
# This program uses Sudoku_solver.py and pygame to make a Sudoku game with various features
#
import copy
import datetime
from Sudoku_solver import Sudoku
from Sudoku_solver import get_square_coors
import pygame
import sys
import time
import random


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
          "LBLUE": (173, 216, 230), "BLUE": (65, 105, 225), "YELLOW": (255, 255, 0),
          "DARKGRAY": (105, 105, 105), "GRAY": (220, 220, 220)}
DELAY = 0.0001
FONT = pygame.font.SysFont("Trebuchet", 35)
NOTE_FONT = pygame.font.SysFont("Trebuchet", 20)
HEADING_FONT = pygame.font.SysFont("Trebuchet", 40)
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
        blanks = 55
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

    def filled(self) -> bool:
        """
        Checks if all the squares are filled
        :return: True if all squares are filled, False if they aren't
        """

        for row in self.squares:
            for sq in row:
                if not sq.text:
                    return False
        return True

    def hint(self) -> None:
        """
        Modifies an empty square with a correct answer
        :return:
        """
        idx = random.randint(0, 81)
        r = idx // 9
        c = idx % 9
        # While the square's value is filled
        while self.squares[r][c].get_val():
            idx = random.randint(0, 82)
            r = idx // 9
            c = idx % 9
        self.squares[r][c].replace(self.solved_board[r][c])
        self.squares[r][c].active = None

    def visual_solve(self, window: pygame.surface, delay: float) -> bool:
        """
        Creates a Sudoku object and calls solve on it with visualization on
        :param window:
        :param delay:
        :return:
        """
        sudo = Sudoku(board=self.board)
        return sudo.solve(self.squares, window, delay)

    def draw(self, s: pygame.surface) -> None:
        """
        Draws the tiles of the board as well as the adjacent tiles if a given tile is active
        :param s: pygame window
        :return: None
        """
        # Checks if there are any active squares
        flag = False
        active_sq = None
        for row in self.squares:
            for sq in row:
                # If there is an active square highlight all the adjacent squares
                if sq.active:
                    flag = True
                    active_sq = sq
                sq.draw(s)
        # If there are active squares highlight the adjacent squares
        if flag:
            draw_others = self.neighbor_squares(active_sq.r, active_sq.c)
            for elem in draw_others:
                r, c = elem
                self.squares[r][c].draw(s, color=COLORS["BLUE"], adj=True)

    def handle_event(self, event: pygame.event):
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

    def neighbor_squares(self, r: int, c: int) -> list:
        """
        Returns a list of neighboring squares for a given square's row and column index
        :param r: row index
        :param c: col index
        :return: list of neighboring squares' indices
        """
        neighbors = []
        s = Sudoku(self.board)
        neighbors.extend(s.get_col_idx(r, c))
        neighbors.extend(s.get_row_idx(r, c))
        neighbors.extend(get_square_coors((r, c)))
        return neighbors

    def deactivate(self, s: pygame.surface):
        for row in self.squares:
            for sq in row:
                if sq.note_mode:
                    sq.note_mode = False
                    sq.note = []
                    sq.b_color = (255, 255, 255)
                    sq.draw(s)
                if sq.active:
                    sq.active = False
                    sq.b_color = (255, 255, 255)
                    sq.draw(s)
                pygame.display.update(sq.rect)


class Square(object):
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
        self.note_mode = False
        self.note = []

    def handle_event(self, event: pygame.event) -> None:
        """
        Handles events for Square objects
        :param event: pygame.event
        :return: None
        """
        # If the event is a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the square can be active
            if self.active is not None:
                # Check if the rectangle collides with the event
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                    self.b_color = COLORS["LBLUE"] if self.active else COLORS['WHITE']
                    # Check if note_mode is on and if so disable it and reset the notes
                    self.note_mode = False
                    self.note = []
                else:
                    self.active = False
                    self.b_color = COLORS["WHITE"]

        # If the event is a keypress
        if event.type == pygame.KEYDOWN:
            # If note mode is enabled
            if self.note_mode:
                # Was backspace key pressed
                if event.key == pygame.K_BACKSPACE:
                    try:
                        self.note.pop()
                    # If there are no more note numbers left set the box's note mode to False
                    except IndexError:
                        self.note_mode = False
                # Add the integer to the notes
                try:
                    if int(event.unicode) in range(1, 10):
                        self.note.append(event.unicode)
                        self.note.sort()
                except ValueError:
                    pass

            # If the cell is active check for other key presses
            if self.active:
                # If the key press is a backspace
                if event.key == pygame.K_BACKSPACE:
                    self.text = ""
                # If the event key is a movement key render the text surface
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_w, pygame.K_s,
                                   pygame.K_a, pygame.K_d]:
                    self.text_surface = FONT.render(self.text, True, COLORS["RED"])

                # Toggle note_mode when key N is pressed
                elif event.key == pygame.K_n:
                    self.note_mode = not self.note_mode
                    self.b_color = COLORS["GRAY"] if self.note_mode else COLORS["LBLUE"]
                else:
                    try:
                        val = int(event.unicode)
                        self.text = event.unicode if val in range(1, 10) else ""
                    except ValueError:
                        self.text = ""
                self.text_surface = FONT.render(self.text, True, COLORS["RED"])

    def draw(self, s: pygame.surface, color=None, adj=False) -> None:
        """
        Blits a white rect onto the previous text to replace it, renders the text surface, then resets the text color
        If note mode is enabled blit a light gray rectangle
        :param adj: flag to determine if the square is being drawn adjacently
        :param s: pygame surface to draw on
        :param color: auxilliary color choice for drawing highlighted squares
        :return: None
        """
        if not self.note_mode:
            # Reset the rectangle
            if color:
                pygame.draw.rect(s, color, self.rect)
            else:
                pygame.draw.rect(s, self.b_color, self.rect)
            # Output the text onto the screen with the current surface
            s.blit(self.text_surface, (self.rect.x + 32, self.rect.y + 22))
            # Reset the text surface color
            color = COLORS["RED"] if self.active is not None else COLORS["BLACK"]
            self.text_surface = FONT.render(str(self.text), True, color)
        else:
            if adj:
                pygame.draw.rect(s, (135, 206, 250), self.rect)
            else:
                pygame.draw.rect(s, self.b_color, self.rect)
            for v in self.note:
                integer = int(v)
                surface = NOTE_FONT.render(v, True, COLORS["DARKGRAY"])
                if integer in range(1, 4):
                    s.blit(surface, (self.rect.x + 5 + (integer-1) * 20, self.rect.y))
                elif integer in range(4, 7):
                    s.blit(surface,
                           (self.rect.x + 5 + (integer-4) * 20, self.rect.y + 20))
                elif integer in range(7, 10):
                    s.blit(surface,
                           (self.rect.x + 5 + (integer-7) * 20, self.rect.y + 40))

                    pygame.display.update(self.rect)

    def toggle(self):
        """
        Toggles the activity status if the cell's active isn't None as well as the color of the box
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

    def replace(self, value: str) -> None:
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


def instructions():
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("|          Welcome to my Sudoku game!!        |")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("|                 CONTROLS                    |")
    print("|    MOUSECLICK = Select/Deselect a square    |")
    print("|          ENTER = Check for accuracy         |")
    print("|              H = Ask for a hint             |")
    print("|    N = enable/disable notes for a square    |")
    print("|       SPACEBAR = Solve puzzle entirely      |")
    print("| WASD = up, down, left, right, respectively  |")
    print("| UP,DOWN,LEFT,RIGHT = up, down, left, right  |")
    print("|                 ESC = QUIT                  |")
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")


def play(delay=0.001) -> None:
    """
    Plays the sudoku game
    :param delay: delay of the visual solve
    :return: None
    """
    instructions()
    # Get the start time
    start_time = datetime.datetime.now()
    # Create the Puzzle object to represent the game board
    puzzle = Puzzle()
    hints_left = ALLOWED_HINTS
    mistakes = 0
    # Blit the sudoku grid
    screen.blit(GRID, (0, 0))

    # Game loop
    solved = False
    clock = pygame.time.Clock()
    while True:

        # Draw the clock on the screen
        elapsed_time = datetime.datetime.now() - start_time
        s = elapsed_time.seconds
        minutes, seconds = divmod(s, 60)
        time_str = f'Time:  {minutes:02}:{seconds:02}'
        time_surface = HEADING_FONT.render(str(time_str), True, COLORS["WHITE"])
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

                # If key is ESCAPE quit the game
                if event.key == pygame.K_ESCAPE:
                    print("Game ended.")
                    pygame.quit()
                    sys.exit()
                # If it's ENTER check the puzzle
                # 13 is the event key representing ENTER
                if event.key == 13:
                    mistake = puzzle.check()
                    win = puzzle.filled()

                    # If there was a mistake
                    if mistake:
                        mistakes += mistake
                        # If too many mistakes are made
                        if mistakes >= ALLOWED_MISTAKES:
                            print("Puzzle could not be solved.")
                            puzzle.visual_solve(screen, delay=0)
                            pygame.quit()
                            sys.exit()
                    # If the player correctly fills the puzzle
                    elif win:
                        print(f"Puzzle was solved in {minutes} minutes and {seconds} seconds")
                        if minutes < 5:
                            print(f"Hmmm are you a puzzle solver too??")
                        pygame.quit()
                        sys.exit()

                # For auto solving
                if event.key == pygame.K_SPACE:
                    # Deactivate all the notes and highlighting
                    puzzle.deactivate(screen)
                    # Solve with the delay
                    solved = puzzle.visual_solve(screen, delay=delay)

                # For hints
                if event.key == pygame.K_h:
                    if hints_left > 0:
                        hints_left -= 1
                        puzzle.hint()
                    else:
                        print("Sorry buddy you're out of hints.")

        # If the program takes too long just quit lmao
        if datetime.datetime.now() - start_time > datetime.timedelta(minutes=10):
            pygame.quit()
            print("Bummer...the puzzle appears unsolvable.")
            sys.exit()

        # Draw the mistakes in the bottom left
        mistake_surface = HEADING_FONT.render("Mistakes: " + str(mistakes), True, COLORS["RED"])
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(30, SCREEN_HEIGHT - 60, 200, 400))
        screen.blit(mistake_surface, (30, SCREEN_HEIGHT - 60))

        # Draw the Sudoku name
        title_surface = HEADING_FONT.render("Welcome to Sudoku", True, COLORS["YELLOW"])
        pygame.draw.rect(screen, COLORS["BLACK"], pygame.Rect(260, SCREEN_HEIGHT - 60, 270, 400))
        screen.blit(title_surface, (260, SCREEN_HEIGHT - 60))
        # Draw the boxes
        puzzle.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

        # If the puzzle is solved
        if solved:
            print(f"Puzzle was auto-solved in {minutes} minutes and {seconds} seconds.")
            time.sleep(5)
            pygame.quit()
            sys.exit()


play(delay=DELAY)
