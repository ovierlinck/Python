from model.cellState import CellState


class IGridListener:
    """
    Interface to implement to register as listener to a Grid
    """


    def onCellChanged(self, row, col, cellState, oldCellState):
        pass


    def onRowCompleted(self, row):
        pass


    def onColCompleted(self, col):
        pass


class Grid:
    """
    The grid part, just a 2D array.
    """


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[CellState.Unknown for y in range(self.height)] for x in range(self.width)]
        self.listeners = []
        self.completedRows = set()
        self.completedCols = set()


    def get(self, row, col):
        return self.cells[col][row]


    def set(self, row, col, cellState):
        """
        Design note: do not allow changing a value (override by mistake)
        But OK to re-set to the same value (easier for algo, useless but harmless) - Does nothing, no notification in such case
        """

        assert cellState != CellState.Unknown, "Can not remove cell at (row:%i, col:%i)" % (row, col)
        assert self.cells[col][row] in (CellState.Unknown, cellState), \
            "Can not replace cell value %s at (row:%i, col:%i) by %s" % (self.cells[col][row], row, col, cellState)

        oldState = self.cells[col][row]
        if oldState == cellState:
            # Nothing to do
            return

        assert row not in self.completedRows, "Can not modify completed row %i (for col %i and value %s)" % (row, col, cellState)
        assert col not in self.completedCols, "Can not modify completed col %i (for row %i and value %s)" % (col, row, cellState)

        self.cells[col][row] = cellState

        rowIsComplete = not any(self.get(row, i) == CellState.Unknown for i in range(self.width))
        colIsComplete = not any(self.get(i, col) == CellState.Unknown for i in range(self.height))
        if rowIsComplete:
            self.completedRows.add(row)
            for listener in self.listeners:
                listener.onRowCompleted(row)
        if colIsComplete:
            self.completedCols.add(row)
            for listener in self.listeners:
                listener.onColCompleted(col)

        for listener in self.listeners:
            listener.onCellChanged(row, col, cellState, oldState)


    def isCompletedRow(self, row):
        return row in self.completedRows


    def isCompletedCol(self, col):
        return col in self.completedCols


    def addListener(self, listener):
        assert isinstance(listener, IGridListener)
        self.listeners.append(listener)


    def removeListener(self, listener):
        self.listeners.remove(listener)
