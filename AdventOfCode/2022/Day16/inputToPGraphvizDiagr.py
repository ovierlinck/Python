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

        if len(self._links[fr])==0:
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

        dump(valves, links)


def dump(valves, links):
    print("-----------------------------------------------------------------------")
    print(valves)
    print(links)


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
