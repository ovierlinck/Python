from model.cellState import CellState

CellImage = {
    CellState.Unknown: ".",
    CellState.Full: "██",
    CellState.Empty: "/"
}


class Formatter:
    """
    Basic empty formatter,needed to customize formatting of Board representation
    Also serves Interface definition - override the desired emthods
    Methods can not return NONE values (but can return "")
    """


    def getTitleLine(self, board):
        return ""


    def getCellImage(self, board, row, col):
        """
        :return: text representing the cell; Will be truncated to 3 chars
        """
        cellValue = board.get(row, col)
        return CellImage[cellValue]


    def getRowPrefix(self, board, line):
        """
        For lines of horizontal blocks + grid
        """
        return ""


    def getRowSuffix(self, board, line):
        """
        For lines of horizontal blocks + grid
        """
        return ""


    def getColPrefix(self, board, line):
        """
        Will go above vertical blocks
        WARNING: these will be written in vertical text
        """
        return ""


    def getColSuffix(self, board, line):
        """
        Will go below vertical blocks
        WARNING: these will be written in vertical text
        """
        return ""


    def getRowPrefixForColBlocks(self, board, index):
        """
        Horizontal prefix (=beginning of line) for the representation of the column blocks, prefixes and suffixes
        :param board:
        :param index : row number of the line being written, -1 if line in front of getColPrefix() or getColSuffix()
        """
        return ""


    def getRowSuffixForColBlocks(self, board, index):
        """
        Horizontal suffix (=end of line) for the representation of the column blocks, prefixes and suffixes
        :param board:
        :param index : row number of the line being written, -1 if line in front of getColPrefix() or getColSuffix()
        """
        return ""


    def getColPrefixForRowBlocks(self, board):
        """
        Vertical prefix (=beginning of col) for the representation of the row blocks
        No index, same everywhere
        """
        return ""


    def getColSuffixForRowBlocks(self, board):
        """
        Vertical suffix (=end of col) for the representation of the row blocks
        No index, same everywhere
        """
        return ""
