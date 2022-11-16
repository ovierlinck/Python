import algo.line
import model.board
import model.cellState
import model.grid


def solveDoF(line):
    """
    Compute degree of freedom and fill defined cell - Does not use possible existing content of line, only block defs and total length
    :param line: one ILine - this line is changed in place
    :return: line, possibly modified
    """
    defs = line.getBlocks()
    neededCells = sum(defs) + len(defs) - 1
    dof = line.getLength() - neededCells

    cursor = 0
    for blockSize in defs:
        if blockSize > dof:
            cursor += dof
            for j in range(blockSize - dof):
                assert line.getCell(cursor) != model.cellState.CellState.Empty, "Cell at index %i of line %s can not be 'Empty'" % (cursor, line)
                line.setCell(cursor, model.cellState.CellState.Full)
                cursor += 1
            if dof == 0 and cursor < line.getLength():
                line.setCell(cursor, model.cellState.CellState.Empty)
        else:
            cursor += blockSize
        cursor += 1

    return line


def _isOnlyOneBlockBefore(line, index):
    """
    :return: True if only one block in line or if only the first can fit before index (excluded), i.e. if not enough room to fit the second block
    """
    blocks = line.getBlocks()
    assert blocks and len(blocks), "Line can not be empty, must have blocks : %s" % line  # Or should be solved explicitly (Empty everywhere,)
    if len(blocks) == 1:
        return True

    firstBlockLength = blocks[0]
    secondBlockLength = blocks[1]

    return firstBlockLength + secondBlockLength + 1 > index


def fillFromStart(line):
    """
    Fill first block, i.e. prolong filled cell to cover length of first block (possibly backward if limited by next block or next empty
    Empty leading cells if would be too long for first block
    Close block ('Empty') if long enough
    :return: line, possibly modified
    """
    blocks = line.getBlocks()
    assert blocks and len(blocks), "Line can not be empty, must have blocks : %s" % line  # Or should be solved explicitly (Empty everywhere,)

    firstBlockLength = blocks[0]

    firstKnownCell = line.getFirstKnownCellFrom(0)
    if firstKnownCell:
        firstKnownIndex, value = firstKnownCell

        if value == model.cellState.CellState.Full:

            # Prolong first block as long as needed
            if firstBlockLength > firstKnownIndex:
                for i in range(firstKnownIndex + 1, firstBlockLength):
                    line.setCell(i, model.cellState.CellState.Full)

            # Prolong backward if block limited by an 'empty' close enough
            secondKnownCell = line.getFirstKnownCellFrom(firstKnownIndex + 1)
            if secondKnownCell:
                secondKnownIndex, value = secondKnownCell
                if value == model.cellState.CellState.Empty and \
                        secondKnownIndex - firstKnownIndex < firstBlockLength and \
                        _isOnlyOneBlockBefore(line, secondKnownIndex):
                    for i in range(secondKnownIndex - firstBlockLength, firstKnownIndex):
                        line.setCell(i, model.cellState.CellState.Full)

            # Prolong backward if block can not join next block (would be too long)
            firstKnownIndex, value = line.getFirstKnownCellFrom(0)  # Refresh firstIndex
            assert value == model.cellState.CellState.Full, "Cell at %i should be Full in line %s" % (firstKnownIndex, line)
            if firstBlockLength > firstKnownIndex:  # First index is part of first block
                endOfFirstBlock = line.getEndOfBlock(firstKnownIndex)
                secondKnownCell = line.getFirstKnownCellFrom(endOfFirstBlock + 1)
                if secondKnownCell:
                    secondKnownIndex, value = secondKnownCell
                    if value == model.cellState.CellState.Full:
                        endOf2ndBlock = line.getEndOfBlock(secondKnownIndex)
                        totalLength = endOf2ndBlock - firstKnownIndex + 1
                        if totalLength > firstBlockLength:  # Combined first and second block would be too long for first block def
                            # First block at most ends at secondKnownIndex-2, so starts at most at secondKnownIndex-2-firstBlockLength+1
                            for i in range(secondKnownIndex - firstBlockLength - 1, firstKnownIndex):
                                line.setCell(i, model.cellState.CellState.Full)

            # Empty leading cell(s) if block 'too long'
            firstKnownIndex, value = line.getFirstKnownCellFrom(0)  # Refresh firstIndex
            assert value == model.cellState.CellState.Full, "Cell at %i should be Full in line %s" % (firstKnownIndex, line)
            if firstBlockLength >= firstKnownIndex:  # First index is part of first block
                endOfBlock = line.getEndOfBlock(firstKnownIndex)
                length = endOfBlock - firstKnownIndex + 1
                assert length <= firstBlockLength, "block [%i-%i] must have a length<%i for line %s" % \
                                                   (firstKnownIndex, endOfBlock, firstBlockLength, line)
                for i in range(0, endOfBlock - firstBlockLength + 1):
                    line.setCell(i, model.cellState.CellState.Empty)

                # Close Block if complete
                if length == firstBlockLength:
                    if endOfBlock + 1 < line.getLength():
                        line.setCell(endOfBlock + 1, model.cellState.CellState.Empty)

        elif value == model.cellState.CellState.Empty:
            # If first gap until Empty is too small for block, mark it as Empty
            if firstBlockLength > firstKnownIndex:
                for i in range(0, firstKnownIndex):
                    line.setCell(i, model.cellState.CellState.Empty)

    return line


def emptyUnknownCells(line):
    assert isinstance(line, algo.line.ILine)
    for i in range(line.getLength()):
        if line.getCell(i) == model.cellState.CellState.Unknown:
            line.setCell(i, model.cellState.CellState.Empty)


def applyRuleOnLines(board, isRow, isMirror, rule):
    """
    Apply the given algo on the given line (rows or columns) of the board
    :param board:
    :param isRow: boolean defining which rows/cols to use
    :param isMirror: boolean defining which rows/cols to use
    :param rule: must be a callable which accept a Line
    :return: the nbr of lines for which one rule was evaluated
    """

    print("Applying rule '%s' for %s (isMirror=%s)" % (getattr(rule, '__name__', str(rule)), "rows" if isRow else "columns", isMirror))
    nbEvaluatedLines = 0
    for index in range(board.nbRows if isRow else board.nbCols):
        completed = board.grid.isCompletedRow(index) if isRow else board.grid.isCompletedCol(index)
        if completed:
            continue
        line = algo.line.BoardLine(board, isRow=isRow, index=index, isMirror=isMirror)
        simplifiedLine = algo.line.SimplifiedLine(line)
        if simplifiedLine.isComplete:
            emptyUnknownCells(line)
        else:
            rule(simplifiedLine)
        nbEvaluatedLines += 1

    return nbEvaluatedLines
