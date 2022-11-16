import model.cellState


# Similar to cellState.CellImage but independent: this one is used for debugging, unittest, parsing...  while cellState.CellImage is used for rendering of the Board

LineCellImage = {
    model.cellState.CellState.Unknown: ".",
    model.cellState.CellState.Full: "*",
    model.cellState.CellState.Empty: "/"
}


def getValueFromImage(char):
    """
    Reverse lookup in LineCellImage
    :return: one CellState
    :raise RuntimeError if no match
    """
    for key, value in LineCellImage.items():
        if value == char:
            return key

    raise RuntimeError("No matching image found for '%s'" % char)


class ILine:
    """
    'interface' to a row or column of the board, containing the block definitions and the grid data
    """


    def getBlocks(self):
        """
        :return: iterable of int, defining the block sizes
        """
        pass


    def getLength(self):
        pass


    def getCell(self, index):
        pass


    def setCell(self, index, cellState):
        pass


    def __str__(self):
        return "%s : %s" % (
            self.getBlocks(),
            " ".join(LineCellImage[self.getCell(index)] for index in range(self.getLength()))
        )


    def lineString(self):
        """
        :return: a string representing the line (only the line, without block definition), using LineCellImage
        """
        return "".join(LineCellImage[self.getCell(i)] for i in range(self.getLength()))


    def getFirstKnownCellFrom(self, start):
        """
        :return: tuple (index, value) of first cell which is not 'Unknown' or None, from cell with index 'start' (included)
        """
        for i in range(start, self.getLength()):
            cell = self.getCell(i)
            if cell != model.cellState.CellState.Unknown:
                return i, cell
        return None


    def getFirstKnownCell(self):
        """
        :return: tuple (index, value) of first cell which is not 'Unknown' or None
        """
        return self.getFirstKnownCellFrom(0)


    def getEndOfBlock(self, start):
        """
        :return: index of end of block = index of last consecutive Full block
        """
        assert self.getCell(start) == model.cellState.CellState.Full, "from=%i must be a Full cell but we get %s" % (start, self)
        while start < self.getLength() and self.getCell(start) == model.cellState.CellState.Full:
            start += 1
        return start - 1


class LocalLine(ILine):
    """
    Basic implementation of line with all data stored internally
    """


    def __init__(self, blocks, lineDef):
        """
        :param blocks:
        :param lineDef: either the length of the line (which will be initialized with 'Unknown' or a string valid for fillFromString()
        """
        self.blocks = [block for block in blocks]  # Local copy, as vector
        if isinstance(lineDef, int):
            self.data = [model.cellState.CellState.Unknown] * lineDef
        else:
            self.fillFromString(lineDef)


    def fillFromString(self, txt):
        """
        Replace current data, possibly changing the length
        :param txt:sequence of LineCellImage. Blanks are allowed and ignored
        :return:
        """
        self.data = []
        for c in txt:
            self.data.append(getValueFromImage(c))


    def getBlocks(self):
        return self.blocks


    def getLength(self):
        return len(self.data)


    def getCell(self, index):
        return self.data[index]


    def setCell(self, index, cellState):
        # Design note: do not allow changing a value (override by mistake)
        # But OK to re-set to the same value (easier for algo, useless but harmless)
        assert isinstance(cellState, model.cellState.CellState)
        assert self.getCell(index) in (model.cellState.CellState.Unknown, cellState), \
            "setCell(index=%i, cellState=%s): Can not change cell value. Line is %s" % (index, cellState, self)
        self.data[index] = cellState


class BoardLine(ILine):
    """
    Implementation of line backed by a Board
    """


    def __init__(self, board, index, isRow, isMirror):
        """

        :param board:
        :param index:
        :param isRow:
        :param isMirror: if True, line is mirrored
        :param recorder: if not None, will be notified of cell value changes - must implement IBoardChangeListener
        """
        self.board = board
        self.isRow = isRow
        self.index = index
        self.isMirror = isMirror

        assert (index <= board.nbRows if isRow else index <= board.nbCols)


    def getBlocks(self):
        blocks = self.board.getRowBlocks(self.index) if self.isRow else self.board.getColBlocks(self.index)
        if self.isMirror:
            copy = blocks.copy()
            copy.reverse()
            return copy
        else:
            return blocks


    def getLength(self):
        return self.board.nbCols if self.isRow else self.board.nbRows


    def getCell(self, index):
        if self.isMirror:
            index = self.getLength() - index - 1
        row, col = (self.index, index) if self.isRow else (index, self.index)
        return self.board.get(row, col)


    def setCell(self, index, cellState):
        if self.isMirror:
            index = self.getLength() - index - 1
        row, col = (self.index, index) if self.isRow else (index, self.index)
        self.board.set(row, col, cellState)


class SimplifiedLine(ILine):
    """
    Decorator of an ILine to make it looks simplified
    Simplification means:
        - skip leading/trailing cells until last Empty included
        - skip all corresponding Blocks
    WARNING: simplification is done at creation time (or on request through call to simplify()), it is NOT dynamically updated
    """


    def __init__(self, other):
        assert isinstance(other, ILine)
        self.other = other
        self.first = None  # index of first useful cell in other
        self.last = None  # index of last useful cell in other
        self.firstBlockIndex = None  # index of first useful block in other
        self.lastBlockIndex = None  # index of last useful block in other

        self.evaluate()


    def getBlocks(self):
        return self.other.getBlocks()[self.firstBlockIndex:self.lastBlockIndex + 1]


    def getLength(self):
        return self.last - self.first + 1


    def getCell(self, index):
        return self.other.getCell(self.first + index)


    def setCell(self, index, cellState):
        self.other.setCell(self.first + index, cellState)


    def evaluate(self):
        self.first = self._findFirst()
        self.last = self._findLast()
        self.firstBlockIndex = self.__findFirstBlockIndex()
        self.lastBlockIndex = self.__findLastBlockIndex()


    def _findFirst(self):
        first = 0
        lastEmpty = -1
        while first < self.other.getLength() and \
                self.other.getCell(first) != model.cellState.CellState.Unknown:
            if self.other.getCell(first) == model.cellState.CellState.Empty:
                lastEmpty = first
            first += 1
        first = lastEmpty + 1  # could overflow - TODO???
        return first


    def _findLast(self):
        # TODO: anyway to factorize with _findFirst()? Mirroring?
        last = self.other.getLength() - 1
        lastEmpty = self.other.getLength()
        while last >= 0 and \
                self.other.getCell(last) != model.cellState.CellState.Unknown:
            if self.other.getCell(last) == model.cellState.CellState.Empty:
                lastEmpty = last
            last -= 1
        last = lastEmpty - 1  # could overflow - TODO???
        return last


    def __findFirstBlockIndex(self):
        """
        requires self.first to be set
        """
        return self.__nbBlocksToSimplify(range(self.first))


    def __findLastBlockIndex(self):
        """
        requires self.last to be set
        """
        nbToSimplify = self.__nbBlocksToSimplify(range(self.other.getLength() - 1, self.last + 1, -1))
        nbOthers = len(self.other.getBlocks())
        return nbOthers - 1 - nbToSimplify


    def __nbBlocksToSimplify(self, cellRangeToSimplify):
        """
        requires self.first to be set
        """
        nbBlockToSimplify = 0
        inBlock = False
        for i in cellRangeToSimplify:
            if self.other.getCell(i) == model.cellState.CellState.Empty:
                if inBlock:  # one block just terminated
                    nbBlockToSimplify += 1
                inBlock = False
            elif self.other.getCell(i) == model.cellState.CellState.Full:
                inBlock = True
            else:
                raise RuntimeError("No Unknown cell expected at %i for line %s, with first=%i" % (i, self.other, self.first))

        if inBlock:  # For the last ongoing block
            nbBlockToSimplify += 1

        return nbBlockToSimplify

