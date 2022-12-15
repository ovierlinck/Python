def part1():
    with open("day3.txt", "r") as inFile:
        nbLines = 0
        ones = []
        gammaRate = []
        N = 12
        for i in range(N):
            ones.append(0)
            gammaRate.append(0)

        for line in inFile:
            value = line.strip()
            for i in range(N):
                if value[i] == '1':
                    ones[i] += 1
            nbLines += 1

        for i in range(N):
            if ones[i] > nbLines / 2:
                gammaRate[i] = 1

    gammaRateInt = int("".join(str(g) for g in gammaRate), 2)
    epsilonRateInt = int("".join(str(1 - g) for g in gammaRate), 2)
    print("gammaRate=%s and as int=%i ; epsilonRate as int=%i; product=%i" % (
        gammaRate, gammaRateInt, epsilonRateInt, gammaRateInt * epsilonRateInt))


def part1Bis():
    with open("day3.txt", "r") as inFile:
        nbLines = 0
        ones = []
        gammaRate = 0
        N = 12
        for i in range(N):
            ones.append(0)

        for line in inFile:
            value = line.strip()
            for i in range(N):
                if value[i] == '1':
                    ones[i] += 1
            nbLines += 1

        for i in range(N):
            if ones[i] > nbLines / 2:
                gammaRate += 2 ** (N - 1 - i)

        epsilonRate = (2 ** N - 1) ^ gammaRate  # Complement a 2 sur N bits

    print("gammaRate=%s and as int=%i ; epsilonRate=%s as int=%i; product=%i" % (
        format(gammaRate, "b"), gammaRate, format(epsilonRate, "b"), epsilonRate, gammaRate * epsilonRate))


part1()
part1Bis()
