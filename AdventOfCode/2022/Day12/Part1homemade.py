import os


os.system("")  # Activate the color in windows console


class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def color_print(text, color):
    return color + text + bcolors.END


N = 1000


def add_edge(neighbours, lineFrom, xFrom, lineTo, xTo):
    if not neighbours.get((lineFrom, xFrom)):
        neighbours[(lineFrom, xFrom)] = []
    neighbours[(lineFrom, xFrom)].append((lineTo, xTo))


def dumpDistances(distances, WIDTH, HEIGHT):
    """
    for k, v in distances.items():
        d, fr = v
        print("Distance to %s: %i from %s" % (k, d, fr))
    """

    for line in range(0, HEIGHT):
        msg = ""
        for col in range(0, WIDTH):
            v = distances.get((line, col))
            if v:
                d, fr = v
                msg += "%i" % (d % 10)
            else:
                msg += " "
        print(msg)


def dumpToAnalyze(toAnalyze):
    print("ToAnalyze=%s" % ", ".join("(%s->%s)" % (fr, to) for fr, to in toAnalyze))


if __name__ == "__main__":

    filename = "data1.txt"
    with open(filename, "r") as input:
        previousLine = None
        start = None
        end = None
        neighbours = {}

        lineNbr = 0
        for line in input:
            line = line.strip()
            print(line)
            WIDTH = len(line)

            for i in range(len(line)):
                if line[i] == "S":
                    start = (lineNbr, i)
                elif line[i] == "E":
                    end = (lineNbr, i)

            line = line.replace("S", "a").replace("E", "z")

            # print(line)

            for i in range(len(line)):
                h = ord(line[i])

                if i > 0 and ord(line[i - 1]) <= h + 1:
                    add_edge(neighbours, lineNbr, i, lineNbr, i - 1)
                if i < len(line) - 1 and ord(line[i + 1]) <= h + 1:
                    add_edge(neighbours, lineNbr, i, lineNbr, i + 1)
                if previousLine:
                    if ord(previousLine[i]) <= h + 1:
                        add_edge(neighbours, lineNbr, i, lineNbr - 1, i)
                    if h <= ord(previousLine[i]) + 1:
                        add_edge(neighbours, lineNbr - 1, i, lineNbr, i)

            lineNbr += 1
            previousLine = line

        HEIGHT = lineNbr - 1

        print("Start=%s - End=%s" % (start, end))

        # for f, t in neighbours.items():
        #    print("%s -> %s" % (f, ",".join(str(n) for n in t)))

        distances = {}  # map from start to (distance, from node)

        print("neighbours[start]=%s" % neighbours[start])

        toAnalyze = []  # List of (originNode, neighbour)
        toAnalyze.append((None, start))

        distance = 0
        while toAnalyze:
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------")
            # dumpToAnalyze(toAnalyze)
            dumpDistances(distances, WIDTH, HEIGHT)

            newToAnalyze = {}  # dict targetNode, fromNode
            for originNode, node in toAnalyze:
                if not distances.get(node):
                    distances[node] = (distance, node)

                if neighbours.get(node):
                    for n in neighbours[node]:
                        if not distances.get(n):
                            newToAnalyze[n] = node

            toAnalyze = []
            for target, origin in newToAnalyze.items():
                toAnalyze.append((origin, target))

            distance += 1
        dumpDistances(distances, WIDTH, HEIGHT)
