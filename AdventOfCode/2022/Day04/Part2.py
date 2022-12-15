def getStartEnd(string):
    parts = string.split("-")
    assert len(parts) == 2
    return int(parts[0]), int(parts[1])


if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        count = 0
        for line in input:
            parts = line.strip().split(",")
            s0, e0 = getStartEnd(parts[0])
            s1, e1 = getStartEnd(parts[1])
            if (s0 <= s1 <= e0) or (s0 <= e1 <= e0) or (s1 <= s0 <= e1) or (s1 <= e0 <= e1):
                count += 1

        print("count=%i" % count)
