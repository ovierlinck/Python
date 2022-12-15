def findEndMarker(line):
    for i in range(len(line) - 4):
        sub = line[i:i + 4]
        letters = set()
        for c in sub:
            letters.add(c)
        if len(letters) == 4:
            print("end of amrker at %i" % (i + 4))
            return i + 4


if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        for line in input:
            findEndMarker(line)
