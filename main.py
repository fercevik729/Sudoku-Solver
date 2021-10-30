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

        self.loc_sets = []
        self.empty_cells = []

    def get_col(self, index: int) -> list:
        """
        Returns a column of the board corresponding to an index value
        :param index: i integer ranging from 0 to 8
        :return: a list representing the column
        """
        return [val[index] for val in self.board]

    def get_row(self, index: int) -> list:
        """
        Returns a row of the board corresponding to an index value
        :param index: i integer ranging from 0 to 8
        :return: a list representing the row
        """
        return [val for val in self.board[index]]

    def get_sets(self) -> str:
        """
        Returns a string representation of all the sets in the board
        :return: string of all location sets
        """
        string = ""
        for ls_of_sets in self.loc_sets:
            for s in ls_of_sets:
                string += str(s)
            string += "\n"
        return string

    def pprint_board(self) -> str:
        """
        Returns a string representation of the board
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

    def conv_to_sets(self) -> None:
        """
        Converts each of the locations in the sudoku puzzle to sets
        :return: None
        """
        for x in range(9):
            ls = []
            for y in range(9):
                var = {self.board[x][y]} if self.board[x][y] else {1, 2, 3, 4, 5, 6, 7, 8, 9}
                ls.append(var)
            self.loc_sets.append(ls)

    def eliminate(self, location: tuple) -> None:
        """
        Eliminates the value in location from the location sets of all the sets in the row, col, and square
        :param location: tuple corresponding to the row and col indices of a given location
        :return: None
        """
        row, col = location

        # If the value is non zero begin elimination
        if self.board[row][col] > 0 or len(self.loc_sets[row][col]) == 1:
            if self.board[row][col]:
                val = self.board[row][col]
            else:
                val = self.loc_sets[row][col].pop()
                self.loc_sets[row][col].add(val)
            # Deletes the value from all empty cells in the row and column location is in
            for i in range(9):
                if i != col:
                    if len(self.loc_sets[row][i]) > 1:
                        self.loc_sets[row][i].discard(val)
                if i != row:
                    if len(self.loc_sets[i][col]) > 1:
                        self.loc_sets[i][col].discard(val)
            # Deletes the value from all sets in the square
            ls = get_square_coors(location)
            for t in ls:
                r, c = t
                if len(self.loc_sets[r][c]) > 1:
                    self.loc_sets[r][c].discard(val)
                # print(str(r) + ", " + str(c) + ": " + str(self.loc_sets[r][c]))

    def back_tracking_eliminate(self, coors: tuple, val: int) -> bool:
        # TODO: Use a backtracking solution that recursively goes through each of the empty cells and tries solutions

        # For all empty cells check each of the possible values
        # Check if any of them works for the row, col, and square in which coors is located
        coor_r, coor_c = coors
        self.board[coor_r][coor_c] = val
        # Validate that the value at that position works
        if self.validate(coor_r, coor_c):
            self.loc_sets[coor_r][coor_c] = {val}
            # If there are no more empty cells return True
            if len(self.empty_cells) == 0:
                return True
            # Otherwise get the new row and col coordinates of the next empty cell
            else:
                new_r, new_c = self.empty_cells.pop(0)
                values = self.loc_sets[new_r][new_c]
                # Recursively call the method for each of the possible values in the set at that point
                for v in values:
                    self.back_tracking_eliminate((new_r, new_c), v)
        else:
            self.board[coor_r][coor_c] = 0

            return False

    def solve(self) -> None:
        # Convert all the board positions to sets
        self.conv_to_sets()
        # For each pair of location coordinates call the eliminate method to reduce the number of possibilities for all
        # empty cells, potentially to 1
        count = 3
        while count > 0:
            for i in range(9):
                for j in range(9):
                    self.eliminate((i, j))
            count -= 1

        for row in range(9):
            for col in range(9):
                s = self.loc_sets[row][col]
                if len(s) == 1:
                    val = s.pop()
                    s.add(val)
                    self.board[row][col] = val
                else:
                    # If the cell is still empty append it to the list of empty cells
                    self.empty_cells.append((row, col))

        # Start backtracking searching if the sudoku isn't solved yet
        if not self.solved():
            start_cell = self.empty_cells.pop(0)
            start_r, start_c = start_cell
            start_vals = self.loc_sets[start_r][start_c]
            for v in start_vals:
                self.back_tracking_eliminate(start_cell, v)

    def solved(self) -> bool:
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

    def validate(self, r: int, c: int) -> bool:
        """
        Checks if the value at self.board[coor-x][coor-y] doesn't violate the rules of Sudoku
        :param r: int value corresponding to a row position
        :param c: int value corresponding to a col position
        :return: True if it doesn't violate rules of Sudoku, False if it does
        """
        val = self.board[r][c]
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
   # s = Sudoku(board=board)
 #   print(s.pprint_board())
 #   print(s.solve())
 #   print(s.pprint_board())

    p = Sudoku(file="Sudokus")
    print(p.pprint_board())
    print(p.solve())
    print(p.pprint_board())


if __name__ == "__main__":
    main()



