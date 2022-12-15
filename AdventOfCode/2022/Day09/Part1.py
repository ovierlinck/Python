if __name__ == "__main__":

    trees = []
    with open("data1.txt", "r") as input:
        for line in input:
            trees.append([int(t) for t in line.strip()])

    height = len(trees)
    width = len(trees[0])

    print("Height=%i / width=%i" % (height, width))

    visibles = []
    visibles.append([True] * width)
    for i in range(height - 2):
        visibles.append([True] + [False] * (width - 2) + [True])
    visibles.append([True] * width)

    for line in range(1, height - 1):

        maxHeight = trees[line][0]
        for col in range(1, width - 1):
            h = trees[line][col]
            if h > maxHeight:
                visibles[line][col] = True
                maxHeight = h

        maxHeight = trees[line][width - 1]
        for col in range(width - 2, 0, -1):
            h = trees[line][col]
            if h > maxHeight:
                visibles[line][col] = True
                maxHeight = h

    for col in range(1, width - 1):

        maxHeight = trees[0][col]
        for line in range(1, height - 1):
            h = trees[line][col]
            if h > maxHeight:
                visibles[line][col] = True
                maxHeight = h

        maxHeight = trees[height - 1][col]
        for line in range(height - 2, 0, -1):
            h = trees[line][col]
            if h > maxHeight:
                visibles[line][col] = True
                maxHeight = h

    count = 0
    for line in visibles:
        print("".join("X" if v else " " for v in line))
        count += line.count(True)

    print("Nb visible = %i" % count)
