if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        stacks = []
        readingStacks = True
        for line in input:
            if readingStacks:
                if line.startswith(" 1   2"):
                    readingStacks = False
                    for s in stacks:
                        print(s)
                else:
                    for i in range(int(len(line) / 4)):
                        char = line[i * 4 + 1]
                        if char != ' ':
                            while len(stacks) <= i:
                                stacks.append(list())
                            stacks[i].append(char)

            else:
                if line.startswith("move"):  # to skip blank line after stack titles
                    parts = line.split(" ")
                    n = int(parts[1])
                    fr = int(parts[3]) - 1
                    to = int(parts[5]) - 1
                    toMove = list()
                    for i in range(n):
                        toMove.append(stacks[fr].pop(0))
                    toMove.reverse()
                    for v in toMove:
                        stacks[to].insert(0, v)

        print("After the moves:")
        message = ""
        for s in stacks:
            print(s)
            message += s[0]
        print("Message = %s " % message)
