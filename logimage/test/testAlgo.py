import unittest

import algo.algo
import algo.line


class AlgoTestCase(unittest.TestCase):

    def doTestLineTransform(self, testedFunction, expectedOutput, lineDef, blocks, expectedBlocks=None):
        """
        Build a LocalLine from inputString + blocks
        Run testedFunction on it
        Check the result, formatted as string, is the same as expectedOutput
        :param testedFunction: a callable taking an ILine a argument and returning a (modified) ILine
        :param expectedOutput: a string representation of the expected line after applying the testedFunction
        :param lineDef: if int, define an empty line of lineDef cells - if string, must be a valid input for LocalLine.fillFromString()
        :param blocks: definition of blocks for that line
        :param expectedBlocks: iterable of int = block sizes
        """
        inputLine = algo.line.LocalLine(blocks, lineDef)
        outputLine = testedFunction(inputLine)
        self.assertEqual(expectedOutput, outputLine.lineString())
        if expectedBlocks:
            self.assertEqual(expectedBlocks, outputLine.getBlocks())


    def doTestSmallestPossibleBlockPositions(self, blocks, expectedPos):
        smallestPos = algo.algo.smallestPossibleBlockPositions(blocks)
        self.assertSequenceEqual(expectedPos, smallestPos)


    def testSmallestPossibleBlockPositions(self):
        self.doTestSmallestPossibleBlockPositions([1, 1, 1], [0, 2, 4])
        self.doTestSmallestPossibleBlockPositions([5, 2, 3], [0, 6, 9])


    def test_DoF(self):
        self.doTestLineTransform(algo.algo.solveDoF, "...**...", 8, blocks=[5])
        self.doTestLineTransform(algo.algo.solveDoF, "........", 8, blocks=[1, 1, 2])
        self.doTestLineTransform(algo.algo.solveDoF, "**/*/***", 8, blocks=[2, 1, 3])
        self.doTestLineTransform(algo.algo.solveDoF, ".*....*.", 8, blocks=[2, 1, 2])


    def test_FillFromStart(self):
        # Design note: test in order of logic of 'aspects 'implemented in fillFromStart()
        self.doTestLineTransform(algo.algo.fillFromStart, "........", "........", blocks=[5])

        # Prolong forward
        self.doTestLineTransform(algo.algo.fillFromStart, "*****/..", "*.......", blocks=[5])  # and close
        self.doTestLineTransform(algo.algo.fillFromStart, ".****...", ".*......", blocks=[5])
        self.doTestLineTransform(algo.algo.fillFromStart, ".**..*..", ".*...*..", blocks=[3])

        # Prolong backward if limited by empty
        self.doTestLineTransform(algo.algo.fillFromStart, ".**./*..", "..*./*..", blocks=[3])
        self.doTestLineTransform(algo.algo.fillFromStart, ".....*./", ".....*./", blocks=[3, 1])  # Must no prolong: not sure this is first block

        # Prolong backward if can not combine with next
        self.doTestLineTransform(algo.algo.fillFromStart, "***/*...", ".**.*...", blocks=[3])  # and close
        self.doTestLineTransform(algo.algo.fillFromStart, "***/**..", "..*.**..", blocks=[3])  # and close
        self.doTestLineTransform(algo.algo.fillFromStart, ".**..**.", "..*..**.", blocks=[3])

        # Empty first cells
        self.doTestLineTransform(algo.algo.fillFromStart, "/..*....", "...*....", blocks=[3])
        self.doTestLineTransform(algo.algo.fillFromStart, "/.**....", "..**....", blocks=[3])
        self.doTestLineTransform(algo.algo.fillFromStart, "//***/..", "..***...", blocks=[3])  # and close
        self.doTestLineTransform(algo.algo.fillFromStart, "//***/*.", "..***.*.", blocks=[3])  # and close
        self.doTestLineTransform(algo.algo.fillFromStart, "/.*./...", "..*./...", blocks=[2])

        # Close if long enough
        self.doTestLineTransform(algo.algo.fillFromStart, "*/......", "*.......", blocks=[1])
        self.doTestLineTransform(algo.algo.fillFromStart, "***/....", "***.....", blocks=[3])
        self.doTestLineTransform(algo.algo.fillFromStart, "/*/.....", ".*......", blocks=[1])

        # Empty first gap if too small
        self.doTestLineTransform(algo.algo.fillFromStart, "///.....", "../.....", blocks=[3])

        # Others
        self.doTestLineTransform(algo.algo.fillFromStart, "......*.", "......*.", blocks=[1, 1])


    def doTestSimplifiedLine(self, expectedOutput, lineDef, blocks, expectedBlocks):
        self.doTestLineTransform(algo.line.SimplifiedLine, expectedOutput, lineDef, blocks, expectedBlocks=expectedBlocks)

        reversedExpectedOutput = expectedOutput[::-1]
        reversedLineDef = lineDef[::-1]
        reversedBlocks = blocks[::-1]
        reversedExpectedBlocks = expectedBlocks[::-1]
        self.doTestLineTransform(algo.line.SimplifiedLine, reversedExpectedOutput, reversedLineDef, reversedBlocks,
                                 expectedBlocks=reversedExpectedBlocks)


    def test_SimplifiedLine(self):
        self.doTestSimplifiedLine("........", "........", blocks=[5], expectedBlocks=[])
        self.doTestSimplifiedLine(".....", "**/.....", blocks=[2], expectedBlocks=[])
        self.doTestSimplifiedLine("*....", "**/*....", blocks=[2, 3], expectedBlocks=[3])
        self.doTestSimplifiedLine("*....", "///**/*....", blocks=[2, 3], expectedBlocks=[3])
        self.doTestSimplifiedLine("*.*/*...", "*.*/*...", blocks=[3, 2], expectedBlocks=[3, 2])
        self.doTestSimplifiedLine("*.*/*...", "//*.*/*...", blocks=[3, 2], expectedBlocks=[3, 2])

        self.doTestSimplifiedLine(".", "*///.//*", blocks=[1, 1], expectedBlocks=[])


    def doTestSmallestPossibleBlockPositions(self, blocks, expectedPos):
        smallestPos = algo.algo.smallestPossibleBlockPositions(blocks)
        self.assertSequenceEqual(expectedPos, smallestPos)


    def testSmallestPossibleBlockPositions(self):
        self.doTestSmallestPossibleBlockPositions([1, 1, 1], [0, 2, 4])
        self.doTestSmallestPossibleBlockPositions([5, 2, 3], [0, 6, 9])


    def doTestPossibleBlockIndexes(self, lineDef, blocks, index, expectedIndexes):
        inputLine = algo.line.LocalLine(blocks, lineDef)
        indexes = algo.algo.possibleBlockIndexes(inputLine, index)
        self.assertSequenceEqual(expectedIndexes, indexes)


    def testPossibleBlockIndexes(self):
        self.doTestPossibleBlockIndexes(8, [3], 0, [0])
        self.doTestPossibleBlockIndexes(8, [3], 1, [0])
        self.doTestPossibleBlockIndexes(8, [3], 2, [0])
        self.doTestPossibleBlockIndexes(8, [3], 3, [0])
        self.doTestPossibleBlockIndexes(8, [3], 4, [0])
        self.doTestPossibleBlockIndexes(8, [3], 7, [0])

        self.doTestPossibleBlockIndexes(8, [3, 2], 0, [0])
        self.doTestPossibleBlockIndexes(8, [3, 2], 1, [0])
        self.doTestPossibleBlockIndexes(8, [3, 2], 2, [0])
        self.doTestPossibleBlockIndexes(8, [3, 2], 3, [0])
        self.doTestPossibleBlockIndexes(8, [3, 2], 4, [0, 1])
        self.doTestPossibleBlockIndexes(8, [3, 2], 5, [1])
        self.doTestPossibleBlockIndexes(8, [3, 2], 6, [1])
        self.doTestPossibleBlockIndexes(8, [3, 2], 7, [1])


    def testCloseSmallBlocks(self):

        self.doTestLineTransform(algo.algo.closeSmallBlocks, "...../*/", "......*.", blocks=[1, 1])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "...../*/", "......*.", blocks=[2, 1])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "..*../*/", "..*...*.", blocks=[2, 1])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "/**///*/", ".**...*.", blocks=[2, 1])

        self.doTestLineTransform(algo.algo.closeSmallBlocks, ".***./*/", ".**...*.", blocks=[4, 1])

        self.doTestLineTransform(algo.algo.closeSmallBlocks, "****/...", ".*../...", blocks=[4, 3])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "****/***", ".**./.*.", blocks=[4, 3])

        self.doTestLineTransform(algo.algo.closeSmallBlocks, "/**/..../**/..../**/", ".**......**......**.", blocks=[2, 2, 2, 2])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "/**//////**//////**/", ".**......**......**.", blocks=[2, 2, 2])
        self.doTestLineTransform(algo.algo.closeSmallBlocks, "/**//////***/////**/", ".**......***.....**.", blocks=[2, 3, 2])


if __name__ == '__main__':
    unittest.main()
