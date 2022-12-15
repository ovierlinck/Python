def part1():
    with open("day2.txt", "r") as inFile:
        depth = 0
        x = 0
        for line in inFile:
            move, value = line.strip().split()
            value = int(value)
            if move == "up":
                depth -= value
            elif move == "down":
                depth += value
            elif move == "forward":
                x += value
            else:
                raise RuntimeError("Error in line '%s'" % line)

        print("Depth = %i , X=%i, product = %i" % (depth, x, depth * x))

def part2():
    with open("day2.txt", "r") as inFile:
        aim = 0
        depth = 0
        x = 0
        for line in inFile:
            move, value = line.strip().split()
            value = int(value)
            if move == "up":
                aim -= value
            elif move == "down":
                aim += value
            elif move == "forward":
                x += value
                depth += aim*value
            else:
                raise RuntimeError("Error in line '%s'" % line)

            print("Depth = %i , X=%i, aim=%i, product = %i" % (depth, x, aim, depth * x))


part2()
