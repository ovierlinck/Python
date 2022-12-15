def parseList(line):
    """
    Parse the string, starting from '[' until matching ]'
    :param line:
    :return: tuple (data, index after data)
    """
    assert line[0] == '['
    i = 1
    data = []
    valueAsStr = ""
    while i < len(line):
        if line[i] == '[':
            d, remaining = parseList(line[i:])
            data.append(d)
            i += remaining - 1  # +1 will be added later in loop!
        elif line[i] == ']':
            i += 1
            break
        elif line[i] == ',':
            if valueAsStr:
                data.append(int(valueAsStr))
                valueAsStr = ""
        else:
            valueAsStr += line[i]
        i += 1

    if valueAsStr:
        data.append(int(valueAsStr))

    # print("Reading line '%s' until %i (excluded) gives %s" % (line, i, data))
    return data, i


def parseLine(line):
    data, remaining = parseList(line)
    assert remaining == len(line), "%i != %i for line %s" % (remaining, len(line), line)

    # print("%s -> %s" % (line, data))
    return data


def doCompare(data1, data2):
    """
    :param data1: list of XXX
    :param data2: list of XXX
    :return: -1 =inOrder, 0=same, +1=NotInOrder
    """

    assert isinstance(data1, list), "%s should be a list" % data1
    assert isinstance(data2, list), "%s should be a list" % data2

    # 2 lists of same size --> check items
    for i in range(len(data1)):
        v1 = data1[i]
        if len(data2) <= i:
            return 1

        v2 = data2[i]

        if isinstance(v1, int) and isinstance(v2, int):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        else:  # At least one of v1, v2 is a list
            if isinstance(v1, int):
                v1 = [v1]
            if isinstance(v2, int):
                v2 = [v2]
            inOrder = compare(v1, v2)
            if inOrder != 0:
                return inOrder

    if len(data1) < len(data2):
        return -1

    return 0


def compare(data1, data2):
    # print("Comparing %s with %s" % (data1, data2))
    c = doCompare(data1, data2)
    # print("%s %s %s" % (data1, "<=>"[c + 1], data2))
    return c


if __name__ == "__main__":

    with open("data1.txt", "r") as input:
        data1 = None
        data2 = None

        sum = 0
        index = 1
        for line in input:
            line = line.strip()
            if line:
                if data1 is None:
                    data1 = parseLine(line)
                else:
                    data2 = parseLine(line)
            else:
                c = compare(data1, data2)
                print("%s %s %s" % (data1, "<=>"[c + 1], data2))
                if c == -1:
                    sum += index
                data1 = data2 = None
                index += 1

    print("SUM=%i" % sum)
