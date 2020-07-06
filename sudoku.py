import os
import sys
from exceptions import ArgumentNumberError

from board import Board


class Sudoku:
    def __init__(self, file_path):
        self._board = Board()
        self._file_path = file_path
        self._values = None

    @property
    def board(self):
        return self._board

    @property
    def file_path(self):
        return self._file_path

    @property
    def values(self):
        return self._values

    def _get_values(self):
        f = open(self.file_path, 'r')
        values = []
        for line in f:
            values.append([int(value) for value in line.strip()])
        f.close()

        self._values = values

    def _validate_values(self):
        assert self._values is not None, (
            "You must call `._get_values()` before calling `._validate_values()`"
        )

        assert len(self._values) == 9, (
            f"Input file {self.file_path} contains {len(self.values)} rows."
            f"File should contain exactly 9 rows."
        )
        for row in self._values:
            assert len(row) == 9, (
                f"Input file {self.file_path} contains a row with {len(row)} columns."
                f"Each row should contain exactly 9 columns."
            )
            for value in row:
                assert value in range(0,10), (
                    f" Input file {self.file_path} contains inputs that are not integers between 0 and 9."
                    f" Value of {value} was found in file."
                )

    def initialize_board(self):
        self._get_values()
        self._validate_values()
        self.board.initialize_values(self.values)

    def solve(self):
        self.board.solve()

def validate_args(args):
    arg_count = len(args)
    if arg_count != 1:
        raise ArgumentNumberError(f"expected 1 argument but received {arg_count}")

    if not os.path.isfile(args[0]):
        abs_path = os.path.abspath(args[0])
        raise FileNotFoundError(f"could not find file define by input argument {abs_path}")


if __name__ == '__main__':
    validate_args(sys.argv[1:])
    sudoku = Sudoku(sys.argv[1])
    sudoku.initialize_board()
    sudoku.solve()
