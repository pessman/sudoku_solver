import pytest

from test.factories import CellFactory


class TestCell:
    def test_solved(self):
        cell = CellFactory()
        assert not cell.solved