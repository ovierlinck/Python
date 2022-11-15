import unittest

import algo.algo
import algo.line
import model.blocksDef


class MyTestCase(unittest.TestCase):

    def doTest(self, testedFunction, expectedOutput, lineDef, *blocks):
        """
        Build a LocalLine from inputString + *blocks
        Run testedFunction on it
        Check the result, formatted as string, is the same as expectedOutput
        :param testedFunction: a callable taking an ILine a argument and returning a (modified) ILine
        :param expectedOutput:
        :param lineDef: if int, define an empty line of lineDef cells - if string, must be a valid input for LocalLine.fillFromString()
        """
        inputLine = algo.line.LocalLine(model.blocksDef.BlocksDef(blocks), lineDef)
        outputLine = testedFunction(inputLine)
        self.assertEqual(expectedOutput, outputLine.lineString())


    def test_DoF(self):
        self.doTest(algo.algo.solveDoF, "...**...", 8, 5)
        self.doTest(algo.algo.solveDoF, "........", 8, 1, 1, 2)
        self.doTest(algo.algo.solveDoF, "**/*/***", 8, 2, 1, 3)
        self.doTest(algo.algo.solveDoF, ".*....*.", 8, 2, 1, 2)


    def test_FillFromStart(self):
        # Design note: test in order of logic of 'aspects 'implemented in fillFromStart()
        self.doTest(algo.algo.fillFromStart, "........", "........", 5)

        # Prolong forward
        self.doTest(algo.algo.fillFromStart, "*****/..", "*.......", 5)  # and close
        self.doTest(algo.algo.fillFromStart, ".****...", ".*......", 5)
        self.doTest(algo.algo.fillFromStart, ".**..*..", ".*...*..", 3)

        # Prolong backward if limited by empty
        self.doTest(algo.algo.fillFromStart, ".**./*..", "..*./*..", 3)
        self.doTest(algo.algo.fillFromStart, ".....*./", ".....*./", 3, 1)  # Must no prolong: not sure this is first block

        # Prolong backward if can not combine with next
        self.doTest(algo.algo.fillFromStart, "***/*...", ".**.*...", 3)  # and close
        self.doTest(algo.algo.fillFromStart, "***/**..", "..*.**..", 3)  # and close
        self.doTest(algo.algo.fillFromStart, ".**..**.", "..*..**.", 3)

        # Empty first cells
        self.doTest(algo.algo.fillFromStart, "/..*....", "...*....", 3)
        self.doTest(algo.algo.fillFromStart, "/.**....", "..**....", 3)
        self.doTest(algo.algo.fillFromStart, "//***/..", "..***...", 3)  # and close
        self.doTest(algo.algo.fillFromStart, "//***/*.", "..***.*.", 3)  # and close
        self.doTest(algo.algo.fillFromStart, "/.*./...", "..*./...", 2)

        # Close if long enough
        self.doTest(algo.algo.fillFromStart, "*/......", "*.......", 1)
        self.doTest(algo.algo.fillFromStart, "***/....", "***.....", 3)
        self.doTest(algo.algo.fillFromStart, "/*/.....", ".*......", 1)

        # Empty first gap if too small
        self.doTest(algo.algo.fillFromStart, "///.....", "../.....", 3)

        # Others
        self.doTest(algo.algo.fillFromStart, "......*.", "......*.", 1, 1)


    def test_SimplifiedLine(self):
        self.doTest(algo.line.SimplifiedLine, "........", "........", 5)
        self.doTest(algo.line.SimplifiedLine, ".....", "**/.....", 5)
        self.doTest(algo.line.SimplifiedLine, ".....", "...../**", 5)
        self.doTest(algo.line.SimplifiedLine, "*....", "**/*....", 5)
        self.doTest(algo.line.SimplifiedLine, "....*", "....*/**", 5)


if __name__ == '__main__':
    unittest.main()
