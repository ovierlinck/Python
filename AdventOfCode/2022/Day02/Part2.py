result = {
    "A X": "Z",
    "A Y": "X",
    "A Z": "Y",
    "B X": "X",
    "B Y": "Y",
    "B Z": "Z",
    "C X": "Y",
    "C Y": "Z",
    "C Z": "X",
}

if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        score = 0
        for line in input:
            move = result[line.strip()]
            score += ord(move) - ord('X') + 1
            score += 3 * (ord(line[2]) - ord('X'))

        print("score=%i" % score)
