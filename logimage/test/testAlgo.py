import unittest

import algo.algo
import algo.line


class MyTestCase(unittest.TestCase):

    def doTest(self, testedFunction, expectedOutput, lineDef, blocks, expectedBlocks=None):
        """
        Build a LocalLine from inputString + blocks
        Run testedFunction on it
        Check the result, formatted as string, is the same as expectedOutput
        :param testedFunction: a callable taking an ILine a argument and returning a (modified) ILine
        :param expectedOutput:
        :param lineDef: if int, define an empty line of lineDef cells - if string, must be a valid input for LocalLine.fillFromString()
        :param: expectedBlocks: iterable of int = block sizes
        """
        inputLine = algo.line.LocalLine(blocks, lineDef)
        outputLine = testedFunction(inputLine)
        self.assertEqual(expectedOutput, outputLine.lineString())
        if expectedBlocks:
            self.assertEqual(expectedBlocks, outputLine.getBlocks())


    def test_DoF(self):
        self.doTest(algo.algo.solveDoF, "...**...", 8, blocks=[5])
        self.doTest(algo.algo.solveDoF, "........", 8, blocks=[1, 1, 2])
        self.doTest(algo.algo.solveDoF, "**/*/***", 8, blocks=[2, 1, 3])
        self.doTest(algo.algo.solveDoF, ".*....*.", 8, blocks=[2, 1, 2])


    def test_FillFromStart(self):
        # Design note: test in order of logic of 'aspects 'implemented in fillFromStart()
        self.doTest(algo.algo.fillFromStart, "........", "........", blocks=[5])

        # Prolong forward
        self.doTest(algo.algo.fillFromStart, "*****/..", "*.......", blocks=[5])  # and close
        self.doTest(algo.algo.fillFromStart, ".****...", ".*......", blocks=[5])
        self.doTest(algo.algo.fillFromStart, ".**..*..", ".*...*..", blocks=[3])

        # Prolong backward if limited by empty
        self.doTest(algo.algo.fillFromStart, ".**./*..", "..*./*..", blocks=[3])
        self.doTest(algo.algo.fillFromStart, ".....*./", ".....*./", blocks=[3, 1])  # Must no prolong: not sure this is first block

        # Prolong backward if can not combine with next
        self.doTest(algo.algo.fillFromStart, "***/*...", ".**.*...", blocks=[3])  # and close
        self.doTest(algo.algo.fillFromStart, "***/**..", "..*.**..", blocks=[3])  # and close
        self.doTest(algo.algo.fillFromStart, ".**..**.", "..*..**.", blocks=[3])

        # Empty first cells
        self.doTest(algo.algo.fillFromStart, "/..*....", "...*....", blocks=[3])
        self.doTest(algo.algo.fillFromStart, "/.**....", "..**....", blocks=[3])
        self.doTest(algo.algo.fillFromStart, "//***/..", "..***...", blocks=[3])  # and close
        self.doTest(algo.algo.fillFromStart, "//***/*.", "..***.*.", blocks=[3])  # and close
        self.doTest(algo.algo.fillFromStart, "/.*./...", "..*./...", blocks=[2])

        # Close if long enough
        self.doTest(algo.algo.fillFromStart, "*/......", "*.......", blocks=[1])
        self.doTest(algo.algo.fillFromStart, "***/....", "***.....", blocks=[3])
        self.doTest(algo.algo.fillFromStart, "/*/.....", ".*......", blocks=[1])

        # Empty first gap if too small
        self.doTest(algo.algo.fillFromStart, "///.....", "../.....", blocks=[3])

        # Others
        self.doTest(algo.algo.fillFromStart, "......*.", "......*.", blocks=[1, 1])


    def doTestSimplifiedLine(self, expectedOutput, lineDef, blocks, expectedBlocks):

        self.doTest(algo.line.SimplifiedLine, expectedOutput, lineDef, blocks, expectedBlocks=expectedBlocks)

        reversedExpectedOutput = expectedOutput[::-1]
        reversedLineDef = lineDef[::-1]
        reversedBlocks = blocks[::-1]
        reversedExpectedBlocks = expectedBlocks[::-1]
        self.doTest(algo.line.SimplifiedLine, reversedExpectedOutput, reversedLineDef, reversedBlocks, expectedBlocks=reversedExpectedBlocks)


    def test_SimplifiedLine(self):
        self.doTestSimplifiedLine("........", "........", blocks=[5], expectedBlocks=[])
        self.doTestSimplifiedLine(".....", "**/.....", blocks=[2], expectedBlocks=[])
        self.doTestSimplifiedLine("*....", "**/*....", blocks=[2, 3], expectedBlocks=[3])
        self.doTestSimplifiedLine("*....", "///**/*....", blocks=[2, 3], expectedBlocks=[3])
        self.doTestSimplifiedLine("*.*/*...", "*.*/*...", blocks=[3, 2], expectedBlocks=[3, 2])
        self.doTestSimplifiedLine("*.*/*...", "//*.*/*...", blocks=[3, 2], expectedBlocks=[3, 2])

        self.doTestSimplifiedLine(".", "*///.//*", blocks=[1, 1], expectedBlocks=[])


if __name__ == '__main__':
    unittest.main()
