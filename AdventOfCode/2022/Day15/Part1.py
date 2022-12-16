def analyzeLine(line, xStart, xEnd, sensors):
    countNotPossible = 0
    for x in range(xStart, xEnd):

        if x % 100000 == 0:
            print(x)

        possible = True
        for sensor in sensors:
            (xs, ys), (xb, yb) = sensor
            if (x, line) == (xb, yb):
                possible = True
                break

            d = abs(xs - xb) + abs(ys - yb)

            dist = abs(xs - x) + abs(ys - line)
            if dist <= d:
                possible = False
                break

        if not possible:
            countNotPossible += 1

    print("%2i: #Impossible=%i" % (line, countNotPossible))


if __name__ == "__main__":

    with open("data1.txt", "r") as input:
        sensors = []

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

            sensors.append(((xs, ys), (xb, yb)))

    analyzeLine(2000000, xMin - dMax, xMax + dMax, sensors)
