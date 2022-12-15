result = {
    "A X": 3,
    "A Y": 6,
    "A Z": 0,
    "B X": 0,
    "B Y": 3,
    "B Z": 6,
    "C X": 6,
    "C Y": 0,
    "C Z": 3,
}

if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        score = 0
        for line in input:
            score += result[line.strip()]
            score += ord(line[2]) - ord('X') + 1

        print("score=%i" % score)
