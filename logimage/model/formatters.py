from model.boardFormatter import Formatter


class SimpleFormatter(Formatter):

    def getTitleLine(self, board):
        return ""


    """
    def getCellImage(self, board, row, col):
        # Just an example: same as Formatter but with Full cell in blue
        value = board.get(row, col)
        orig = super().getCellImage(board, row, col)
        if value == model.cellState.CellState.Full:
            return colored("%3s" % orig, bcolors.OKCYAN)
        return orig
    """


    def getRowPrefix(self, board, line):
        index = str(line).rjust(1 if board.nbRows <= 10 else 2)
        return "|%s%s:" % ("*" if board.grid.isCompletedRow(line) else " ", index)


    def getRowSuffix(self, board, line):
        return "|"


    def getColPrefix(self, board, line):
        index = str(line).rjust(1 if board.nbCols <= 10 else 2)
        return "_%s%s¨" % ("*" if board.grid.isCompletedCol(line) else " ", index)


    def getColSuffix(self, board, line):
        return "_"


    def getRowPrefixForColBlocks(self, board, index):
        return "|"


    def getRowSuffixForColBlocks(self, board, index):
        return "|"


    def getColPrefixForRowBlocks(self, board):
        return "_"


    def getColSuffixForRowBlocks(self, board):
        return "_"
