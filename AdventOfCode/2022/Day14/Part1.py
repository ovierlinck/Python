def extendWidth(cave, width):
    currentWidth = len(cave[0])
    if currentWidth >= width:
        return
    for i in range(len(cave)):
        cave[i] = cave[i] + " " * (width - currentWidth)


def extendHeight(cave, height):
    currentHeight = len(cave)
    if currentHeight >= height:
        return

    currentWidth = len(cave[0])
    for i in range(height - currentHeight):
        cave.append(" " * currentWidth)


def setChar(cave, x, y, char):
    string = cave[y]
    string = string[:x] + char + string[x + 1:]
    cave[y] = string


def fall1Sand(cave, x, y):
    """
    :return: True if sand fall off cave
    """
    stopped = False
    while not stopped:

        if y == len(cave) - 1:
            return True

        if cave[y + 1][x] == " ":
            y += 1
        elif x == 0:
            return True
        elif cave[y + 1][x - 1] == " ":
            y += 1
            x -= 1
        elif x == caveWidth - 1:
            return True
        elif cave[y + 1][x + 1] == " ":
            y += 1
            x += 1
        else:
            stopped = True

    setChar(cave, x, y, "o")


def dumpCave(cave):
    print("-" * 500 + "V" + "-" * 10)
    for line in cave:
        print(line)


def dumpCavePrefix(cave):
    print("   " + "-" * 500 + "V" + "-" * 10)
    for i in range(len(cave)):
        print("%3i%s" % (i, cave[i]))


if __name__ == "__main__":
    cave = [""]

    extendWidth(cave, 500)

    with open("data1.txt", "r") as input:
        for line in input:
            line = line.strip()
            print(line)

            segments = line.split("->")

            start = None
            for point in segments:
                xEnd, yEnd = point.split(",")
                xEnd, yEnd = int(xEnd), int(yEnd)

                extendWidth(cave, xEnd + 1)
                extendHeight(cave, yEnd + 1)

                if start is not None:
                    xStart, yStart = start
                    if xStart == xEnd:
                        for y in range(yStart, yEnd, 1 if yStart < yEnd else -1):
                            setChar(cave, xStart, y, "#")
                        setChar(cave, xStart, yEnd, "#")

                    elif yStart == yEnd:
                        for x in range(xStart, xEnd, 1 if xStart < xEnd else -1):
                            setChar(cave, x, yStart, "#")
                        setChar(cave, xEnd, yStart, "#")
                    else:
                        raise RuntimeError("Diagonal not supported:%s" % line)

                start = xEnd, yEnd

    dumpCave(cave)

    nbSand = 0
    caveHeight = len(cave)
    caveWidth = len(cave[0])

    out = False
    while not out:
        x = 500
        y = 0

        out = fall1Sand(cave, x, y)

        nbSand += 1

    dumpCave(cave)

    print("nbSand=%i" % (nbSand - 1))
