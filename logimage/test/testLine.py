import unittest

import algo.line


class LineTestCase(unittest.TestCase):

    def doTestExtractBlocks(self, expectedBlocks, lineDef):
        inputLine = algo.line.LocalLine([], lineDef)
        extractedBlocks = inputLine.extractBlocks()
        self.assertSequenceEqual(expectedBlocks, extractedBlocks)


    def testExtractBlocks(self):
        self.doTestExtractBlocks(((2, 2), (5, 5)), "..*..*..")
        self.doTestExtractBlocks(((2, 5),), "..****..")
        self.doTestExtractBlocks(((0, 3),), "****..")
        self.doTestExtractBlocks(((1, 3), (5, 5)), "/***.*")
        self.doTestExtractBlocks(((5, 5),), ".....*")


if __name__ == '__main__':
    unittest.main()
