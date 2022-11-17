import algo.algo
import algo.line
import data
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


def applyRuleOnLines(board, isRow, rule):
    """
    Apply the given algo on the given line (rows or columns) of the board
    :param board:
    :param isRow: boolean defining which rows/cols to use
    :param isMirror: boolean defining which rows/cols to use
    :param rule: must be a callable which accept a Line
    :return: the nbr of lines for which one rule was evaluated
    """

    print("Applying rule '%s' for %s" % (getattr(rule, '__name__', str(rule)), "rows" if isRow else "columns"))
    nbEvaluatedLines = 0
    for index in range(board.nbRows if isRow else board.nbCols):
        completed = board.grid.isCompletedRow(index) if isRow else board.grid.isCompletedCol(index)
        if completed:
            continue
        line = algo.line.BoardLine(board, isRow=isRow, index=index)
        simplifiedLine = algo.line.SimplifiedLine(line)
        if simplifiedLine.isComplete:
            algo.algo.emptyUnknownCells(line)
        else:
            rule(simplifiedLine)
        nbEvaluatedLines += 1

    return nbEvaluatedLines


def applyRuleOnRowsAndCols(board, rule):
    """
    Apply the given rules on all rows and all cols of the board
    :param board:
    :param rule: the rule, a callable taking a ILine as arg
    :return: the nb of rules evaluation
    """
    nbEvals = 0
    board.addGridListener(PerRuleRunListener)
    try:
        for isRow in (True, False):
            PerRuleRunListener.reset()
            nbEvals += applyRuleOnLines(board, isRow=isRow, rule=rule)
            print(board)
            if board.grid.isCompleted():
                break
            pass
    finally:
        board.removeGridListener(PerRuleRunListener)

    return nbEvals


if __name__ == "__main__":

    board = data.boards[60373]

    board.setFormatter(MyFormatter())

    nbCycles = 0
    nbBoardRules = 0
    nbEvals = 0
    changed = True
    board.addGridListener(PerCycleListener)

    while changed and not board.grid.isCompleted():
        print("================================================================================================")
        PerCycleListener.reset()

        for rule in (algo.algo.solveDoF,
                     algo.algo.fillFromStart,
                     algo.algo.fillFromEnd,
                     algo.algo.closeSmallBlocks):

            if not board.grid.isCompleted():
                nbEvals += applyRuleOnRowsAndCols(board, rule=rule)
                nbBoardRules += 1

        nbCycles += 1

        changed = bool(PerCycleListener.changedCells)

    board.removeGridListener(PerCycleListener)

    print("Nbr of cycle of rule set : %i / Nbr of board-level rule evaluations : %i / Nbr of line-level rule evaluations : %i" %
          (nbCycles, nbBoardRules, nbEvals))
