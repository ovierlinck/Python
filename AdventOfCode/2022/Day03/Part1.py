if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        prio = 0
        for line in input:
            line = line.strip()
            first = line[0:int(len(line) / 2)]
            second = line[int(len(line) / 2):]
            common = {x for x in first if x in second}
            common = common.pop()
            if common <= 'Z':
                inc = ord(common) - ord('A') + 1 + 26
            else:
                inc = ord(common) - ord('a') + 1

            # print("%s --> %i " % (common, inc))
            prio += inc

        print("prio=%i" % prio)
