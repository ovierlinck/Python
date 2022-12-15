import os

import networkx


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


def xyToEdge(row, col):
    return row * N + col


if __name__ == "__main__":

    with open("data1.txt", "r") as input:
        previousLine = None
        start = None
        end = None
        G = networkx.DiGraph()

        lineNbr = 0
        for line in input:
            line = line.strip()
            print(line)

            for i in range(len(line)):
                thisEdge = xyToEdge(lineNbr, i)
                if line[i] == "S":
                    start = thisEdge
                elif line[i] == "E":
                    end = thisEdge

            line = line.replace("S", "a").replace("E", "z")

            print(line)

            for i in range(len(line)):
                thisEdge = xyToEdge(lineNbr, i)
                h = ord(line[i])

                if i > 0 and ord(line[i - 1]) <= h + 1:
                    G.add_edge(thisEdge, xyToEdge(lineNbr, i - 1))
                if i < len(line) - 1 and ord(line[i + 1]) <= h + 1:
                    G.add_edge(thisEdge, xyToEdge(lineNbr, i + 1))
                if previousLine:
                    if ord(previousLine[i]) <= h + 1:
                        G.add_edge(thisEdge, xyToEdge(lineNbr - 1, i))
                    if h <= ord(previousLine[i]) + 1:
                        G.add_edge(xyToEdge(lineNbr - 1, i), thisEdge)

            lineNbr += 1
            previousLine = line

        print("Start=%i - End=%i" % (start, end))
        print(G)
        print(G.edges)
        s = networkx.shortest_path(G, start, end)
        print("Shortest path=%s" % s)
        print("Path length=%i  => %i steps" % (len(s), len(s) - 1))

        with open("data1.txt", "r") as input:
            lineNbr = 0
            for line in input:
                line = line.strip()
                msg = ""
                for i in range(len(line)):
                    thisEdge = xyToEdge(lineNbr, i)
                    msg += color_print(line[i], bcolors.RED if thisEdge in s else bcolors.GREEN)
                print(msg)
                lineNbr += 1
