# Sudoku-Solver
This is a simple text-based sudoku solver.
To use: update the Sudokus text file with the 81 numbers you want for your Sudoku puzzle.
Make sure that each of these numbers are space-separated and are within the range of 0-9
where 0 represents an empty cell and 1-9 represents a filled out cell. The program will
print out a textual representation of the unsolved puzzle, then a solved representation of
it.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Sudoku-Solver.
(To be implemented)
```bash
pip install git+https://github.com/fercevik729/Sudoku-Solver/master
```

## Usage

```python
from Sudoku-Solver import Sudoku_display

# displays a pygame window of the Sudoku puzzle. To completely solve press SPACEBAR. At the end after 5 seconds it will close and print out the time it took to solve it
Sudoku_display.visualize(delay=DELAY)

```

## Example

### Unsolved
![sudoku_unsolved](https://user-images.githubusercontent.com/62676762/139597870-227b5b12-095d-421a-bba9-86830e82c156.png)

### In progress
![Sudoku_in_progree](https://user-images.githubusercontent.com/62676762/139597903-537c4e87-258e-4034-922a-e365fb7fcd92.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
