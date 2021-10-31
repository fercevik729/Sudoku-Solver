# Sudoku-Solver
This is a simple text-based sudoku solver.
To use: update the Sudokus text file with the 81 numbers you want for your Sudoku puzzle.
Make sure that each of these numbers are space-separated and are within the range of 0-9
where 0 represents an empty cell and 1-9 represents a filled out cell. The program will
print out a textual representation of the unsolved puzzle, then a solved representation of
it.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install Sudoku-Solver
```

## Usage

```python
from Sudoku-Solver import Sudoku_solver

# displays a Sudoku puzzle
Sudoku_solver.visualize()

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
