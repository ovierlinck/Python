def computeSignal(i, x):
    if (i - 20) % 40 == 0:
        print("......................... SIGNAL + %i" % (i * x))
        return i * x
    else:
        return 0


if __name__ == "__main__":

    with open("data1.txt", "r") as input:

        i = 1
        x = 1
        signal = 0

        for line in input:
            signal += computeSignal(i, x)

            if line.startswith("addx"):
                increment = int(line.split(" ")[1].strip())
                print("%i %s" % (i, line.strip(" \n")))
                i += 1
                signal += computeSignal(i, x)

                x += increment
                print("%i   +%i => x=%i" % (i, increment, x))
            else:  # noop
                print("%i noop" % i)

            i += 1

    print("SIGNAL=%i" % signal)
