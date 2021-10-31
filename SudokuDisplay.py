from sudokusolver import Sudoku
import pygame
import sys
import time

# Setup the actual display
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sudoku")

LOGO = pygame.image.load("assets/letter_s.png")
pygame.display.set_icon(LOGO)
COLORS = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "GREEN": (0, 255, 0)}

FONT = pygame.font.Font(None, 14)


class Square (object):
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
        self.value = text
        self.text_surface = FONT.render(text, True, COLORS["BLACK"])
        self.active = False

    def handle_event(self, event) -> None:
        """
        Handles events for the Tile object
        :param event: an event
        :return: None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the rectangle
            if self.rect.collidepoint(event.pos):
                # Flip the active variable
                self.active = not self.active
            else:
                self.active = False
        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:
            # Check if the box is active
            if self.active:
                # If the backspace key is pressed reset the tile text
                if event.key == pygame.K_BACKSPACE:
                    self.text = ""
                elif event.key == pygame.K_KP_ENTER:
                    self.active = False
                # Otherwise if event.unicode is an integer in range(1,10) set the Tile
                # text to that
                else:
                    try:
                        val = int(event.unicode)
                        self.text = event.unicode if val in range(1, 10) else ""
                    except ValueError:
                        self.text = ""
                # Re-render the text.
                self.text_surface = FONT.render(self.text, True, COLORS["BLACK"])

    def draw(self, s):
        # Output the text on the pygame screen
        s.blit(self.text_surface, self.rect.x+5, self.rect.y+5)
        pygame.draw.rect(s, COLORS["WHITE"], self.rect, 2)

    # For use with Sudoku algorithms
    def delete(self, s):
        self.text = ""

    def replace(self, value, s):
        self.text = value
        self.text_surface = FONT.render(value, True, COLORS["GREEN"])


def main():
    start_time = time.time()

    # Create all the square objects
    boxes = []
    for r in range(9):
        for c in range(9):
            boxes.append(Square())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event()


        # If the program takes too long just quit lmao
        if time.time() - start_time > 300:
            pygame.quit()
            print("Bummer...the puzzle appears unsolvable")
            sys.exit()
        else:
            # Constantly load the sudoku template
            screen.blit(pygame.image.load("assets/blank-sudoku-grid.png"), (0, 0))

            pygame.display.update()
            # Check if user clicks on
            # Update the boxes in the display as the user provides input
            # When the user wants the computer to solve it they press the SPACE BAR
            # # Create a Sudoku object with the values in the display board as part of the board attribute
            # # As the Sudoku.solve() method runs, update the display board with the new values in a green-bordered
            # # square
            # # If the value is incorrect, update the display board with red-bordered squares
            # # Repeat until completion
            # Done

main()
