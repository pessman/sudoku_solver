import factory

from cell import Cell


class CellFactory(factory.Factory):
    class Meta:
        model = Cell

    row = 0
    column = 0
    number = None
