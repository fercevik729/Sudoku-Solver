#
# Sudoku Display
# by Furkan Ercevik
# 31 October 2021
# This program uses Sudoku_solver.py and pygame to create a visualization of the backtracking algorithm
#
from Sudoku_solver import Sudoku
import pygame
import sys
import time

# TODO: Future program ideas: turn the visualizer into a playable game with a game clock, have Square objects that
#  the player can edit and confirm the values of, have a background process that checks for mistakes and solves the
#  program after 3 mistakes,

# Pygame window setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sudoku")

# CONSTANTS
LOGO = pygame.image.load("assets/letter_s.png")
GRID = pygame.image.load("assets/blank-sudoku-grid.png")
pygame.display.set_icon(LOGO)
COLORS = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "GREEN": (0, 255, 0), "RED": (255, 0, 0)}
DELAY = 0.0001
FONT = pygame.font.Font(None, 25)


class Square (object):
    # TODO: add event handler for sudoku game
    """
     Makes Square objects that represents the individual squares of the Sudoku puzzle
    """
    def __init__(self, x, y, s, text=""):
        """
        Initializes a Tile object
        :param x: x_position
        :param y: y_position
        :param s: size
        :param text: current value
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
        s.blit(self.text_surface, (self.rect.x+17, self.rect.y+13))

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


def main():
    start_time = time.time()
    s = Sudoku(file="Sudokus")
    # Create all the square objects and store them in a list of lists
    start_x, start_y = (25, 20)
    delta_x, deltay_y = (88, 65)
    boxes = []
    for r in range(9):
        ls = []
        for c in range(9):
            if s.board[r][c]:
                ls.append(Square(start_x + c * delta_x, start_y + r * deltay_y, 40, str(s.board[r][c])))
            else:
                ls.append(Square(start_x + c * delta_x, start_y + r * deltay_y, 40))
        boxes.append(ls)

    # Game loop
    solved = False
    while True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Create a sudoku object and call solve on it
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solved = s.solve(boxes, screen, delay=DELAY)
        if solved:
            print(f"Puzzle solved in {(time.time() - start_time):.2f} seconds.")
            time.sleep(5)
            pygame.quit()
            sys.exit()
        # If the program takes too long just quit lmao
        if time.time() - start_time > 400:
            pygame.quit()
            print("Bummer...the puzzle appears unsolvable")
            sys.exit()
        # Constantly load the sudoku template
        screen.blit(GRID, (0, 0))

        # Draw the boxes
        for row_boxes in boxes:
            for box in row_boxes:
                box.draw(screen)
        # Update the boxes
        pygame.display.flip()
        clock.tick(30)


main()

