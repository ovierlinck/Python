from enum import Enum, auto

import algo.algo
import algo.line
import data
import model.board
import model.cellState
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


    def hasRunOnRow(self, row, rule):
        self.changedRows[row].add(rule)


    def hasRunOnCol(self, col, rule):
        self.changedCol[col].add(rule)


class ToDoRulesTracker(model.grid.IGridListener):
    """
    Track which rules needs to be run on which row/col
    """

    class Mode(Enum):
        """
        Define the effect of a cell change: which set of ToDo rules is impacted
        """
        RowOnly = auto()
        ColOnly = auto()
        Both = auto()

    def __init__(self):
        self.remainingRulesOnRows = None
        self.remainingRulesOnCols = None
        self.rules = None
        self.mode = None

        self.reset()


    def setMode(self, mode):
        """
        Tells which ToDo list is impacted by next cell changes
        """
        self.mode = mode


    def setRules(self, rules):
        """
        These rules will be registered as to be done for the next cell change.
        """
        self.rules = {rule for rule in rules}  # internal copy


    def reset(self):
        """
        Empty both ToDo lists - Do no change other state
        """
        self.remainingRulesOnRows = dict()  # From row index to set of rules
        self.remainingRulesOnCols = dict()  # From col index to set of rules


    def hasTodo(self):
        return self.remainingRulesOnRows or \
               self.remainingRulesOnCols


    def onCellChanged(self, row, col, cellState, oldCellState):

        # Special handling for 'Empty', can trigger new 'SimplifiedLine', need to reevaluate all rules

        if self.mode != ToDoRulesTracker.Mode.ColOnly or \
                cellState == model.cellState.CellState.Empty:
            self.remainingRulesOnRows[row] = {rule for rule in self.rules}
        if self.mode != ToDoRulesTracker.Mode.RowOnly or \
                cellState == model.cellState.CellState.Empty:
            self.remainingRulesOnCols[col] = {rule for rule in self.rules}


    def removeEmptyTodo(self, mode):
        if mode != ToDoRulesTracker.Mode.ColOnly:
            keys = [key for key, value in self.remainingRulesOnRows.items() if not value]
            for key in [key for key, value in self.remainingRulesOnRows.items() if not value]:
                del self.remainingRulesOnRows[key]
        if mode != ToDoRulesTracker.Mode.RowOnly:
            for key in [key for key, value in self.remainingRulesOnCols.items() if not value]:
                del self.remainingRulesOnCols[key]


class MyFormatter(model.formatters.SimpleFormatter):

    def __init__(self):
        self.listener = None


    def setGridListener(self, listener):
        self.listener = listener


    def getCellImage(self, board, row, col):
        orig = super().getCellImage(board, row, col)
        if (row, col) in self.listener.changedCells:
            return model.colors.colored("%3s" % orig, model.colors.Colors.CYAN)

        if board.grid.isCompletedRow(row) or board.grid.isCompletedCol(col):
            return model.colors.colored("%3s" % orig, model.colors.Colors.YELLOW)

        return orig


def getRuleName(rule):
    return getattr(rule, '__name__', str(rule))


def applyRuleOnLine(board, index, isRow, rule):
    """
    Simplify line and apply rule on it
    """
    print("   Run %s on %s %i " % (getRuleName(rule), "row" if isRow else "col", index))
    line = algo.line.BoardLine(board, isRow=isRow, index=index)
    simplifiedLine = algo.line.SimplifiedLine(line)
    if simplifiedLine.isComplete:
        algo.algo.emptyUnknownCells(line)
    else:
        rule(simplifiedLine)


def applyRuleOnLines(board, isRow, rule):
    """
    Apply the given algo on the given line (rows or columns) of the board
    :param board:
    :param isRow: boolean defining which rows/cols to use
    :param rule: must be a callable which accept a Line
    :return: the nbr of lines for which one rule was evaluated
    """

    print("Applying rule '%s' for %s" % (getRuleName(rule), "rows" if isRow else "columns"))
    nbEvaluatedLines = 0
    for index in range(board.nbRows if isRow else board.nbCols):
        completed = board.grid.isCompletedRow(index) if isRow else board.grid.isCompletedCol(index)
        if completed:
            continue
        applyRuleOnLine(board, index, isRow, rule)
        nbEvaluatedLines += 1

    return nbEvaluatedLines


def dumpToDoRules(executedRulesListener):
    print("************ ToDo Rules:")
    for row, rules in executedRulesListener.remainingRulesOnRows.items():
        print("   Row %s : %s" % (row, ", ".join(getRuleName(rule) for rule in rules)))
    for col, rules in executedRulesListener.remainingRulesOnCols.items():
        print("   Col %s : %s" % (col, ", ".join(getRuleName(rule) for rule in rules)))
    print("************ end of ToDo Rules")


def solveBoard(board):
    nbEvals = 0

    rulesToDoListener = ToDoRulesTracker()  # Track the changed row/cols and the rules run on them
    rulesToDoListener.setRules((algo.algo.fillFromStart,
                                algo.algo.fillFromEnd,
                                algo.algo.closeSmallBlocks))

    PerCycleListener = MyGridListener()  # Track the changed cells on a complete run of all rules - used to know if something changed (or if completed/blocked) and for formatting

    board.addGridListener(rulesToDoListener)
    board.addGridListener(PerCycleListener)

    formatter = MyFormatter()
    formatter.setGridListener(PerCycleListener)
    board.setFormatter(formatter)

    # Bootstrap list of changed row/col: run on rows and cols (ignore MyListener, not yet populated)
    rulesToDoListener.setMode(ToDoRulesTracker.Mode.Both)
    for isRow in [True, False]:
        nbEvals += applyRuleOnLines(board, isRow, rule=algo.algo.solveDoF)
        print(board)
        dumpToDoRules(rulesToDoListener)

    rulesToDoListener.rules.add(algo.algo.solveDoF)

    # Run remaining rules
    while not board.grid.isCompleted() and rulesToDoListener.hasTodo():

        PerCycleListener.reset()

        for isRow in [True, False]:

            print("=========================== Run TODO rules for %s" % ("rows" if isRow else "cols"))

            rulesToDoListener.setMode(ToDoRulesTracker.Mode.ColOnly if isRow else ToDoRulesTracker.Mode.RowOnly)
            rulesToDo = rulesToDoListener.remainingRulesOnRows if isRow else rulesToDoListener.remainingRulesOnCols
            for row in rulesToDo.keys():

                while rulesToDo[row]:
                    rule = rulesToDo[row].pop()
                    applyRuleOnLine(board, row, isRow=isRow, rule=rule)
                    nbEvals += 1
            rulesToDoListener.removeEmptyTodo(ToDoRulesTracker.Mode.RowOnly if isRow else ToDoRulesTracker.Mode.ColOnly)

            print(board)
            dumpToDoRules(rulesToDoListener)

    board.addGridListener(rulesToDoListener)
    board.removeGridListener(PerCycleListener)

    print("Nb Evals : %i " % nbEvals)


if __name__ == "__main__":
    board = data.boards[60373]

    solveBoard(board)
