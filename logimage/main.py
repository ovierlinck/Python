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


PerRuleRunListener = MyGridListener()  # Track the changed cells (on the last run), used for formatting - frequently reset
PerCycleListener = MyGridListener()  # Track the changed cells on a complete run of all rules - used to know if something changed (or if completed/blocked)


class MyFormatter(model.formatters.SimpleFormatter):
    def getCellImage(self, board, row, col):
        orig = super().getCellImage(board, row, col)
        if (row, col) in PerRuleRunListener.changedCells:
            return model.colors.colored("%3s" % orig, model.colors.Colors.CYAN)
        elif board.grid.isCompletedRow(row) or board.grid.isCompletedCol(col):
            return model.colors.colored("%3s" % orig, model.colors.Colors.YELLOW)

        return orig


def applyRuleOnRowsAndCols(board, isMirror, rule):
    """
    Apply the given rules on all rows and all cols of the board
    :param board:
    :param isMirror:
    :param rule: the rule, a callable taking a ILine as arg
    :return: the nb of rules evaluation
    """
    nbEvals = 0
    board.addGridListener(PerRuleRunListener)
    try:
        for isRow in (True, False):
            PerRuleRunListener.reset()
            nbEvals += algo.algo.applyRuleOnLines(board, isRow=isRow, isMirror=isMirror, rule=rule)
            print(board)
            if board.grid.isCompleted():
                break
            pass
    finally:
        board.removeGridListener(PerRuleRunListener)

    return nbEvals


if __name__ == "__main__":

    # 59367 from nonograms.org
    board = model.board.Board(
        [
            [5],
            [1, 1],
            [1, 1],
            [1, 1, 1, 1],
            [1, 1],
            [1, 1],
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

    # 55917 from nonograms.org
    board = model.board.Board(
        [
            [3],
            [1, 1],
            [1, 1, 1],
            [3, 1],
            [5, 1],
            [1, 1, 1],
            [1, 4],
            [1, 1, 1],
            [1, 2, 2],
            [2, 3, 1]
        ],
        [
            [1],
            [2, 3],
            [4, 1, 1],
            [1, 3],
            [1, 1, 1, 2],
            [1, 1, 2],
            [4, 1, 1],
            [1, 1],
            [1, 1],
            [5],
        ])

    board.setFormatter(MyFormatter())

    nbCycles = 0
    nbBoardRules = 0
    nbEvals = 0
    changed = True
    board.addGridListener(PerCycleListener)

    while changed and not board.grid.isCompleted():
        print("================================================================================================")
        PerCycleListener.reset()

        nbEvals += applyRuleOnRowsAndCols(board, isMirror=False, rule=algo.algo.solveDoF)
        nbBoardRules += 1

        for isMirror in (False, True):
            if board.grid.isCompleted():
                break
            nbEvals += applyRuleOnRowsAndCols(board, isMirror=isMirror, rule=algo.algo.fillFromStart)
            nbBoardRules += 1

        changed = bool(PerCycleListener.changedCells)
        nbCycles += 1

    board.removeGridListener(PerCycleListener)

    print("Nbr of cycle of rule set : %i / Nbr of board-level rule evaluations : %i / Nbr of line-level rule evaluations : %i" %
          (nbCycles, nbBoardRules, nbEvals))
