if __name__ == "__main__":
    with open("data1.txt", "r") as input:
        maxSum = 0
        currentSum = 0
        for line in input:
            if not line.strip():
                maxSum = max(maxSum, currentSum)
                currentSum = 0
                print("temp max = %i" % maxSum)
            else:
                value = int(line)
                currentSum += value

        print("MAX=%i" % maxSum)
