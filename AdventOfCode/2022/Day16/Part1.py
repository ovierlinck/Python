class Links:
    """
    Store all links (with distance)
    ASSUMPTION: links are symmetric (always exists in pair, same distance in both direction). Store only one

    """


    def __init__(self):
        self._links = {}  # dict (fromName to dict {nextName to distance} }  where fromName<NextName


    def __str__(self):
        return str(self._links)


    def addLink(self, fr, to, distance):
        assert fr != to
        fr, to = min(fr, to), max(fr, to)

        if self._links.get(fr) is None:
            self._links[fr] = {}

        if self._links[fr].get(to) is None:
            self._links[fr][to] = distance


    def removeLink(self, fr, to):
        assert fr != to
        fr, to = min(fr, to), max(fr, to)
        del self._links[fr][to]

        if len(self._links[fr]) == 0:
            del self._links[fr]


    def getOneWayLinks(self, fr):
        links = self._links.get(fr)
        if links:
            return links
        return {}


    def getLinks(self, valve):
        """
        :return: dict (other, distance)
        """
        links = {}
        for fr, dic in self._links.items():
            for to, dist in dic.items():
                if fr == valve:
                    links[to] = dist
                elif to == valve:
                    links[fr] = dist
        return links


    def getDistance(self, fr, to):
        fr, to = min(fr, to), max(fr, to)
        return self._links[fr][to]


def exportAsDot(outputName, valves, links):
    with open(outputName, "w") as output:

        output.write("graph {\n")
        for valve, rate in valves.items():
            output.write('%s [label="%s\\n %i"]\n' % (valve, valve, rate))

        for fr in valves.keys():
            for to, dist in links.getOneWayLinks(fr).items():
                output.write('%s--%s [label="%i"]\n' % (fr, to, dist))

        output.write("}\n")


def parseInput(file):
    # ASSUMPTION: links are symmetric (always exists in pair, same distance in both direction). Store only one
    valves = {}  # from name to rate
    links = Links()

    with open(file, "r") as input:

        for line in input:
            line = line.strip()
            line = line.replace("tunnels", "tunnel").replace("valves", "valve").replace("leads", "lead")
            parts = line.split(" has flow rate=")
            valveName = parts[0][len("Valve "):]

            parts = parts[1].split("; tunnel lead to valve ")
            rate = int(parts[0])
            leads = parts[1].split(", ")

            valves[valveName] = rate
            for lead in leads:
                links.addLink(valveName, lead, 1)

    return valves, links


def removeLink(links, fr, to):
    for l in links[fr]:
        t, dist = l
        if t == to:
            links[fr].remove(l)
            print("remove %s->%s - links are now %s" % (fr, to, links))
            return


def simplify(valves, links, toSimplify):
    for item in toSimplify:
        linksToNeighboors = links.getLinks(item)
        print("Simplifying %s which has links %s" % (item, linksToNeighboors))
        assert len(linksToNeighboors) == 2
        fr, to = linksToNeighboors.keys()
        distance = sum(linksToNeighboors.values())

        links.addLink(fr, to, distance)
        for l in linksToNeighboors.keys():
            links.removeLink(item, l)
        del valves[item]

        # dump(valves, links)


def dump(valves, links):
    print("-----------------------------------------------------------------------")
    print(valves)
    print(links)


nbAnalyzedPaths = 0


def addData(toAnalyze, node, data):
    if toAnalyze.get(node) is None:
        toAnalyze[node] = []
    else:
        if any(data == item for item in toAnalyze[node]):
            return  # already there

    global nbAnalyzedPaths
    nbAnalyzedPaths += 1

    time, flow, open = data
    if not any(time >= otherTime and flow < otherFlow for otherTime, otherFlow, otherOpen in toAnalyze[node]):

        toRemove = []
        for d in toAnalyze[node]:
            otherTime, otherFlow, otherOpen = d
            if time <= otherTime and flow >= otherFlow:
                toRemove.append(d)
        if toRemove:
            # print("before simplification: %s" % toAnalyze[node])
            for d in toRemove:
                toAnalyze[node].remove(d)
            # print("after simplification: %s" % toAnalyze[node])

        toAnalyze[node].append(data)

    #else: print("Not good enough - not added")


def explore(valves, links):
    print("=========Explore ============")

    N = 30
    bestFlow = 0

    toAnalyze = {"AA": [(0, 0, {"AA"})]}  # dict from last node to list of tuple (elapsed time, flow, set of open valves)
    i = 0
    while toAnalyze:

        i += 1
        i %= 100
        if i == 0:
            print("Best=%i / NbPath:%i" % (bestFlow, len(toAnalyze)))

            print("All paths=")
            for path, data in toAnalyze.items():
                print("   %s : %s" % (path, data))

        node = next(iter(toAnalyze.keys()))
        data = toAnalyze.get(node).pop()
        if not toAnalyze[node]:
            del toAnalyze[node]

        # print("Analyzing path %s / Data=%s" % (node, data))

        time, flow, openValves = data
        neighboors = links.getLinks(node)
        for n, distance in neighboors.items():
            newTime = time + distance

            # Add case if we don't open it (even if not yet opened)
            if newTime <= N:
                addData(toAnalyze, n, (newTime, flow, openValves))

            if n not in openValves:
                # case if we open it
                rate = valves.get(n)
                newTime += 1
                remainingTime = N - newTime
                if newTime <= N:
                    newFlow = flow + rate * remainingTime
                    bestFlow = max(bestFlow, newFlow)
                    newOpenValves = openValves.copy()
                    newOpenValves.add(n)
                    if len(newOpenValves) < len(valves):
                        addData(toAnalyze, n, (newTime, newFlow, newOpenValves))
                    #  else: all valves already opened, nothing left to do

    print("Best flow = %i" % bestFlow)


if __name__ == "__main__":

    file = "data1.txt"

    valves, links = parseInput(file)

    dump(valves, links)

    outputName = file.replace(".txt", ".dot")
    exportAsDot(outputName, valves, links)

    toSimplify = []
    for valve, rate in valves.items():
        if rate == 0:
            leads = links.getLinks(valve)
            if len(leads) <= 2:  # not a 'crossing point'!
                toSimplify.append(valve)
            else:
                print("Not possible to simplify %s" % valve)

    print("To Simplify: %s " % toSimplify)

    simplify(valves, links, toSimplify)

    dump(valves, links)

    outputName = file.replace(".txt", ".SIMPLIFIED.dot")
    exportAsDot(outputName, valves, links)

    explore(valves, links)
    print("nbAnalyzedPaths=%i" % nbAnalyzedPaths)
