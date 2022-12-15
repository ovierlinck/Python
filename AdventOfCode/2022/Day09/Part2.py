def getScore(col, treeLine):
    """
    Count visible tree from col to beginning of line
    """
    maxHeight = treeLine[col]
    for i in range(col - 1, -1, -1):
        if treeLine[i] >= maxHeight:
            return col - i
    return col


def getScoreLeft(line, col, trees):
    return getScore(col, trees[line])


def getScoreRight(line, col, trees):
    treeLine = trees[line][::-1]
    return getScore(len(treeLine) - col - 1, treeLine)


def getScoreUp(line, col, trees):
    treeLine = [trees[l][col] for l in range(len(trees))]
    return getScore(line, treeLine)


def getScoreDown(line, col, trees):
    treeLine = [trees[l][col] for l in range(len(trees))][::-1]
    return getScore(len(trees) - line - 1, treeLine)


if __name__ == "__main__":

    trees = []
    with open("data1.txt", "r") as input:
        for line in input:
            trees.append([int(t) for t in line.strip()])

    height = len(trees)
    width = len(trees[0])

    print("Height=%i / width=%i" % (height, width))

    maxScore = 0
    for line in range(1, height - 1):
        msg = ""
        for col in range(1, width - 1):
            score = getScoreLeft(line, col, trees) * getScoreRight(line, col, trees) * getScoreUp(line, col, trees) * getScoreDown(line, col, trees)
            maxScore = max(maxScore, score)

    print(maxScore)
