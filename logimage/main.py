import algo.algo
import algo.line
import model.board
import model.colors
import model.formatters
import model.grid


class MyGridListener(model.grid.IGridListener):

    def __init__(self):
        self.changedCols = None
        self.changedRows = None
        self.changedCells = None
        self.reset()


    def reset(self):
        self.changedRows = set()
        self.changedCols = set()
        self.changedCells = set()


    def onCellChanged(self, row, col, cellState, oldCellState):
        self.changedRows.add(row)
        self.changedCols.add(col)
        self.changedCells.add((row, col))


listener = MyGridListener()


class MyFormatter(model.formatters.SimpleFormatter):
    def getCellImage(self, board, row, col):
        orig = super().getCellImage(board, row, col)
        if (row, col) in listener.changedCells:
            return model.colors.colored("%3s" % orig, model.colors.Colors.CYAN)
        elif board.grid.isCompletedRow(row) or board.grid.isCompletedCol(col):
            return model.colors.colored("%3s" % orig, model.colors.Colors.YELLOW)

        return orig


def applyRule(board, isMirror, rule):
    board.addGridListener(listener)
    try:
        for isRow in (True, False):
            listener.reset()
            algo.algo.applyRule(board, isRow=isRow, isMirror=isMirror, rule=rule)
            print(board)
            pass
    finally:
        board.removeGridListener(listener)


if __name__ == "__main__":
    board = model.board.Board(
        [
            [5],
            [1, 1],
            [1, 1],
            [1, 1, 1, 1],
            [1, 1],
            [3, 1],
            [1, 1],
            [1, 2, 1, 1],
            [2, 1, 2],
        ],
        [
            [7],
            [1, 1],
            [1, 1, 1],
            [1, 1],
            [1, 1, 1],
            [1, 1],
            [3, 1],
            [6],
        ])

    board.setFormatter(MyFormatter())

    applyRule(board, isMirror=False, rule=algo.algo.solveDoF)

    for isMirror in (False, True):
        applyRule(board, isMirror=isMirror, rule=algo.algo.fillFromStart)
