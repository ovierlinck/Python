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

    dataFile = "data1.txt"

    with open(dataFile, "r") as input:
        previousLine = None
        starts = []
        end = None
        G = networkx.DiGraph()

        lineNbr = 0
        for line in input:
            line = line.strip()
            print(line)

            for i in range(len(line)):
                thisEdge = xyToEdge(lineNbr, i)
                if line[i] == "E":
                    end = thisEdge

            line = line.replace("S", "a").replace("E", "z")

            print(line)

            for i in range(len(line)):

                thisEdge = xyToEdge(lineNbr, i)

                if line[i] == "a":
                    starts.append(thisEdge)

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

        print("Possible starts:%s " % ", ".join(str(s) for s in starts))
        print("End=%i" % end)
        print(G)
        # print(G.edges)
        shortestPath = None

        print("Trying from each 'a' position' (%i possibilities)" % len(starts))
        for start in starts:
            try:
                s = networkx.shortest_path(G, start, end)
                print("Shortest path from %i: Nb steps=%i" % (start, len(s) - 1))
                if not shortestPath or len(s) < len(shortestPath):
                    shortestPath = s
            except networkx.exception.NetworkXNoPath:
                print("No path found from %i" % start)

        print("Best result: Shortest path from %i: Nb steps=%i" % (shortestPath[0], len(shortestPath) - 1))

        with open(dataFile, "r") as input:
            lineNbr = 0
            for line in input:
                line = line.strip()
                msg = ""
                for i in range(len(line)):
                    thisEdge = xyToEdge(lineNbr, i)
                    msg += color_print(line[i], bcolors.RED if thisEdge in shortestPath else bcolors.GREEN)
                print(msg)
                lineNbr += 1
