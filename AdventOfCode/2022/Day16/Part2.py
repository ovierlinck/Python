XMAX = 4000000
YMAX = 4000000

# XMAX=20
# YMAX=20

sensors = []  # Tuple (tuple sensor pos, tuple beacon pos, distance)


def testCell(x, y, sensor):
    """
    :return: True if possible
    """
    if x < 0 or x > XMAX:
        return False
    if y < 0 or y > YMAX:
        return False

    for s in sensors:
        if s == sensor:
            continue

        (xs, ys), (xb, yb), dMax = s

        dist = abs(xs - x) + abs(ys - y)
        if dist <= dMax:
            return False

    print("Cell %i, %i is possible --> tuningFreq=%i" % (x, y, x * 4000000 + y))
    return True


def checkBorder(sensor, sensors):
    print("Testing border of sensor %s" % str(sensor))

    (xs, ys), (xb, yb), d = sensor
    for i in range(d + 1):
        testCell(xs + i, ys - d - 1 + i, sensor)
        testCell(xs + d + 1 - i, ys - i, sensor)
        testCell(xs - i, ys + d + 1 - i, sensor)
        testCell(xs - d - 1 + i, ys + i, sensor)


def distanceFromSensor(t):
    s, b, d = t
    return d


if __name__ == "__main__":

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

    for sensor in sensors:
        checkBorder(sensor, sensors)
