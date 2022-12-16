from multiprocessing import Pool

def analyzeLine(line, xStart, xEnd, sensors):
    for x in range(xStart, xEnd):

        if x % 1000000 == 0 and line%100==0:
            print("Line=%i x=%i" % (line, x))

        possible = True
        for sensor in sensors:
            (xs, ys), (xb, yb), d = sensor
            if (x, line) == (xb, yb):
                possible = False
                break

            dist = abs(xs - x) + abs(ys - line)
            if dist <= d:
                possible = False
                break

        if possible:
            msg = "%2i: Possible at %i --> tuningFreq=%i" % (line, x, x * 4000000 + line)
            print(msg)
            raise RuntimeError(msg)  # ;-)


def distanceFromSensor(t):
    s, b, d = t
    return d


def analyzeLines(block):
    firstLine, lastLine, sensors=block
    print("Scanning (%i, %i)" % (firstLine, lastLine))
    for line in range(firstLine, lastLine):
        analyzeLine(line, 0, 4000001, sensors)


if __name__ == "__main__":

    sensors = []  # Tuple (tuple sensor pos, tuple beacon pos, distance)

    with open("data1.txt", "r") as input:

        xMin = 99999999999
        xMax = dMax = -99999999999

        width = 0
        for line in input:
            line = line.strip()
            parts = line.split(": closest beacon is at x=")
            assert parts[0].startswith("Sensor at x=")
            xs, ys = parts[0][len("Sensor at x="):].split(", y=")
            xb, yb = parts[1].split(", y=")

            xs, ys = int(xs), int(ys)
            xb, yb = int(xb), int(yb)

            d = abs(xs - xb) + abs(ys - yb)

            xMin = min(xMin, xs, xb)
            xMax = max(xMax, xs, xb)
            dMax = max(dMax, d)

            sensors.append(((xs, ys), (xb, yb), d))

    sensors.sort(key=lambda t: distanceFromSensor(t), reverse=True)
    print("---- SENSORS ---------------------------")
    for sensor in sensors:
        print(sensor)

    N = 20
    lineBlocks = [(thr * 4000000//N, (thr + 1) * 4000000//N,sensors) for thr in range(N) ]
    p = Pool(10)
    p.map(analyzeLines, lineBlocks)
