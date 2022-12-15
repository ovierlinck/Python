def findEndMarker(line):
    N = 14
    for i in range(len(line) - N):
        sub = line[i:i + N]
        letters = set()
        for c in sub:
            letters.add(c)
        if len(letters) == N:
            print("end of marker at %i" % (i + N))
            return


if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        for line in input:
            findEndMarker(line)
