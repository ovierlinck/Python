from model.boardFormatter import Formatter
from model.cellState import CellState
from model.formatters import SimpleFormatter
from model.grid import Grid


class Board:
    def __init__(self, rowBlocks, colBlocks):
        """
        :param rowBlocks: iterable of int[], to set definitions of blocks for all rows
        :param colBlocks: iterable of int[], to set definitions of blocks for all columns
        """
        assert sum(sum(block) for block in rowBlocks) == sum(sum(block) for block in colBlocks)

        self.rowBlocks = [blocks for blocks in rowBlocks]
        self.colBlocks = [blocks for blocks in colBlocks]

        self.nbCols = len(self.colBlocks)
        self.nbRows = len(self.rowBlocks)

        self.grid = Grid(self.nbCols, self.nbRows)

        self.formatter = Formatter()


    def addGridListener(self, gridListener):
        self.grid.addListener(gridListener)


    def removeGridListener(self, gridListener):
        self.grid.removeListener(gridListener)


    def setFormatter(self, formatter):
        self.formatter = formatter


    def __str__(self):
        text = self.formatter.getTitleLine(self)

        maxNbRowBlocks = self.getMaxNbRowBlocks()
        maxNbColBlocks = self.getMaxNbColBlocks()

        # Compute some length (=nb characters)
        rowPrefixLength = max(len(self.formatter.getRowPrefix(self, row)) for row in range(self.nbRows))
        rowBlocksLength = 3 * maxNbRowBlocks
        lengthLinePrefixForColsBlocks = max(len(self.formatter.getRowPrefixForColBlocks(self, line)) for line in range(maxNbColBlocks))
        leftToGrid = max(lengthLinePrefixForColsBlocks, rowPrefixLength + rowBlocksLength)

        # If some free place for row blocks (because of long getLinePrefixForColBlocks()), allocate it to the row block (not the row prefix)
        # --> spacesForRowBlock defines the actual length of the rowBlock
        spacesForRowBlock = leftToGrid - rowPrefixLength

        # Prefix of Vertical blocks
        allPrefix = [self.formatter.getColPrefix(self, col) for col in range(self.nbCols)]
        prefixHeight = max(len(prefix) for prefix in allPrefix)
        for height in range(prefixHeight):
            line = self.formatter.getRowPrefixForColBlocks(self, -1)
            if height == 0:
                line += self.formatter.getColPrefixForRowBlocks(self) * (leftToGrid - len(line))
            else:
                line = line.ljust(leftToGrid)

            for col in range(self.nbCols):
                line += "%3s" % allPrefix[col][height]
            line += self.formatter.getRowSuffixForColBlocks(self, -1) + "\n"
            text += line

        # Vertical blocks
        for i in range(maxNbColBlocks):
            prefix = self.formatter.getRowPrefixForColBlocks(self, i)
            line = prefix.ljust(leftToGrid)
            for col in range(self.nbCols):
                blocks = self.getColBlocks(col)
                nbDefs = len(blocks)
                index = i + nbDefs - maxNbColBlocks
                line += ("%3i" % blocks[index]) if index >= 0 else "   "
            line += self.formatter.getRowSuffixForColBlocks(self, i) + "\n"
            text += line

        # Horizontal blocks and grid
        for row in range(self.nbRows):

            line = self.formatter.getRowPrefix(self, row).ljust(rowPrefixLength)
            blockText = ""
            for i in range(maxNbRowBlocks):
                blocks = self.getRowBlocks(row)
                nbDefs = len(blocks)
                index = i + nbDefs - maxNbRowBlocks
                blockText += ("%3i" % blocks[index]) if index >= 0 else "   "
            if spacesForRowBlock > 0:
                blockText = blockText.rjust(spacesForRowBlock)
            line += blockText
            for col in range(self.nbCols):
                image = self.formatter.getCellImage(self, row, col)  # Do not truncate (don't use [:3] as it will remove formatting,colors
                line += "%3s" % image

            text += line + self.formatter.getRowSuffix(self, row) + "\n"

        # Suffix of Vertical blocks
        allSuffix = [self.formatter.getColSuffix(self, col) for col in range(self.nbCols)]
        suffixHeight = max(len(suffix) for suffix in allSuffix)
        for height in range(suffixHeight):
            line = self.formatter.getRowPrefixForColBlocks(self, -1)

            if height == suffixHeight - 1:
                line += self.formatter.getColSuffixForRowBlocks(self) * (leftToGrid - len(line))
            else:
                line = line.ljust(leftToGrid)

            for col in range(self.nbCols):
                line += "%3s" % allSuffix[col][height]

            line += self.formatter.getRowSuffixForColBlocks(self, -1) + "\n"
            text += line

        return text


    def getMaxNbRowBlocks(self):
        return max(len(blocks) for blocks in self.rowBlocks)


    def getMaxNbColBlocks(self):
        return max(len(blocks) for blocks in self.colBlocks)


    def getRowBlocks(self, row):
        """
        :param row:
        :return: 1 BlocksDef
        """
        return self.rowBlocks[row]


    def getColBlocks(self, col):
        """
        :param col:
        :return: 1 BlocksDef
        """
        return self.colBlocks[col]


    def get(self, row, col):
        return self.grid.get(row, col)


    def set(self, row, col, cellState):
        self.grid.set(row, col, cellState)


if __name__ == "__main__":
    board = Board(
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

    board.set(2, 2, CellState.Full)
    board.set(2, 4, CellState.Empty)

    print("%s" % board)

    board.setFormatter(SimpleFormatter())

    print("%s" % board)
