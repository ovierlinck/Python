if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        prio = 0
        lines = [None, None, None]
        for line in input:
            for i in range(3):
                if lines[i] is None:
                    lines[i] = line
                    break

            if lines[2] is not None:
                common2 = {x for x in lines[0] if x in lines[1] and x != '\n'}
                common3 = {x for x in common2 if x in lines[2]}
                common = common3.pop()

                if common <= 'Z':
                    inc = ord(common) - ord('A') + 1 + 26
                else:
                    inc = ord(common) - ord('a') + 1
                print("%s --> %i " % (common, inc))
                lines = [None, None, None]
                prio += inc

        print("prio=%i" % prio)
