import algo.line
import model.board
import model.cellState
import model.grid


def _getDegreeOfFreedom(line):
    blocks = line.getBlocks()
    neededCells = sum(blocks) + len(blocks) - 1
    return line.getLength() - neededCells


def solveDoF(line):
    """
    Compute degree of freedom and fill defined cell - Does not use possible existing content of line, only block defs and total length
    :param line: one ILine - this line is changed in place
    :return: line, possibly modified
    """
    dof = _getDegreeOfFreedom(line)

    cursor = 0
    for blockSize in line.getBlocks():
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


def fillFromEnd(line):
    return fillFromStart(algo.line.MirroredLine(line))


def smallestPossibleBlockPositions(blocks):
    """
    Return the smallest possible index (of first cell) for each block (= squeeze them to the left or to the top).
    :param blocks: iterable of int:
    :return: a list of pos, one for each block
    """
    answer = list()
    cursor = 0
    for block in blocks:
        answer.append(cursor)
        cursor += block + 1
    return answer


def possibleBlockIndexes(line, index):
    """
    Find all the blocks which could occupy cell of given index. It ignored the content of the line,only its block and he line length
    (purely based on degree of freedom, not on possible Empty of Full cells)
    :param line:
    :param index:
    :return: a list of block index (NOT block length) referring items from line.getBlocks()
    """
    answer = list()
    dof = _getDegreeOfFreedom(line)
    blocks = line.getBlocks()
    smallestPositions = smallestPossibleBlockPositions(blocks)
    answer = list()
    for i in range(len(smallestPositions)):
        if smallestPositions[i] <= index <= smallestPositions[i] + blocks[i] - 1 + dof:
            answer.append(i)
    return answer


def closeSmallBlocks(line):
    """
    Close block ('Empty' on each side) if long enough
    :return: line, possibly modified
    """
    blocks = line.getBlocks()
    assert blocks and len(blocks), "Line can not be empty, must have blocks : %s" % line  # Or should be solved explicitly (Empty everywhere,)

    # Check if existing block in line is already at its max possible line --> close it
    for start, end in line.extractBlocks():
        possibleIndexes = possibleBlockIndexes(line, start)
        maxBlockLength = max(blocks[i] for i in possibleIndexes)
        length = end - start + 1
        if length == maxBlockLength:  #
            if start > 0:
                line.setCell(start - 1, model.cellState.CellState.Empty)
            if end + 1 < line.getLength():
                line.setCell(end + 1, model.cellState.CellState.Empty)

    # Check if block is limited to the left and must be extended to the right to accommodate minimal possible block length
    for start, end in line.extractBlocks():
        possibleIndexes = possibleBlockIndexes(line, start)
        lastKnownCell = line.getLastKnownCellUntil(start - 1)
        if lastKnownCell:
            lastKnownIndex, lastKnownValue = lastKnownCell
        else:
            lastKnownIndex = -1
            lastKnownValue = model.cellState.CellState.Empty

        if lastKnownValue == model.cellState.CellState.Empty:  # Block is limited to the left by Empty or grid border
            minBlockLength = min(blocks[i] for i in possibleIndexes)
            for i in range(end + 1, lastKnownIndex + minBlockLength + 1):
                line.setCell(i, model.cellState.CellState.Full)

    # Check if block is limited to the right and must be extended to the left to accommodate minimal possible block length
    for start, end in line.extractBlocks():
        possibleIndexes = possibleBlockIndexes(line, start)
        firstKnownCell = line.getFirstKnownCellFrom(end + 1)
        if firstKnownCell:
            firstKnownIndex, firstKnownValue = firstKnownCell
        else:
            firstKnownIndex = line.getLength()
            firstKnownValue = model.cellState.CellState.Empty

        if firstKnownValue == model.cellState.CellState.Empty:  # Block is limited to the right by Empty or grid border
            minBlockLength = min(blocks[i] for i in possibleIndexes)
            for i in range(firstKnownIndex - minBlockLength, start):
                line.setCell(i, model.cellState.CellState.Full)

    # Check if all blocks are found
    extractedBlocks = [end-start+1 for start,end in line.extractBlocks()]
    if extractedBlocks == line.getBlocks():
        for i in range(line.getLength()):
            if line.getCell(i) == model.cellState.CellState.Unknown:
                line.setCell(i, model.cellState.CellState.Empty)

    return line


def emptyUnknownCells(line):
    assert isinstance(line, algo.line.ILine)
    for i in range(line.getLength()):
        if line.getCell(i) == model.cellState.CellState.Unknown:
            line.setCell(i, model.cellState.CellState.Empty)

