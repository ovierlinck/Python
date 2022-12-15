def part1():
    with open("day1.txt", "r") as inFile:
        count = 0
        previous = None
        for line in inFile:
            value = int(line.strip())
            if previous and value > previous:
                count += 1
            previous = value

    print("Nbr of increasing item = %i " % count)


def part2():

    previous = 0
    count = 0
    sums = [0, 0, 0]
    with open("day1.txt", "r") as inFile:
        line1 = inFile.readline()
        line2 = inFile.readline()
        value1 = int(line1.strip())
        value2 = int(line2.strip())

        sums[0] += value1
        sums[0] += value2
        sums[1] += value2

        index = 0

        for line in inFile:
            value = int(line.strip())

            for i in range(3):
                sums[i] += value

            if previous and sums[index] > previous:
                count += 1

            previous = sums[index]
            sums[index] = 0

            index += 1
            index %= 3

    print("Nb of increasing sums = %i" % count)


part2()