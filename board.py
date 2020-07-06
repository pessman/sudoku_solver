import random
from collections import defaultdict

from cell import Cell


class Board:
    def __init__(self):
        self._rows = None
        self._columns = None
        self._quadrants = None
        self._total = []
        self._moves = []

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def quadrants(self):
        return self._quadrants

    def _add_cell_to_row(self, row, cell):
        if self.rows is None:
            self._rows = defaultdict(list)

        self._rows[row].append(cell)

    def _add_cell_to_column(self, column, cell):
        if self.columns is None:
            self._columns = defaultdict(list)

        self._columns[column].append(cell)

    def _add_cell_to_quadrant(self, quadrant, cell):
        if self.quadrants is None:
            self._quadrants = defaultdict(lambda: defaultdict(list))

        self._quadrants[quadrant[0]][quadrant[1]].append(cell)

    def _add_cell(self, row, column, value):
        cell = Cell(row, column, value)
        self._add_cell_to_row(row, cell)
        self._add_cell_to_column(column, cell)
        quadrant = (int(row/3), int(column/3))
        self._add_cell_to_quadrant(quadrant, cell)
        self._total.append(cell)

    def _reset_all_possibilities(self):
        for cell in self._total:
            if not cell.solved:
                cell.add_possibilities(range(1,10))

    def _update_row_possibilites(self):
        for row, cells in self.rows.items():
            row_values = {cell.number for cell in cells if cell.solved}
            for cell in cells:
                if not cell.solved:
                    cell.remove_possibilities(row_values)

    def _update_column_possibilites(self):
        for column, cells in self.columns.items():
            column_values = {cell.number for cell in cells if cell.solved}
            for cell in cells:
                if not cell.solved:
                    cell.remove_possibilities(column_values)

    def _update_quadrant_possibilites(self):
        for quadrant_row_key, quadrant_row_value in self.quadrants.items():
            for quadrant_column_key, quadrant_column_value in quadrant_row_value.items():
                quadrant_values = {cell.number for cell in quadrant_column_value if cell.solved}
                for cell in quadrant_column_value:
                    if not cell.solved:
                        cell.remove_possibilities(quadrant_values)

    def _update_possibilites(self):
        self._reset_all_possibilities()
        self._update_row_possibilites()
        self._update_column_possibilites()
        self._update_quadrant_possibilites()


    def initialize_values(self, values):
        assert self.rows is None and self.columns is None and self.quadrants is None, (
            "Initialize values should only be ran once per sudoku solve"
        )

        for row_index, row in enumerate(values):
            for column_index, value in enumerate(row):
                if value == 0:
                    value = None
                self._add_cell(row_index, column_index, value)

        self._update_possibilites()

    def _conflicts_exist(self):
        """
        TODO: Investigate if the position of the cell (row,column values) matter for the cell that is 
        found to be in conflict. Could potentially help determine how far backtracking must occur.

        Scans the entire sudoku boards cells to see if there are any cells that have no possibilities
        for values. This state indicates that a previous cell value selection was incorrect and
        backtracking must occur.
        
        Returns:
            bool -- True indicates that a cell has no selection options available.
        """
        for cell in self._total:
            if len(cell.possibilities) == 0:
                # print("CONFLICT", cell)
                return True

        return False

    def _make_move(self, cell, value):
        cell.number = value
        cell.update_attempted(value)
        # print("makemove", cell)
        self._moves.append((cell.row, cell.column))

    def _reset_cell(self, cell, reset_attempted=False):
        cell.number = None
        if reset_attempted:
            cell.reset_attempted()
        # print("MOVES", self._moves)
        del self._moves[-1]
        # print("MOVES", self._moves)
        self._update_possibilites()

    def _backtrack(self):
        last_move = self._moves[-1]
        cell = self.rows[last_move[0]][last_move[1]]
        # print("backtrack", cell)
        if not cell.choices_left():
            self._reset_cell(cell, reset_attempted=True)
            if self._moves:
                self._backtrack()
        elif self._moves:
            self._reset_cell(cell, reset_attempted=False)

    def _make_guess(self):
        if self._conflicts_exist():
            self._backtrack()
        next_move = (None, None)
        for cell in self._total:
            if not cell.solved:
                if next_move[1] is None or len(cell.possibilities-cell.attempted) < next_move[1]:
                    next_move = (cell, len(cell.possibilities-cell.attempted))

        cell = next_move[0]
        # print("make guess", cell)
        self._make_move(cell, random.choice(list(cell.possibilities-cell.attempted)))

    def _solved(self):
        if [cell for cell in self._total if not cell.solved]:
            return False

        return True

    def _print_board(self):
        board_text = " --- --- --- \n"
        for row_index, row in enumerate(self.rows.values()):
            row_text = ""
            for index in range(0,9):
                value = row[index].number
                if value is None:
                    value = " "
                row_text = "".join([row_text, str(value)]) if index % 3 else "".join([row_text, f"|{str(value)}"])
            else:
                row_text = "".join([row_text, "|\n"])
            board_text = "".join([board_text, row_text])
            if row_index in [2,5]:
                board_text = "".join([board_text, "|---|---|---|\n"])
        else:
            board_text = "".join([board_text, " --- --- --- \n"])
        return board_text

    def solve(self):
        print(self._print_board())
        while not self._solved():
            self._make_guess()
            self._update_possibilites()
        print(self._print_board())
