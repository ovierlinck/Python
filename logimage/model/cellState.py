from enum import Enum, auto


class CellState(Enum):
    """
    Possible state of one cell in the grid
    """
    Unknown = auto()
    Full = auto()
    Empty = auto()  # Known to be empty (usually shown as 'crossed')

    def __str__(self):
        return self.name

