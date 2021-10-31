#
# Sudoku Solver
# by Furkan Ercevik
# 30 October 2021
# This program implements basic features of object-oriented programming and the recursive backtracking algorithm to
# devise a solution to an incomplete Sudoku puzzle
#


def get_square_coors(indices: tuple) -> list:
    """
    Finds the coordinates of the other elements in the corresponding square
    located in
    :param indices: row and column indices
    :return: list of tuples representing coordinates
    """
    coors = []
    row, col = indices

    # Find the values of the start row and column coordinates
    if row < 3:
        start_row = 0
    elif row < 6:
        start_row = 3
    else:
        start_row = 6

    if col < 3:
        start_col = 0
    elif col < 6:
        start_col = 3
    else:
        start_col = 6

    # Append the list of coordinates in the square
    for i in range(3):
        for j in range(3):
            coors.append((start_row + i, start_col + j))

    # Remove the initial coordinates
    coors.remove(indices)
    # Return the final list of coordinates
    return coors


class Sudoku(object):

    def __init__(self, board=None, file=None):
        """
        Constructs a Sudoku object
        :param board: 2x2 matrix consisting of numbers from 0-9 where 0 represents an empty cell
        """
        # If a board matrix exists use it
        if board:
            self.board = board
        # Otherwise use the text file containing the numbers as the board where each 9 numbers corresponds to a single
        # row
        else:
            self.board = []
            with open(file, "r") as f:
                w = f.read().replace("\n", " ")
                nums = [int(n) for n in w.split()]
            for i in range(9):
                self.board.append(nums[i*9:(i*9)+9])

    def solve(self) -> bool:
        """
        Using a backtracking algorithm, this function sets and resets the values of empty cells to numbers between
        1 and 9 until all of the cells are filled with values that abide by Sudoku's rules
        :return: True if all the cells can be properly filled with values from 1-9, False if otherwise
        """
        # Iterate over all the rows and columns
        for r in range(9):
            for c in range(9):
                # If the value at board[r][c] is 0 start trying out values from 1-9
                if not self.board[r][c]:
                    for val in range(1, 10):
                        # Validate that the value at that position works
                        if self.validate(r, c, val):
                            self.board[r][c] = val
                            # If all the solutions for the next empty cells make logical sense return True
                            if self.solve():
                                return True
                            else:
                                # Otherwise reassign the current value to 0 and redo the backtracking process
                                self.board[r][c] = 0
                    # If all the values have been tried and don't work then this solution is incorrect
                    return False
        # If there are no more empty cells return True
        return True

    def solved(self) -> bool:
        """
        Checks if the Sudoku board has been solved
        :return: True if it solved, False if otherwise
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

    def validate(self, r: int, c: int, val: int) -> bool:
        """
        Checks if the value at self.board[r][c] doesn't violate the rules of Sudoku
        :param self: the Sudoku object itself
        :param val: value that is being checked
        :param r: int value corresponding to a row position
        :param c: int value corresponding to a col position
        :return: True if it doesn't violate rules of Sudoku, False if it does
        """
        # Create a list of values in the same column as (r,c)
        cols = []
        for i in range(9):
            if i != r:
                cols.append(self.board[i][c])
        rows = self.board[r][:c] + self.board[r][c+1:]
        sq = get_square_coors((r, c))
        if val in cols:
            return False
        if val in rows:
            return False
        if val in sq:
            return False
        return True

    def __str__(self) -> str:
        """
        Returns an elegant string representation of the board
        :return: string representing the board and its values
        """
        string = ""
        for i in range(9):
            # Every 3 rows add a big dashed line
            if i % 3 == 0:
                string += "+---------+---------+---------+\n"
            for j in range(9):
                # If the col index is a multiple of 3 add a pipe to the string
                if j % 3 == 0:
                    string += "|"
                # Add the value or '.' to the string
                string += " " + str(self.board[i][j] if self.board[i][j] else ".") + " "
                # If the col index is the last one, add a pipe as well
                if j == 8:
                    string += "|"
            # Add a new line at every row
            string += "\n"
        # Add the final big dashed line
        string += "+---------+---------+---------+"
        return string


def main():
    board = [[0, 0, 4, 0, 0, 0, 0, 6, 7],
             [3, 0, 0, 4, 7, 0, 0, 0, 5],
             [1, 5, 0, 8, 2, 0, 0, 0, 3],

             [0, 0, 6, 0, 0, 0, 0, 3, 1],
             [8, 0, 2, 1, 0, 5, 6, 0, 4],
             [4, 1, 0, 0, 0, 0, 9, 0, 0],

             [7, 0, 0, 0, 8, 0, 0, 4, 6],
             [6, 0, 0, 0, 1, 2, 0, 0, 0],
             [9, 3, 0, 0, 0, 0, 7, 1, 0]]

    s = Sudoku(board=board)
    print(s)
    s.solve()
    print(s)

    p = Sudoku(file="Sudokus")
    print(p)
    p.solve()
    print(p)


main()




